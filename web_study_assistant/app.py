import re
import json
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from groq import Groq
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "studyassistant2026"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Database setup
def init_db():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS quiz_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  topic TEXT,
                  score TEXT,
                  date TEXT)''')
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def create_user(username, password):
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    hashed = generate_password_hash(password)
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

def save_quiz(user_id, topic, score):
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute("INSERT INTO quiz_history (user_id, topic, score, date) VALUES (?, ?, ?, ?)",
              (user_id, topic, score, datetime.now().strftime("%d %b %Y, %I:%M %p")))
    conn.commit()
    conn.close()

def get_history(user_id):
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute("SELECT topic, score, date FROM quiz_history WHERE user_id = ? ORDER BY id DESC", (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def convert_markdown(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    text = text.replace('\n\n', '</p><p>').replace('\n', '<br>')
    return f'<p>{text}</p>'

def explain_topic(topic):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a study assistant. Explain topics clearly and simply for a college student."},
            {"role": "user", "content": f"Explain this topic in simple terms: {topic}"}
        ]
    )
    result = response.choices[0].message.content
    return convert_markdown(result)

def generate_quiz(topic):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": """You are a quiz generator. Return ONLY a JSON array with exactly 3 questions. No extra text before or after. Format:
[
  {
    "question": "question text",
    "options": ["option A", "option B", "option C", "option D"],
    "answer": "option A"
  }
]"""},
            {"role": "user", "content": f"Generate a quiz on: {topic}"}
        ]
    )
    result = response.choices[0].message.content
    result = result.strip()
    if result.startswith("```"):
        result = result.split("```")[1]
        if result.startswith("json"):
            result = result[4:]
    return json.loads(result)

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if create_user(username, password):
            return redirect(url_for("login"))
        else:
            error = "Username already taken."
    return render_template("register.html", error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = get_user(username)
        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect(url_for("index"))
        else:
            error = "Invalid username or password."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    explanation = None
    quiz = None
    topic = None
    score = None
    results = None

    if request.method == "POST":
        topic = request.form.get("topic")
        action = request.form.get("action")

        if action == "explain":
            explanation = explain_topic(topic)

        elif action == "quiz":
            quiz = generate_quiz(topic)

        elif action == "submit_quiz":
            quiz_data = json.loads(request.form.get("quiz_data"))
            correct = 0
            results = []
            for i, q in enumerate(quiz_data):
                user_answer = request.form.get(f"q{i}")
                is_correct = user_answer == q["answer"]
                if is_correct:
                    correct += 1
                results.append({
                    "question": q["question"],
                    "options": q["options"],
                    "correct_answer": q["answer"],
                    "user_answer": user_answer,
                    "is_correct": is_correct
                })
            score = f"{correct}/{len(quiz_data)}"
            save_quiz(session["user_id"], topic, score)

    return render_template("index.html",
                         explanation=explanation,
                         quiz=quiz,
                         topic=topic,
                         score=score,
                         results=results)

@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect(url_for("login"))
    records = get_history(session["user_id"])
    return render_template("history.html", records=records)

if __name__ == "__main__":
    init_db()
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
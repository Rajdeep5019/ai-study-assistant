import re
import json
from flask import Flask, render_template, request
from groq import Groq
import os

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

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

@app.route("/", methods=["GET", "POST"])
def index():
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

    return render_template("index.html",
                         explanation=explanation,
                         quiz=quiz,
                         topic=topic,
                         score=score,
                         results=results)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
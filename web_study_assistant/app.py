from unittest import result

import re

def convert_markdown(text):
    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Headers
    text = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    # Line breaks
    text = text.replace('\n\n', '</p><p>').replace('\n', '<br>')
    return f'<p>{text}</p>'
from flask import Flask, render_template, request
from groq import Groq
import os

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

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
            {"role": "system", "content": "You are a quiz generator. Generate exactly 3 multiple choice questions with 4 options each. At the end clearly write the correct answers."},
            {"role": "user", "content": f"Generate a quiz on this topic: {topic}"}
        ]
    )
    response.choices[0].message.content
    return markdown.markdown(result)
 
@app.route("/", methods=["GET", "POST"])
def index():
    explanation = None
    quiz = None
    topic = None
    if request.method == "POST":
        topic = request.form.get("topic")
        action = request.form.get("action")
        if action == "explain":
            explanation = explain_topic(topic)
        elif action == "quiz":
            quiz = generate_quiz(topic)
    return render_template("index.html", explanation=explanation, quiz=quiz, topic=topic)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
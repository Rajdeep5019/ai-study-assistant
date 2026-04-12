from groq import Groq

import os
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def explain_topic(topic):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a study assistant. Explain topics clearly and simply for a college student."},
            {"role": "user", "content": f"Explain the topic in simple terms: {topic}"}
        ]
    )
    return response.choices[0].message.content

def generate_quiz(topic):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a study assistant. Generate a quiz with 5 questions and answers based on the given topic."},
            {"role": "user", "content": f"Generate a quiz for the topic: {topic}"}
        ]
    )
    return response.choices[0].message.content

def save_session(topic, explanation, quiz):
    filename = f"{topic}_study_session.txt"
    with open(filename, "w") as f:
        f.write(f"TOPIC: {topic}\n")
        f.write("="*50 + "\n\n")
        f.write("EXPLANATION:\n")
        f.write(explanation + "\n\n")
        f.write("="*50 + "\n\n")
        f.write("QUIZ:\n")
        f.write(quiz + "\n")
    print(f"\nSession saved to {filename}")

topic = input("Enter a topic you want to study: ")

explanation = explain_topic(topic)
quiz = generate_quiz(topic)

print("\n--- Explanation ---")
print(explanation)

print("\n--- Quiz ---")
print(quiz)

save_session(topic, explanation, quiz)
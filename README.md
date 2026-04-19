 # AI Study Assistant

A full-stack AI-powered web application that helps students learn any topic through explanations and interactive quizzes.

## Live Demo
https://ai-study-assistant-x4xw.onrender.com

## Features
- **Topic Explainer** — Enter any topic and get a clear, simple explanation powered by LLaMA 3.3
- **Interactive Quiz** — Generate a 3-question MCQ quiz on any topic with instant answer checking
- **Score Display** — See your score and which answers were correct or wrong after submission
- **Quiz History** — All past quiz attempts saved per user with topic, score, and date
- **User Authentication** — Register, login, logout with securely hashed passwords

## Tech Stack
- **Backend** — Python, Flask
- **AI Model** — LLaMA 3.3 via Groq API
- **Database** — SQLite
- **Frontend** — HTML, CSS
- **Deployment** — Render

## How to Run Locally

1. Clone the repository
   git clone https://github.com/Rajdeep5019/ai-study-assistant.git

2. Install dependencies
   pip install flask groq markdown werkzeug

3. Set your Groq API key
   On Windows PowerShell:
   $env:GROQ_API_KEY="your-key-here"

4. Run the app
   cd web_study_assistant
   python app.py

5. Open browser at http://127.0.0.1:5000

## Project Structure
web_study_assistant/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── Procfile               # Render deployment config
└── templates/
├── index.html         # Main app page
├── login.html         # Login page
├── register.html      # Registration page
└── history.html       # Quiz history page

## What I Learned
- REST API integration with Python
- AI model API usage via Groq
- Full-stack web development with Flask
- User authentication and password hashing
- SQLite database design and queries
- Git version control and GitHub
- Cloud deployment on Render

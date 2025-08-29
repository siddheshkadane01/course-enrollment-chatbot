# AI Course Chatbot (FastAPI + Web UI)

A simple, human-friendly AI chatbot that helps students explore a course, ask questions, and register — all in one place. It runs on FastAPI (backend) with a clean web interface (HTML/CSS/JS). OpenAI powers the conversation, and Google Sheets can store registrations.

## What it does
- Chat with an AI about the course (topics, price, duration, outcomes)
- Keeps short conversation context for more natural replies
- One-click registration form (optional Google Sheets saving)
- Handy API docs at /docs for testing
- Clean, responsive frontend you can share quickly

## Tech
- Backend: FastAPI, Pydantic
- AI: OpenAI (GPT-4o-mini by default)
- Data (optional): Google Sheets via gspread
- Frontend: Vanilla HTML/CSS/JS (served by FastAPI)

## Quick start
1) Install
- Create/activate a venv
- pip install -r requirements.txt

2) Configure
- Copy .env.example to .env
- Add your OPENAI_API_KEY (and Google Sheets creds if you want registrations saved)

3) Run
- uvicorn main:app --host 0.0.0.0 --port 8000
- Open http://localhost:8000 (chat UI)
- Visit http://localhost:8000/docs (API docs)

## Endpoints
- POST /start — quick intro
- POST /chat — send user message, get AI reply
- POST /register — register interest (optionally writes to Google Sheets)
- GET /course-info — course details shown in the UI
- GET /health — quick health check

## Screenshots
- Web chat UI (index.html)
- Mobile-friendly, with typing indicator and clean layout

## Why this project
- Great starter to demo an AI assistant with a real use case
- Easy to deploy, easy to extend (swap model, add auth, store chats)

## License
MIT — use it, remix it, ship it.

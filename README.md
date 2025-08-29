# AI Course Chatbot (FastAPI + Web UI)

A simple, human-friendly AI chatbot that helps students explore a course, ask questions, and register — all in one place. It runs on FastAPI (backend) with a clean web interface (HTML/CSS/JS). OpenAI powers the conversation, and Google Sheets can store registrations.

Think of it as a conversational landing page for your course: visitors get instant answers, see the essentials, and can register without back-and-forth emails.

## What it does
- Chat with an AI about the course (topics, price, duration, outcomes)
- Keeps short conversation context for more natural replies
- One-click registration form (optional Google Sheets saving)
- Handy API docs at /docs for testing
- Clean, responsive frontend you can share quickly

## Why it’s useful
- Reduces repetitive Q&A and saves support time
- Increases conversion with an interactive, friendly UX
- API-first design makes it easy to integrate elsewhere

## How it works (at a glance)
- Frontend (HTML/CSS/JS) sends messages to FastAPI
- FastAPI calls OpenAI (GPT-4o-mini) and returns a reply
- Short-term context keeps chats coherent
- Optional Google Sheets stores registrations for easy follow-up

## Customize in minutes
- UI: tweak colors/fonts in `static/style.css`
- Model: change `OPENAI_MODEL` in `.env`
- Course info: adjust the `/course-info` response in `main.py`
- Form: edit fields in `static/index.html` and `/register` handler

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

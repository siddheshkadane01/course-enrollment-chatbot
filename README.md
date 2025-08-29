# AI Course Chatbot — FastAPI + OpenAI + Web UI

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-async-green?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange)](https://platform.openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## TL;DR
A clean, end‑to‑end AI chatbot that answers course questions and collects registrations. Backend: FastAPI. Frontend: vanilla HTML/CSS/JS. AI: OpenAI. Optional Google Sheets to store leads.

## What it does
- Chat about the course (topics, price, duration, outcomes)
- Short conversation memory for more natural replies
- One‑click registration form (optional Google Sheets saving)
- Swagger docs at `/docs` and a responsive web UI at `/`

## Demo chat (realistic snippet)
```
You: Hey! What does this course cover?
Bot: It's a hands‑on AI & ML bootcamp. You'll learn Python, data prep, model training
     (regression → classification → CNNs), deployment basics, and portfolio tips.

You: How long is it and what's the price?
Bot: 12 weeks, weekend-friendly. Standard price is $999. Scholarships available.

You: Can I register here?
Bot: Yep! Click "Register" in the UI or send your name/email/phone and I’ll log it.
```

## Run it locally
```bash
# 1) Install
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) Configure
cp .env.example .env
# add your OPENAI_API_KEY to .env

# 3) Start
uvicorn main:app --host 0.0.0.0 --port 8000
# UI: http://localhost:8000  |  API docs: http://localhost:8000/docs
```

## Quick API test
```bash
# Intro
curl -s -X POST http://localhost:8000/start | jq

# Chat
curl -s -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"demo","message":"Tell me about the syllabus"}' | jq

# Register (Google Sheets optional)
curl -s -X POST http://localhost:8000/register \
  -H 'Content-Type: application/json' \
  -d '{"name":"Alex","email":"alex@example.com","phone":"1234567890","course":"AI Bootcamp"}' | jq
```

## Tech highlights (what I used and why)
- FastAPI (async) + Pydantic models for fast, typed APIs
- OpenAI GPT‑4o‑mini for lightweight, contextual responses
- Conversation memory (short sliding window) per user
- Google Sheets via `gspread` for simple, ops‑friendly lead storage
- Clean web UI (semantic HTML, CSS variables, subtle animations, fetch API)
- CORS enabled, OpenAPI/Swagger out of the box

## Customize in minutes
- UI theme: `static/style.css`
- Course info: `/course-info` in `main.py`
- Model choice: `OPENAI_MODEL` in `.env`
- Form fields: `static/index.html` + `/register` in `main.py`

## Endpoints
- POST `/start` — quick intro
- POST `/chat` — user message → AI reply
- POST `/register` — save interest (optionally to Google Sheets)
- GET `/course-info` — course details for the UI
- GET `/health` — health check

## Tests
```bash
python -m pytest -q test_chatbot.py
```

## Why this project
A practical, portfolio‑ready example of building an AI assistant end‑to‑end: API design, model integration, state handling, and a shareable UI—cleanly packaged for recruiters and real users.

## License
MIT

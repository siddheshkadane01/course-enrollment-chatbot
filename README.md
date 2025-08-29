# 🤖 AI Course Chatbot with FastAPI

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive full-stack AI-powered chatbot built with FastAPI and modern web technologies. Features intelligent course information, student registration, and a beautiful responsive web interface.

## 🌟 Live Demo

- **Web Interface**: http://localhost:8000 (when running locally)
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🎯 Project Overview

This project demonstrates a complete full-stack AI chatbot application with:
- **Backend**: FastAPI with OpenAI GPT-4o-mini integration
- **Frontend**: Modern HTML/CSS/JavaScript with responsive design
- **Database**: Google Sheets API for data persistence
- **Features**: Real-time chat, user registration, course information
- **Architecture**: RESTful API with comprehensive documentation

## ✨ Key Features

### 🤖 AI & Backend
- **Intelligent Conversations** - OpenAI GPT-4o-mini powered responses
- **Context Management** - Maintains conversation history for personalized interactions
- **Course Information** - Comprehensive course details and FAQ handling
- **Student Registration** - Complete signup flow with validation
- **Google Sheets Integration** - Automatic data persistence
- **Health Monitoring** - System status and configuration checking

### 🌐 Frontend & UI
- **Modern Web Interface** - Beautiful, responsive chat interface
- **Real-time Messaging** - Instant chat with typing indicators
- **Mobile Responsive** - Works perfectly on all devices
- **Registration Modal** - Smooth user onboarding experience
- **Course Sidebar** - Interactive course information display
- **Gradient Animations** - Modern UI with smooth transitions

### 🛠️ Developer Experience
- **FastAPI Framework** - Auto-generated OpenAPI documentation
- **Error Handling** - Graceful error responses and logging
- **CORS Support** - Frontend-backend integration ready
- **Static File Serving** - Integrated web server
- **Hot Reload** - Development-friendly setup

## 📁 Project Structure

```
ai-course-chatbot/
├── 🖥️ Backend
│   ├── main.py                     # Main FastAPI application with AI functionality
│   ├── demo_chatbot.py            # Demo version (no API keys required)
│   ├── test_chatbot.py            # Comprehensive test suite
│   └── requirements.txt           # Python dependencies
├── 🌐 Frontend
│   └── static/
│       ├── index.html             # Modern chat interface
│       ├── style.css              # Responsive styling with animations
│       └── script.js              # Chat functionality and API integration
├── 📋 Configuration
│   ├── .gitignore                 # Git ignore rules
│   ├── .env.example              # Environment variables template
│   └── credentials.json.example   # Google Sheets API template
├── 📖 Documentation
│   ├── README.md                  # This comprehensive guide
│   ├── FIXED_INSTRUCTIONS.md     # Troubleshooting guide
│   └── PROJECT_OVERVIEW.md       # Detailed features and usage
└── 📄 Logs
    ├── ai_server.log             # Server logs (auto-generated)
    └── frontend_server.log       # Frontend server logs
```

## � Screenshots & Demo

### Web Interface
![Chat Interface](https://via.placeholder.com/800x500/4f46e5/ffffff?text=Modern+Chat+Interface)
*Modern, responsive chat interface with real-time messaging*

### API Documentation
![API Docs](https://via.placeholder.com/800x500/059669/ffffff?text=FastAPI+Swagger+Documentation)
*Auto-generated interactive API documentation*

### Mobile Responsive
![Mobile View](https://via.placeholder.com/300x600/dc2626/ffffff?text=Mobile+Responsive+Design)
*Fully responsive design for all devices*

## 🚀 Quick Start

### One-Command Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd ai-course-chatbot

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your-openai-api-key-here"

# Start the server
python main.py
```

### 🌐 Access Your App
- **Web Interface**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

**Method 2: Update .env.example**
```bash
# Copy and rename the example file
cp .env.example .env
# Edit .env with your actual API key
nano .env
```

**Method 3: Direct in Code (for testing)**
Edit `main.py` line 66:
```python
OPENAI_API_KEY = "your-openai-api-key-here"
```

### Step 4: Setup Google Sheets (Optional but Recommended)

#### Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable **Google Sheets API** and **Google Drive API**

#### Create Service Account
1. Navigate to "APIs & Services" > "Credentials"  
2. Click "Create Credentials" > "Service Account"
3. Download the JSON credentials file
4. Rename to `credentials.json` and place in project root

#### Setup Google Sheet  
1. Create a Google Sheet named "Course Registrations"
2. Share with your service account email (from credentials.json)
3. Grant "Editor" permissions

### Step 5: Test Installation

```bash
# Quick health check
/Users/siddhesh/Downloads/INTERN/.venv/bin/python -c "
import openai
from openai import OpenAI
print('✅ OpenAI package working')
import fastapi
print('✅ FastAPI working')
import gspread  
print('✅ Google Sheets integration ready')
print('🎉 All systems ready!')
"
```

## 🚀 Running the Application

### ⚠️ Important: Use Virtual Environment Python

**Always use the full path to avoid "command not found" errors:**
```bash
/Users/siddhesh/Downloads/INTERN/.venv/bin/python
```

### Option 1: Full AI Chatbot (Recommended)

```bash
# Navigate to project directory
cd /Users/siddhesh/Downloads/INTERN

# Set your OpenAI API key
export OPENAI_API_KEY="your-openai-api-key-here"

# Start the main AI server
/Users/siddhesh/Downloads/INTERN/.venv/bin/python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Access Points:**
- **API Server**: `http://localhost:8000`
- **Interactive Docs**: `http://localhost:8000/docs` 
- **Health Check**: `http://localhost:8000/health`

### Option 2: Demo Version (No API Keys Required)

```bash
# Start demo server with pre-programmed responses
/Users/siddhesh/Downloads/INTERN/.venv/bin/python demo_chatbot.py
```

**Access Points:**
- **Demo Server**: `http://localhost:8001`
- **Demo Docs**: `http://localhost:8001/docs`

### Option 3: Easy Startup Script

```bash
# Make executable and run
chmod +x start_server.sh
./start_server.sh
```

### Option 4: Background Server

```bash
# Run server in background
cd /Users/siddhesh/Downloads/INTERN
nohup /Users/siddhesh/Downloads/INTERN/.venv/bin/python -c "
import os
os.environ['OPENAI_API_KEY'] = 'your-key-here'
import uvicorn
uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=False)
" > server.log 2>&1 &

# Check if running
curl -X GET "http://localhost:8000/health"
```

## 📚 API Endpoints & Usage

### 🔗 Available Endpoints

| Method | Endpoint | Description | Status |
|--------|----------|-------------|---------|
| GET | `/` | API information and available endpoints | ✅ |
| POST | `/start` | Start new conversation (Telegram-style) | ✅ |
| POST | `/chat` | Send message to AI chatbot | ✅ |
| POST | `/register` | Register for course | ✅ |
| GET | `/course-info` | Get complete course information | ✅ |
| GET | `/health` | System health and configuration status | ✅ |
| GET | `/docs` | Interactive API documentation (Swagger) | ✅ |

### 🧪 Testing Your Chatbot

#### Automated Testing
```bash
# Run comprehensive test suite
/Users/siddhesh/Downloads/INTERN/.venv/bin/python test_chatbot.py

# Interactive chat session
/Users/siddhesh/Downloads/INTERN/.venv/bin/python test_chatbot.py interactive
```

#### Manual API Testing

**1. Health Check**
```bash
curl -X GET "http://localhost:8000/health"
# Expected: {"status":"healthy","openai_configured":true,...}
```

**2. Start Conversation**
```bash
curl -X POST "http://localhost:8000/start" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "test_user_123", "message": "hello"}'
```

**3. Chat with AI**
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "test_user_123", "message": "What is the course duration?"}'
```

**4. Register Student**
```bash
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john.doe@example.com",
       "phone": "+1-555-0123",
       "user_id": "test_user_123"
     }'
```

**5. Get Course Information**
```bash
curl -X GET "http://localhost:8000/course-info"
```

## 💬 Example API Usage

### Start a Conversation

```bash
curl -X POST "http://localhost:8000/start" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "user123", "message": "hello"}'
```

### Chat with the Bot

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "user123", "message": "What is the course duration?"}'
```

### Register for Course

```bash
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john.doe@example.com",
       "phone": "+1-555-0123",
       "user_id": "user123"
     }'
```

## 🎛️ Easy Customization

### 📝 Modify Course Information

Edit the `COURSE_INFO` dictionary in `main.py` (lines 18-35):

```python
COURSE_INFO = {
    "name": "Your Course Name Here",
    "duration": "Your Duration (e.g., 8 weeks)",
    "price": "Your Price (e.g., $199)",
    "instructor": "Your Instructor Name",
    "format": "Your Format (e.g., Online/In-person)",
    "schedule": "Your Schedule (e.g., Tues/Thu 6-8 PM)",
    "description": "Your course description...",
    "benefits": [
        "Your benefit 1",
        "Your benefit 2",
        "Add as many as needed"
    ],
    "prerequisites": "Your prerequisites or 'None'",
    "support": "Your support details"
}
```

### ❓ Update FAQ Responses  

Edit the `FAQ_RESPONSES` dictionary in `main.py` (lines 37-50):

```python
FAQ_RESPONSES = {
    "duration": "Your custom duration response",
    "price": "Your custom pricing response", 
    "benefits": "Your custom benefits response",
    "schedule": "Your custom schedule response",
    "registration": "Your custom registration instructions",
    # Add more FAQs as needed
    "new_topic": "Response for new topic"
}
```

### 🤖 Modify AI Behavior

Update the `get_system_prompt()` function (around line 170) to change how the AI responds:

```python
def get_system_prompt() -> str:
    return f"""
You are a helpful AI assistant for [YOUR COURSE NAME].

IMPORTANT INSTRUCTIONS:
- Be friendly and encouraging
- Focus on [YOUR SPECIFIC TOPICS]
- Always mention [YOUR KEY SELLING POINTS]
- If unsure, direct to support at [YOUR EMAIL]

COURSE DETAILS:
[Your custom course information here]
"""
```

## 🔧 Configuration & Settings

### OpenAI Model Settings

In `generate_ai_response()` function, customize:
```python
response = openai_client.chat.completions.create(
    model="gpt-4o-mini",        # or "gpt-4" for more advanced responses
    max_tokens=500,             # Adjust response length (150-1000)
    temperature=0.7             # Control creativity (0.0-1.0)
)
```

### Conversation Context Management

Default: Keeps last 5 exchanges per user. To modify, edit `update_conversation_context()`:
```python
# Keep only last N exchanges 
if len(conversation_contexts[user_id]) > N:
    conversation_contexts[user_id] = conversation_contexts[user_id][-N:]
```

### Google Sheets Configuration

```python
# In main.py, update these variables:
GOOGLE_CREDENTIALS_PATH = "path/to/your/credentials.json"
GOOGLE_SHEET_NAME = "Your Sheet Name"
```

## 🚨 Troubleshooting Common Issues

### Issue 1: "python: command not found"
**Solution**: Use the full virtual environment path
```bash
# ❌ Wrong
python main.py

# ✅ Correct  
/Users/siddhesh/Downloads/INTERN/.venv/bin/python main.py
```

### Issue 2: "OpenAI API Error: insufficient_quota"
**Cause**: Your OpenAI account needs credits  
**Solution**: 
1. Visit [OpenAI Billing](https://platform.openai.com/account/billing)
2. Add credits to your account ($5 minimum)
3. Restart the server

### Issue 3: "ModuleNotFoundError"  
**Solution**: Reinstall dependencies
```bash
/Users/siddhesh/Downloads/INTERN/.venv/bin/python -m pip install -r requirements.txt
```

### Issue 4: Server Won't Start
**Check**: Are you in the right directory?
```bash
cd /Users/siddhesh/Downloads/INTERN
pwd  # Should show: /Users/siddhesh/Downloads/INTERN
```

### Issue 5: Google Sheets Not Saving
**Check**: 
1. Service account email has access to sheet
2. `credentials.json` is in project root
3. Sheet name matches `GOOGLE_SHEET_NAME` variable

### Issue 6: Port Already in Use  
**Solution**: Kill existing processes or use different port
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --port 8001
```

## � System Monitoring & Health

### Health Check Endpoint

```bash
curl -X GET "http://localhost:8000/health"
```

**Healthy Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-29T22:39:40.133519",
  "openai_configured": true,
  "google_sheets_configured": false
}
```

### Server Logs

```bash
# View real-time logs (if running in background)
tail -f ai_server.log

# Check for errors
grep -i error ai_server.log
```

### Performance Monitoring

- **Response Time**: Check `/docs` for endpoint response times
- **Context Usage**: Monitor `context_length` in chat responses  
- **Registration Success**: Check `sheets_saved` in registration responses

## 🔒 Security & Best Practices

### API Key Security
- ✅ Never commit API keys to version control
- ✅ Use environment variables or `.env` files
- ✅ Rotate API keys regularly
- ✅ Monitor API usage and billing

### Input Validation  
- ✅ Pydantic models validate all inputs
- ✅ Email format validation for registrations
- ✅ Phone number format checking
- ✅ SQL injection protection (using proper ORM patterns)

### Rate Limiting (Production Recommendation)
```python
# Add to main.py for production
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# Apply to endpoints
@app.post("/chat")
@limiter.limit("10/minute")
async def chat_with_bot(request: Request, chat_data: ChatMessage):
    # ... existing code
```

## 🚀 Production Deployment

### Environment Variables for Production
```bash
export OPENAI_API_KEY="your-production-key"
export GOOGLE_CREDENTIALS_PATH="/app/credentials.json"  
export GOOGLE_SHEET_NAME="Production Course Registrations"
export HOST="0.0.0.0"
export PORT="8000"
```

### Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t ai-chatbot .
docker run -p 8000:8000 -e OPENAI_API_KEY="your-key" ai-chatbot
```

### Reverse Proxy with Nginx (Production)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## � Advanced Features & Extensions

### Webhook Integration
Add webhook support for external systems:
```python
@app.post("/webhook")
async def receive_webhook(data: dict):
    # Process webhook data
    # Integrate with CRM, email systems, etc.
    return {"status": "received"}
```

### Multi-Language Support
```python
COURSE_INFO_LANGUAGES = {
    "en": {"name": "Complete Python Development Bootcamp"},
    "es": {"name": "Bootcamp Completo de Desarrollo Python"},
    "fr": {"name": "Bootcamp Complet de Développement Python"}
}
```

### Email Notifications
```python
# Add email sending capability
import smtplib
from email.mime.text import MIMEText

async def send_confirmation_email(registration_data):
    # Implementation for email confirmations
    pass
```

### Database Integration  
```python
# Replace in-memory storage with database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# PostgreSQL/MySQL integration for production
```

### Analytics Dashboard
```python
@app.get("/analytics")
async def get_analytics():
    return {
        "total_registrations": len(registrations),
        "conversations_today": count_conversations_today(),
        "popular_questions": get_popular_questions()
    }
```

## 🎓 Learning Outcomes & Skills Demonstrated

This project showcases proficiency in:

### Backend Development
- ✅ **FastAPI Framework** - Modern Python web framework
- ✅ **RESTful API Design** - Proper HTTP methods and status codes
- ✅ **Pydantic Validation** - Data modeling and validation
- ✅ **Async Programming** - Asynchronous request handling

### AI Integration  
- ✅ **OpenAI API** - GPT model integration and prompt engineering
- ✅ **Context Management** - Conversation state handling
- ✅ **Error Handling** - Graceful API failure management

### External APIs
- ✅ **Google Sheets API** - Data persistence and automation
- ✅ **OAuth 2.0** - Service account authentication
- ✅ **API Rate Limiting** - Production-ready request management

### Software Engineering
- ✅ **Environment Management** - Virtual environments and dependencies  
- ✅ **Configuration Management** - Environment variables and settings
- ✅ **Logging & Monitoring** - Application health and debugging
- ✅ **Documentation** - Comprehensive API documentation
- ✅ **Testing** - Automated testing and validation

### DevOps & Deployment
- ✅ **Process Management** - Background service handling
- ✅ **Health Monitoring** - System status endpoints
- ✅ **Production Readiness** - Security and scalability considerations

## 🤝 Contributing & Support

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Getting Help
- 📧 **Email**: Create an issue in the repository
- 📚 **Documentation**: Check `/docs` endpoint when server is running
- 🐛 **Bug Reports**: Use the issue tracker
- 💡 **Feature Requests**: Open an enhancement issue

### Project Roadmap
- [ ] Web frontend interface (React/Vue.js)
- [ ] WhatsApp integration
- [ ] Payment processing (Stripe/PayPal)
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Voice message support
- [ ] Mobile app integration

## � License & Credits

### License
This project is open source and available under the **MIT License**.

### Credits & Acknowledgments
- **FastAPI** - Modern web framework for building APIs
- **OpenAI** - GPT models for intelligent responses  
- **Google Sheets API** - Data persistence and automation
- **Pydantic** - Data validation and settings management
- **Uvicorn** - Lightning-fast ASGI server

---

## 🎉 Quick Start Summary

```bash
# 1. Navigate to project
cd /Users/siddhesh/Downloads/INTERN

# 2. Set your OpenAI API key
export OPENAI_API_KEY="your-key-here"

# 3. Start the server  
/Users/siddhesh/Downloads/INTERN/.venv/bin/python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 4. Open interactive documentation
open http://localhost:8000/docs

# 5. Test the chatbot
curl -X POST "http://localhost:8000/start" -H "Content-Type: application/json" -d '{"user_id": "test", "message": "hello"}'
```

**🎯 Your AI-powered course chatbot is ready to help students learn about your course and handle registrations! 🤖✨**

**For immediate testing without OpenAI credits, run the demo version:**
```bash
/Users/siddhesh/Downloads/INTERN/.venv/bin/python demo_chatbot.py
# Then visit: http://localhost:8001/docs
```

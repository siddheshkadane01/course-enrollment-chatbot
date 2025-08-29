"""
Simple Demo Script - Run the chatbot with mock responses
========================================================

This script demonstrates the chatbot functionality without requiring OpenAI API key.
It uses hardcoded responses for testing and demonstration purposes.
"""

import json
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List, Optional

app = FastAPI(title="Demo Course Chatbot")

# Simple in-memory conversation storage
conversations: Dict[str, List[Dict]] = {}

# Course information (same as main app)
COURSE_INFO = {
    "name": "Complete Python Development Bootcamp",
    "duration": "12 weeks (3 months)",
    "price": "$299",
    "instructor": "John Smith",
    "format": "Online with live sessions",
    "schedule": "Monday, Wednesday, Friday - 7:00 PM to 9:00 PM EST"
}

class ChatMessage(BaseModel):
    user_id: str
    message: str

class RegistrationData(BaseModel):
    name: str
    email: str
    phone: str
    user_id: Optional[str] = None

def get_demo_response(message: str) -> str:
    """Generate demo responses without AI"""
    message_lower = message.lower()
    
    # Greeting responses
    if any(word in message_lower for word in ["hello", "hi", "start", "hey"]):
        return f"""👋 Welcome to {COURSE_INFO['name']}!

I'm here to help you learn about our Python development course. Here's what I can tell you:

📚 **Course:** {COURSE_INFO['name']}
⏰ **Duration:** {COURSE_INFO['duration']}
💰 **Price:** {COURSE_INFO['price']}
👨‍💻 **Instructor:** {COURSE_INFO['instructor']}

Ask me about:
- Course details and schedule
- Pricing and payment options  
- How to register
- Course benefits

What would you like to know?"""

    # FAQ responses
    elif "duration" in message_lower:
        return f"The course runs for {COURSE_INFO['duration']}. Classes are held {COURSE_INFO['schedule']}."
    
    elif "price" in message_lower or "cost" in message_lower:
        return f"The course costs {COURSE_INFO['price']}. We offer flexible payment plans if needed!"
    
    elif "schedule" in message_lower or "time" in message_lower:
        return f"Classes are scheduled for {COURSE_INFO['schedule']}. All sessions are recorded if you miss any!"
    
    elif "register" in message_lower:
        return "Great! To register, I'll need your name, email, and phone number. You can use the /register endpoint or tell me you'd like to sign up!"
    
    elif "instructor" in message_lower or "teacher" in message_lower:
        return f"Your instructor is {COURSE_INFO['instructor']}, an experienced Python developer with 8+ years in the industry."
    
    elif "benefits" in message_lower or "learn" in message_lower:
        return """🎯 **Course Benefits:**
✅ Learn Python from beginner to advanced
✅ Build real-world projects
✅ Get hands-on experience with frameworks
✅ Receive a certificate of completion
✅ Access to lifetime materials
✅ 1-on-1 mentorship sessions
✅ Job placement assistance"""
    
    else:
        return f"""I understand you're asking about: "{message}"

I'm a demo version, so I have pre-programmed responses for common questions like:
- Course duration and schedule
- Pricing information
- Registration process
- Course benefits
- Instructor details

Try asking: "What is the course duration?" or "How much does it cost?" or "How do I register?"

For the full AI experience, set up the OpenAI API key in the main application! 🤖"""

@app.post("/start")
async def start_conversation(data: ChatMessage):
    """Start demo conversation"""
    conversations[data.user_id] = []
    response = get_demo_response("hello")
    
    conversations[data.user_id].append({
        "user": data.message,
        "bot": response,
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "response": response,
        "context_length": len(conversations[data.user_id]),
        "demo_mode": True
    }

@app.post("/chat")
async def chat(data: ChatMessage):
    """Demo chat endpoint"""
    if data.user_id not in conversations:
        conversations[data.user_id] = []
    
    response = get_demo_response(data.message)
    
    conversations[data.user_id].append({
        "user": data.message,
        "bot": response,
        "timestamp": datetime.now().isoformat()
    })
    
    # Keep only last 5 exchanges
    if len(conversations[data.user_id]) > 5:
        conversations[data.user_id] = conversations[data.user_id][-5:]
    
    return {
        "response": response,
        "context_length": len(conversations[data.user_id]),
        "demo_mode": True
    }

@app.post("/register")
async def register(data: RegistrationData):
    """Demo registration endpoint"""
    return {
        "success": True,
        "message": f"""🎉 Demo Registration Successful!

**Registration Details:**
✅ **Name:** {data.name}
✅ **Email:** {data.email}
✅ **Phone:** {data.phone}
✅ **Course:** {COURSE_INFO['name']}

Note: This is demo mode - registration data is not actually saved.
In the full version, data would be saved to Google Sheets automatically!

Welcome to the Python development community! 🐍✨""",
        "registration_id": f"DEMO_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "demo_mode": True
    }

@app.get("/")
async def root():
    return {
        "message": "Demo Course Chatbot API",
        "mode": "demo",
        "note": "This is a demo version with pre-programmed responses",
        "endpoints": ["/start", "/chat", "/register", "/docs"]
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Demo Chatbot...")
    print("Visit http://localhost:8001/docs for API documentation")
    print("Press Ctrl+C to stop the server")
    uvicorn.run("demo_chatbot:app", host="0.0.0.0", port=8001, reload=True)

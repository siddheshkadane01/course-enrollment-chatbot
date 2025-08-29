"""
AI Chatbot for Course Information and Registration
=================================================

This FastAPI application creates a chatbot that:
1. Provides course information using OpenAI GPT
2. Handles course FAQs
3. Processes student registration
4. Saves registration data to Google Sheets

Configuration:
- Update COURSE_INFO dictionary to modify course details
- Update FAQ_RESPONSES dictionary to modify FAQ answers
- Set your OpenAI API key in the environment or update OPENAI_API_KEY
- Set up Google Sheets API credentials (see setup instructions)
"""

import os
import json
from typing import List, Dict, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import openai
import gspread
from google.oauth2.service_account import Credentials

# ===== CONFIGURATION SECTION =====
# Edit these dictionaries to customize your course information

COURSE_INFO = {
    "name": "Complete Python Development Bootcamp",
    "duration": "12 weeks (3 months)",
    "price": "$299",
    "instructor": "John Smith",
    "format": "Online with live sessions",
    "schedule": "Monday, Wednesday, Friday - 7:00 PM to 9:00 PM EST",
    "description": "A comprehensive Python development course covering web development, data science, and automation",
    "benefits": [
        "Learn Python from beginner to advanced level",
        "Build real-world projects including web applications",
        "Get hands-on experience with popular Python frameworks",
        "Receive a certificate of completion",
        "Access to lifetime course materials",
        "1-on-1 mentorship sessions",
        "Job placement assistance"
    ],
    "prerequisites": "No prior programming experience required",
    "support": "24/7 support via email and Discord community"
}

FAQ_RESPONSES = {
    "duration": f"The course duration is {COURSE_INFO['duration']}.",
    "price": f"The course price is {COURSE_INFO['price']}. We also offer payment plans if needed.",
    "benefits": f"Course benefits include: {', '.join(COURSE_INFO['benefits'])}",
    "schedule": f"Classes are held {COURSE_INFO['schedule']}.",
    "prerequisites": f"Prerequisites: {COURSE_INFO['prerequisites']}",
    "instructor": f"Your instructor will be {COURSE_INFO['instructor']}, an experienced Python developer.",
    "format": f"The course format is {COURSE_INFO['format']}.",
    "support": f"We provide {COURSE_INFO['support']}.",
    "registration": "To register, please use the /register endpoint and provide your name, email, and phone number.",
    "certificate": "Yes, you will receive a certificate of completion after successfully finishing the course."
}

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "Course Registrations")

# ===== END CONFIGURATION SECTION =====

app = FastAPI(
    title="Course Chatbot API",
    description="AI-powered chatbot for course information and registration",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
try:
    from openai import OpenAI
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    print(f"OpenAI client initialization error: {e}")
    openai_client = None

# In-memory storage for conversation context (in production, use Redis or database)
conversation_contexts: Dict[str, List[Dict]] = {}

# Pydantic models
class ChatMessage(BaseModel):
    user_id: str
    message: str

class RegistrationData(BaseModel):
    name: str
    email: EmailStr
    phone: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    context_length: int
    timestamp: str

# ===== GOOGLE SHEETS INTEGRATION =====

def setup_google_sheets():
    """
    Setup Google Sheets integration.
    Make sure you have:
    1. Created a Google Cloud Project
    2. Enabled Google Sheets API
    3. Created a service account and downloaded credentials.json
    4. Shared your Google Sheet with the service account email
    """
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_PATH, scopes=scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"Google Sheets setup error: {e}")
        return None

def save_to_google_sheets(registration_data: RegistrationData):
    """Save registration data to Google Sheets"""
    try:
        client = setup_google_sheets()
        if not client:
            return False
            
        # Open the spreadsheet
        sheet = client.open(GOOGLE_SHEET_NAME).sheet1
        
        # Check if headers exist, if not add them
        if not sheet.get_all_records():
            headers = ["Timestamp", "Name", "Email", "Phone", "User ID", "Course"]
            sheet.insert_row(headers, 1)
        
        # Add the registration data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row_data = [
            timestamp,
            registration_data.name,
            registration_data.email,
            registration_data.phone,
            registration_data.user_id or "N/A",
            COURSE_INFO["name"]
        ]
        
        sheet.append_row(row_data)
        return True
    except Exception as e:
        print(f"Error saving to Google Sheets: {e}")
        return False

# ===== CONVERSATION CONTEXT MANAGEMENT =====

def get_conversation_context(user_id: str) -> List[Dict]:
    """Get the last 5 messages for a user"""
    return conversation_contexts.get(user_id, [])

def update_conversation_context(user_id: str, user_message: str, bot_response: str):
    """Update conversation context, keeping only last 5 exchanges"""
    if user_id not in conversation_contexts:
        conversation_contexts[user_id] = []
    
    conversation_contexts[user_id].append({
        "user": user_message,
        "assistant": bot_response,
        "timestamp": datetime.now().isoformat()
    })
    
    # Keep only last 5 exchanges (10 messages total)
    if len(conversation_contexts[user_id]) > 5:
        conversation_contexts[user_id] = conversation_contexts[user_id][-5:]

# ===== AI CHATBOT LOGIC =====

def get_system_prompt() -> str:
    """Generate the system prompt with course information"""
    benefits_text = "\n".join([f"- {benefit}" for benefit in COURSE_INFO["benefits"]])
    
    return f"""
You are a helpful AI assistant for the "{COURSE_INFO['name']}" course. 

COURSE DETAILS:
- Course Name: {COURSE_INFO['name']}
- Duration: {COURSE_INFO['duration']}
- Price: {COURSE_INFO['price']}
- Instructor: {COURSE_INFO['instructor']}
- Format: {COURSE_INFO['format']}
- Schedule: {COURSE_INFO['schedule']}
- Prerequisites: {COURSE_INFO['prerequisites']}
- Support: {COURSE_INFO['support']}

COURSE BENEFITS:
{benefits_text}

COURSE DESCRIPTION:
{COURSE_INFO['description']}

Your role is to:
1. Greet users warmly and introduce the course
2. Answer questions about the course details, pricing, schedule, benefits, etc.
3. Help users with the registration process
4. Be friendly, informative, and encouraging
5. If asked about registration, guide them to provide their name, email, and phone number

Keep responses conversational and helpful. If you don't know something specific about the course, refer them to contact support.
"""

def generate_ai_response(user_message: str, context: List[Dict]) -> str:
    """Generate AI response using OpenAI GPT"""
    try:
        # Check if it's a greeting or first message
        if not context and any(greeting in user_message.lower() for greeting in ["hello", "hi", "hey", "start", "help"]):
            return f"""Hello! 👋 Welcome to our {COURSE_INFO['name']} information assistant!

I'm here to help you learn about our comprehensive Python development course. Here's what I can help you with:

📚 **Course Overview:** {COURSE_INFO['description']}
⏰ **Duration:** {COURSE_INFO['duration']}
💰 **Price:** {COURSE_INFO['price']}
📅 **Schedule:** {COURSE_INFO['schedule']}

Feel free to ask me about:
- Course details and curriculum
- Pricing and payment options
- Schedule and format
- Benefits and what you'll learn
- How to register
- Any other questions!

What would you like to know about the course?"""

        # Check for FAQ keywords
        user_lower = user_message.lower()
        for keyword, response in FAQ_RESPONSES.items():
            if keyword in user_lower:
                return response

        # Build conversation history for context
        messages = [{"role": "system", "content": get_system_prompt()}]
        
        # Add conversation context
        for exchange in context:
            messages.append({"role": "user", "content": exchange["user"]})
            messages.append({"role": "assistant", "content": exchange["assistant"]})
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        # Generate response using OpenAI
        if not openai_client:
            return "I'm sorry, the AI service is not available right now. Please try again later or contact support."
            
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
        except Exception as e:
            print(f"OpenAI API call error: {e}")
            return "I'm sorry, I'm having trouble processing your request right now. Please try again or contact our support team for assistance."
        
        content = response.choices[0].message.content
        return content.strip() if content else "I'm sorry, I couldn't generate a response."
    
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "I'm sorry, I'm having trouble processing your request right now. Please try again or contact our support team for assistance."

# ===== API ENDPOINTS =====

@app.get("/")
async def root():
    """Serve the frontend application"""
    return FileResponse('static/index.html')

@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "message": f"Welcome to {COURSE_INFO['name']} Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "/start": "Start a conversation with the chatbot",
            "/chat": "Send a message to the chatbot",
            "/register": "Register for the course",
            "/course-info": "Get course information"
        }
    }

@app.post("/start")
async def start_conversation(user_data: ChatMessage):
    """
    Start a new conversation - Telegram bot style endpoint
    This simulates the /start command in Telegram bots
    """
    try:
        # Clear any existing context for this user
        if user_data.user_id in conversation_contexts:
            del conversation_contexts[user_data.user_id]
        
        # Generate welcome response
        welcome_message = f"""🎉 Welcome to {COURSE_INFO['name']}!

I'm your personal course assistant, here to help you learn everything about our Python development program.

**Quick Course Overview:**
📚 **Course:** {COURSE_INFO['name']}
⏰ **Duration:** {COURSE_INFO['duration']}
💰 **Investment:** {COURSE_INFO['price']}
👨‍💻 **Instructor:** {COURSE_INFO['instructor']}
📱 **Format:** {COURSE_INFO['format']}

**What you'll get:**
{chr(10).join([f'✅ {benefit}' for benefit in COURSE_INFO['benefits'][:5]])}

Type 'info' for detailed course information, 'faq' for common questions, or 'register' to secure your spot!

What would you like to know? 🤔"""

        # Update conversation context
        update_conversation_context(user_data.user_id, "/start", welcome_message)
        
        return ChatResponse(
            response=welcome_message,
            context_length=len(get_conversation_context(user_data.user_id)),
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting conversation: {str(e)}")

@app.post("/chat")
async def chat_with_bot(chat_data: ChatMessage):
    """Send a message to the chatbot and get a response"""
    try:
        # Get conversation context
        context = get_conversation_context(chat_data.user_id)
        
        # Generate AI response
        bot_response = generate_ai_response(chat_data.message, context)
        
        # Update conversation context
        update_conversation_context(chat_data.user_id, chat_data.message, bot_response)
        
        return ChatResponse(
            response=bot_response,
            context_length=len(get_conversation_context(chat_data.user_id)),
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.post("/register")
async def register_for_course(registration: RegistrationData):
    """Handle course registration and save to Google Sheets"""
    try:
        # Save to Google Sheets
        sheets_success = save_to_google_sheets(registration)
        
        # Generate confirmation message
        confirmation_message = f"""🎉 Thank you for registering, {registration.name}!

**Registration Details:**
✅ **Name:** {registration.name}
✅ **Email:** {registration.email}
✅ **Phone:** {registration.phone}
✅ **Course:** {COURSE_INFO['name']}

{'✅ **Saved to our system successfully!**' if sheets_success else '⚠️ **Registration received but there was an issue with our system. We will contact you shortly.**'}

**What's Next:**
1. You'll receive a confirmation email within 24 hours
2. Course materials will be sent 1 week before start date
3. You'll get access to our Discord community
4. Payment instructions will be included in the confirmation email

**Course starts:** Contact us for the next batch schedule
**Need help?** Reply here or email support@ourcompany.com

Welcome to the {COURSE_INFO['name']} family! 🐍✨"""

        # Update conversation context if user_id is provided
        if registration.user_id:
            update_conversation_context(
                registration.user_id, 
                f"Registration: {registration.name}, {registration.email}, {registration.phone}", 
                confirmation_message
            )
        
        return {
            "success": True,
            "message": confirmation_message,
            "registration_id": f"REG_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{registration.name[:3].upper()}",
            "sheets_saved": sheets_success
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing registration: {str(e)}")

@app.get("/course-info")
async def get_course_info():
    """Get complete course information"""
    return {
        "course_details": COURSE_INFO,
        "faqs": FAQ_RESPONSES,
        "registration_info": {
            "process": "Use the /register endpoint with name, email, and phone",
            "requirements": ["Valid email address", "Phone number", "Full name"]
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "openai_configured": bool(OPENAI_API_KEY and OPENAI_API_KEY != "your-openai-api-key-here"),
        "google_sheets_configured": os.path.exists(GOOGLE_CREDENTIALS_PATH)
    }

# ===== ERROR HANDLERS =====

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "Endpoint not found. Use /docs to see available endpoints."}
    )

@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error. Please try again later."}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

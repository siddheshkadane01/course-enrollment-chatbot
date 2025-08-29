"""
Test Script for Course Chatbot
==============================

This script demonstrates how to interact with the chatbot API.
Run this after starting the FastAPI server.
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

def test_chatbot_flow():
    """Test the complete chatbot flow"""
    
    print("🤖 Testing Course Chatbot API")
    print("=" * 50)
    
    # Test user ID
    user_id = f"test_user_{datetime.now().strftime('%H%M%S')}"
    
    # Test 1: Start conversation
    print("\n1️⃣ Testing /start endpoint...")
    start_response = requests.post(f"{BASE_URL}/start", json={
        "user_id": user_id,
        "message": "start"
    })
    
    if start_response.status_code == 200:
        data = start_response.json()
        print("✅ Start conversation successful!")
        print(f"Response: {data['response'][:100]}...")
        print(f"Context length: {data['context_length']}")
    else:
        print(f"❌ Start failed: {start_response.status_code}")
        return
    
    # Test 2: Ask about course duration
    print("\n2️⃣ Testing course duration query...")
    chat_response = requests.post(f"{BASE_URL}/chat", json={
        "user_id": user_id,
        "message": "What is the course duration?"
    })
    
    if chat_response.status_code == 200:
        data = chat_response.json()
        print("✅ Duration query successful!")
        print(f"Response: {data['response']}")
    else:
        print(f"❌ Duration query failed: {chat_response.status_code}")
    
    # Test 3: Ask about pricing
    print("\n3️⃣ Testing pricing query...")
    chat_response = requests.post(f"{BASE_URL}/chat", json={
        "user_id": user_id,
        "message": "How much does the course cost?"
    })
    
    if chat_response.status_code == 200:
        data = chat_response.json()
        print("✅ Pricing query successful!")
        print(f"Response: {data['response']}")
    else:
        print(f"❌ Pricing query failed: {chat_response.status_code}")
    
    # Test 4: Registration
    print("\n4️⃣ Testing registration...")
    registration_response = requests.post(f"{BASE_URL}/register", json={
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1-555-0123",
        "user_id": user_id
    })
    
    if registration_response.status_code == 200:
        data = registration_response.json()
        print("✅ Registration successful!")
        print(f"Success: {data['success']}")
        print(f"Registration ID: {data['registration_id']}")
    else:
        print(f"❌ Registration failed: {registration_response.status_code}")
    
    # Test 5: Get course info
    print("\n5️⃣ Testing course info endpoint...")
    info_response = requests.get(f"{BASE_URL}/course-info")
    
    if info_response.status_code == 200:
        data = info_response.json()
        print("✅ Course info retrieved!")
        print(f"Course name: {data['course_details']['name']}")
        print(f"Available FAQs: {len(data['faqs'])} items")
    else:
        print(f"❌ Course info failed: {info_response.status_code}")
    
    # Test 6: Health check
    print("\n6️⃣ Testing health check...")
    health_response = requests.get(f"{BASE_URL}/health")
    
    if health_response.status_code == 200:
        data = health_response.json()
        print("✅ Health check successful!")
        print(f"Status: {data['status']}")
        print(f"OpenAI configured: {data['openai_configured']}")
        print(f"Google Sheets configured: {data['google_sheets_configured']}")
    else:
        print(f"❌ Health check failed: {health_response.status_code}")
    
    print("\n🎉 Testing complete!")
    print(f"Visit {BASE_URL}/docs for interactive API documentation")

def interactive_chat():
    """Interactive chat session with the bot"""
    user_id = f"interactive_user_{datetime.now().strftime('%H%M%S')}"
    
    print("🤖 Interactive Chat Session")
    print("=" * 50)
    print("Type 'quit' to exit, 'register' to test registration")
    
    # Start the conversation
    start_response = requests.post(f"{BASE_URL}/start", json={
        "user_id": user_id,
        "message": "start"
    })
    
    if start_response.status_code == 200:
        print(f"\n🤖 Bot: {start_response.json()['response']}")
    else:
        print("❌ Failed to start conversation")
        return
    
    while True:
        user_input = input("\n👤 You: ").strip()
        
        if user_input.lower() == 'quit':
            print("👋 Goodbye!")
            break
        
        if user_input.lower() == 'register':
            # Test registration flow
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            phone = input("Enter your phone: ")
            
            reg_response = requests.post(f"{BASE_URL}/register", json={
                "name": name,
                "email": email,
                "phone": phone,
                "user_id": user_id
            })
            
            if reg_response.status_code == 200:
                print(f"\n🤖 Bot: {reg_response.json()['message']}")
            else:
                print(f"❌ Registration failed: {reg_response.status_code}")
            continue
        
        # Send message to chatbot
        chat_response = requests.post(f"{BASE_URL}/chat", json={
            "user_id": user_id,
            "message": user_input
        })
        
        if chat_response.status_code == 200:
            data = chat_response.json()
            print(f"\n🤖 Bot: {data['response']}")
            print(f"[Context: {data['context_length']} exchanges]")
        else:
            print(f"❌ Chat failed: {chat_response.status_code}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        try:
            interactive_chat()
        except KeyboardInterrupt:
            print("\n👋 Chat session ended!")
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect to the chatbot server. Make sure it's running on localhost:8000")
    else:
        try:
            test_chatbot_flow()
        except requests.exceptions.ConnectionError:
            print("❌ Could not connect to the chatbot server.")
            print("Please start the server first with: uvicorn main:app --reload")
            print("Then run this test script again.")

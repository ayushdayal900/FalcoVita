"""
Quick test script to verify Google Chat webhook is working
"""
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

webhook_url = os.environ.get('GOOGLE_CHAT_WEBHOOK_URL', '')

if not webhook_url:
    print("❌ ERROR: GOOGLE_CHAT_WEBHOOK_URL not found in .env file")
    print("Please add it to backend/.env")
    exit(1)

print(f"✅ Webhook URL found: {webhook_url[:50]}...")

# Send a simple test message
message = {
    "text": "🧪 Test message from FalcoVita - If you see this, the webhook is working!"
}

try:
    print("\n📤 Sending test message to Google Chat...")
    response = requests.post(
        webhook_url,
        headers={'Content-Type': 'application/json; charset=UTF-8'},
        data=json.dumps(message)
    )
    
    if response.status_code == 200:
        print("✅ SUCCESS! Message sent to Google Chat!")
        print("Check your Google Chat space for the message.")
    else:
        print(f"❌ FAILED! Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ ERROR: {e}")

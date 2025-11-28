"""
Test script to manually trigger daily reminders and see emails in MailHog
"""

from backend.tasks import send_daily_reminders
from backend.app import app

def test_daily_reminders():
    print("Testing daily reminder task...")
    print("Make sure MailHog is running at http://localhost:8025")
    print("-" * 50)
    
    with app.app_context():
        result = send_daily_reminders()
        print(f"Result: {result}")
        print("-" * 50)
        print("Check MailHog at http://localhost:8025 to see the emails!")

if __name__ == "__main__":
    test_daily_reminders()

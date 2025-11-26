import sys
import os
import uuid

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.extensions import db
from backend.models import User

app = create_app()

def reproduce_registration():
    client = app.test_client()
    
    # Generate unique email to avoid conflict
    unique_id = str(uuid.uuid4())[:8]
    email = f"test_patient_{unique_id}@example.com"
    
    payload = {
        "name": f"Test Patient {unique_id}",
        "email": email,
        "password": "password123",
        "contact_number": "1234567890",
        "role": "patient",
        "dob": "1990-01-01",
        "contact": f"123{unique_id[:7]}", # Unique contact
        "doctor_id": 1 # Assuming doctor with ID 1 exists, or it might be nullable/ignored if not strictly enforced
    }
    
    print(f"Attempting to register patient: {email}")
    
    try:
        response = client.post('/api/auth/register', json=payload)
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.get_json()}")
        
        if response.status_code == 201:
            print("Registration successful!")
        else:
            print("Registration failed.")
            
    except Exception as e:
        print(f"Exception during registration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    with app.app_context():
        # Ensure DB tables exist
        db.create_all()
        reproduce_registration()

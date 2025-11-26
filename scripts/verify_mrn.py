import sys
import os
import uuid

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.extensions import db
from backend.models import User, Patient

app = create_app()

def verify_mrn_generation():
    with app.app_context():
        client = app.test_client()
        
        # Unique email and contact
        unique_id = uuid.uuid4().hex[:8]
        email = f"test_patient_{unique_id}@example.com"
        contact = f"1{unique_id[:9]}" # Ensure it fits in 15 chars
        password = "password123"
        
        payload = {
            "role": "patient",
            "name": "Test Patient",
            "email": email,
            "password": password,
            "contact_number": contact,
            "dob": "1990-01-01",
            "contact": contact
        }
        
        # Register
        response = client.post('/api/auth/register', json=payload)
        
        if response.status_code != 201:
            print(f"FAILED: Registration failed with status {response.status_code}")
            print(response.json)
            return

        print("Registration successful.")
        
        # Verify DB
        user = User.query.filter_by(email=email).first()
        if not user:
            print("FAILED: User not found in DB.")
            return
            
        patient = Patient.query.filter_by(id=user.id).first()
        if not patient:
            print("FAILED: Patient record not found.")
            return
            
        print(f"Patient MRN: {patient.medical_record_number}")
        
        if patient.medical_record_number and patient.medical_record_number.startswith("MRN-"):
            print("SUCCESS: MRN generated correctly.")
        else:
            print(f"FAILED: Invalid MRN format: {patient.medical_record_number}")

if __name__ == "__main__":
    verify_mrn_generation()

import requests
import sys

BASE_URL = "http://localhost:5000/api"

def test_blocked_doctor_visibility():
    # 1. Login as admin to get token (if needed, but for now assuming no auth for reproduction or using basic auth if setup)
    # Actually, the app seems to use Flask-Security-Too. I might need to login.
    # But for quick test, I'll try to hit the endpoint directly if it's open or mock the service call.
    
    # Better: Use the app context directly like in other debug scripts.
    from backend.app import app
    from backend.models import User, Doctor, db
    from backend.services.doctors_services import DoctorService

    with app.app_context():
        # Find a doctor
        doctor_user = User.query.filter_by(role='doctor').first()
        if not doctor_user:
            print("No doctors found.")
            return

        print(f"Testing with Doctor: {doctor_user.name} (ID: {doctor_user.id})")
        
        # Ensure not blocked initially
        doctor_user.blacklisted = False
        db.session.commit()
        
        # 1. Fetch all (default) -> Should include him
        doctors = DoctorService.get_all(include_blocked=False)
        found = any(d['user']['id'] == doctor_user.id for d in doctors)
        print(f"Initial fetch (include_blocked=False): Found = {found}")

        # 2. Block him
        doctor_user.blacklisted = True
        db.session.commit()
        print("Doctor blocked.")

        # 3. Fetch all (include_blocked=False) -> Should NOT include him
        doctors = DoctorService.get_all(include_blocked=False)
        found = any(d['user']['id'] == doctor_user.id for d in doctors)
        print(f"Fetch blocked (include_blocked=False): Found = {found} (Expected: False)")

        # 4. Fetch all (include_blocked=True) -> Should include him
        doctors = DoctorService.get_all(include_blocked=True)
        found = any(d['user']['id'] == doctor_user.id for d in doctors)
        print(f"Fetch blocked (include_blocked=True): Found = {found} (Expected: True)")

        # Reset
        doctor_user.blacklisted = False
        db.session.commit()
        print("Doctor unblocked (reset).")

if __name__ == "__main__":
    test_blocked_doctor_visibility()

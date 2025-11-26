from backend.app import create_app
from backend.extensions import db
from backend.models import User, Doctor, Department
from backend.services.doctors_services import DoctorService
import uuid

app = create_app()

with app.app_context():
    print("Creating test data...")
    
    # Ensure a department exists
    dept = Department.query.first()
    if not dept:
        dept = Department(name="Test Dept", overview="Test Overview")
        db.session.add(dept)
        db.session.commit()
    
    # Create a dummy doctor
    unique_id = str(uuid.uuid4())[:8]
    email = f"test_doctor_{unique_id}@example.com"
    
    data = {
        "name": "Test Doctor",
        "email": email,
        "password": "password123",
        "department_id": dept.id,
        "specialization": "Testing",
        "qualifications": "MBBS",
        "experience": 5
    }
    
    try:
        new_doctor = DoctorService.create(data)
        doctor_id = new_doctor.id
        print(f"Created doctor with ID: {doctor_id}")
        
        # Verify creation
        user = User.query.get(doctor_id)
        doctor = Doctor.query.get(doctor_id)
        assert user is not None
        assert doctor is not None
        
        print("Attempting to delete doctor...")
        DoctorService.delete_by_id(doctor_id)
        
        # Verify deletion
        user = User.query.get(doctor_id)
        doctor = Doctor.query.get(doctor_id)
        
        if user is None and doctor is None:
            print("SUCCESS: Doctor and User records deleted successfully.")
        else:
            print("FAILURE: Records still exist.")
            if user: print("User record found.")
            if doctor: print("Doctor record found.")
            
    except Exception as e:
        print(f"ERROR: {e}")

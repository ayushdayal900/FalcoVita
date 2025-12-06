from backend.app import app
from backend.extensions import db
from backend.models import User
from flask_security.utils import hash_password

def reset_passwords():
    with app.app_context():
        print("Resetting all passwords...")
        users = User.query.all()
        count = 0
        for user in users:
            if user.role == 'admin':
                new_pass = "Admin@123"
            elif user.role == 'doctor':
                new_pass = "Doctor@123"
            elif user.role == 'patient':
                new_pass = "Patient@123"
            else:
                new_pass = "User@123"
            
            user.password = hash_password(new_pass)
            count += 1
            if count % 10 == 0:
                print(f"Processed {count} users...")
        
        db.session.commit()
        print(f"Successfully reset passwords for {count} users.")
        print("\n=== New Credentials ===")
        print("Admin:   admin@iitm.ac.in / Admin@123")
        print("Doctor:  doctor1@hospital.com / Doctor@123")
        print("Patient: patient1@example.com / Patient@123")

if __name__ == "__main__":
    reset_passwords()

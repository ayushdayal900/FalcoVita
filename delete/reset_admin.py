from backend.app import app
from backend.extensions import db, user_datastore
from flask_security.utils import hash_password

def reset_admin():
    with app.app_context():
        email = "admin@iitm.ac.in"
        new_password = "Admin@123"
        
        print(f"Resetting password for: {email}")
        user = user_datastore.find_user(email=email)
        
        if user:
            user.password = hash_password(new_password)
            db.session.commit()
            print("Password reset successfully.")
            print(f"New Hash: {user.password}")
        else:
            print("User NOT found")

if __name__ == "__main__":
    reset_admin()

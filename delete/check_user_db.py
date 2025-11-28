from backend.app import app
from backend.extensions import user_datastore
from flask_security.utils import verify_password

def check_user():
    with app.app_context():
        email = "doctor1@hospital.com"
        user = user_datastore.find_user(email=email)
        if user:
            print(f"User found: {user.email}")
            print(f"Role: {user.roles[0].name if user.roles else 'No Role'}")
            print(f"Password Hash: {user.password}")
            
            is_valid = verify_password("Doctor@123", user.password)
            print(f"Password 'Doctor@123' valid? {is_valid}")
            
            print(f"Config SECURITY_PASSWORD_HASH: {app.config.get('SECURITY_PASSWORD_HASH')}")
            print(f"Config SECURITY_PASSWORD_SALT: {app.config.get('SECURITY_PASSWORD_SALT')}")
        else:
            print("User not found")

if __name__ == "__main__":
    check_user()

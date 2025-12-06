from backend.app import app
from backend.extensions import db, user_datastore
from flask_security.utils import hash_password

with app.app_context():
    print("Resetting admin password...")
    user = user_datastore.find_user(email="admin@iitm.ac.in")
    if user:
        print(f"Found user: {user.email}")
        # Hash the password using the CURRENT app configuration (including the new salt)
        user.password = hash_password("Admin@123")
        db.session.commit()
        print("Password reset successfully to 'Admin@123'")
    else:
        print("User not found!")

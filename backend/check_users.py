from backend.app import app
from backend.models import User
from backend.extensions import db

with app.app_context():
    users = User.query.all()
    print(f"Total Users: {len(users)}")
    for u in users:
        print(f"ID: {u.id} | Name: {u.name} | Email: {u.email} | Role: {u.role} | Active: {u.active}")

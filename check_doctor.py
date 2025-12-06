from backend.app import app
from backend.models import User

with app.app_context():
    users = User.query.filter(User.name.like('%Scott%')).all()
    print("Found users:", [u.name for u in users])

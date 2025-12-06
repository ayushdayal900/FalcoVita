from backend.app import app
from backend.extensions import db
from backend.models import User, Billing, Payment, Inventory, ChatMessage

def create_tables():
    with app.app_context():
        print("Creating new database tables...")
        # db.create_all() only creates tables that don't exist
        db.create_all()
        print("Successfully created tables: Billing, Payment, Inventory, ChatMessage")

if __name__ == "__main__":
    create_tables()

"""
Database migration to add availability_slot_id to appointments table

This migration adds a foreign key column to link appointments with availability slots.
Run this after updating the models.
"""

from backend.app import app
from backend.extensions import db

def migrate():
    """Add availability_slot_id column to appointment table"""
    with app.app_context():
        # Check if column already exists
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('appointment')]
        
        if 'availability_slot_id' in columns:
            print("Column 'availability_slot_id' already exists. Skipping migration.")
            return
        
        print("Adding availability_slot_id column to appointment table...")
        
        # Add the column using raw SQL
        with db.engine.connect() as conn:
            # Add column as nullable
            conn.execute(db.text("""
                ALTER TABLE appointment 
                ADD COLUMN availability_slot_id INTEGER
            """))
            
            # Add foreign key constraint
            conn.execute(db.text("""
                ALTER TABLE appointment 
                ADD CONSTRAINT fk_appointment_availability_slot 
                FOREIGN KEY (availability_slot_id) 
                REFERENCES availability_slot(id)
            """))
            
            conn.commit()
        
        print("Migration completed successfully!")
        print("Note: Existing appointments will have NULL availability_slot_id")

def rollback():
    """Remove availability_slot_id column from appointment table"""
    with app.app_context():
        print("Rolling back migration...")
        
        with db.engine.connect() as conn:
            # Drop foreign key constraint first
            conn.execute(db.text("""
                ALTER TABLE appointment 
                DROP CONSTRAINT IF EXISTS fk_appointment_availability_slot
            """))
            
            # Drop the column
            conn.execute(db.text("""
                ALTER TABLE appointment 
                DROP COLUMN IF EXISTS availability_slot_id
            """))
            
            conn.commit()
        
        print("Rollback completed successfully!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        rollback()
    else:
        migrate()

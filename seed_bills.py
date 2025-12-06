from backend.app import app
from backend.models import User, Patient, Billing, db
from datetime import datetime, timedelta

with app.app_context():
    # Find a patient
    patient_user = User.query.join(Patient).first()
    if patient_user and patient_user.patient:
        pid = patient_user.patient.id
        print(f"Seeding bills for patient {patient_user.name}")
        
        # Pending Bill
        b1 = Billing(
            patient_id=pid,
            total_amount=150.00,
            status='pending',
            due_date=datetime.now() + timedelta(days=7)
        )
        
        # Paid Bill
        b2 = Billing(
            patient_id=pid,
            total_amount=500.00,
            status='paid',
            due_date=datetime.now() - timedelta(days=30)
        )
        
        db.session.add(b1)
        db.session.add(b2)
        db.session.commit()
        print("Seeded bills.")
    else:
        print("No patient found to seed bills.")

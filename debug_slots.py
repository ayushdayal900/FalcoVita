from backend.app import app
from backend.models import User, Doctor, AvailabilitySlot

with app.app_context():
    # Find Glenn Pierce
    users = User.query.filter(User.name.like('%Glenn Pierce%')).all()
    if not users:
        print("Doctor 'Glenn Pierce' not found in User table.")
    else:
        for u in users:
            print(f"Found User: {u.name} (ID: {u.id})")
            doctor = Doctor.query.get(u.id)
            if doctor:
                print(f"  Is Doctor. Checking slots...")
                slots = AvailabilitySlot.query.filter_by(doctor_id=doctor.id).all()
                if slots:
                    for s in slots:
                        print(f"    Slot: {s.available_date} - {s.time_slot} ({s.status})")
                else:
                    print("    No slots found in AvailabilitySlot table.")
            else:
                print("    Not a doctor.")

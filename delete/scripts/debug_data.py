from backend.app import app
from backend.models import User, Patient, Doctor, Department, Appointment

def debug_data():
    with app.app_context():
        users = User.query.filter(User.name.like('%Leonard%')).all()
        for u in users:
            print(f"User: {u.id}, {u.name}, {u.email}, Role: {u.role}")
            if u.role == 'patient':
                p = Patient.query.filter_by(id=u.id).first()
                print(f"  -> Patient Record: {'FOUND' if p else 'MISSING'}")
            elif u.role == 'doctor':
                d = Doctor.query.filter_by(id=u.id).first()
                print(f"  -> Doctor Record: {'FOUND' if d else 'MISSING'}")

        print("\n--- Departments ---")
        depts = Department.query.all()
        for d in depts:
            print(f"Dept: {d.id}, {d.name}")

if __name__ == "__main__":
    debug_data()

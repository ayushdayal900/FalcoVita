import uuid
import random
from datetime import datetime, timedelta, timezone

from faker import Faker
from backend.password_utils import hash_password
from backend.extensions import db
from backend.models import (
    User,
    Doctor, Patient, Department,
    Appointment, PatientHistory, Prescription, AvailabilitySlot
)
from backend.app import app  


fake = Faker()

def seed_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        print("Creating admin user...")
        # Create Admin user
        admin_user = User(
            name="Admin User",
            email="admin@iitm.ac.in",
            password=hash_password("Admin@123"),
            role="admin",
            active=True,
            blacklisted=False
        )
        db.session.add(admin_user)
        db.session.commit()

        print("Creating departments...")
        departments = []
        dept_names = ["Cardiology", "Neurology", "Orthopedics", "Dermatology", "Pediatrics"]
        for name in dept_names:
            dept = Department(name=name, overview=fake.text(50))
            departments.append(dept)
        db.session.add_all(departments)
        db.session.commit()

        print("Creating doctors...")
        doctors = []
        for i in range(10):
            user = User(
                name=fake.name(),
                email=f"doctor{i+1}@hospital.com",
                password=hash_password("Doctor@123"),
                role="doctor",
                contact_number=fake.phone_number()[:15],
                active=True,
                blacklisted=False
            )
            db.session.add(user)
            db.session.flush()

            doctor = Doctor(
                id=user.id,
                department_id=random.choice(departments).id,
                specialization=random.choice(["Cardiology", "Neurology", "Surgery", "Pediatrics"]),
                qualifications=fake.sentence(nb_words=3),
                experience=random.randint(2, 20),
            )
            doctors.append(doctor)

        db.session.add_all(doctors)
        db.session.commit()

        print("Creating patients...")
        patients = []
        for i in range(50):
            user = User(
                name=fake.name(),
                email=f"patient{i+1}@example.com",
                password=hash_password("Patient@123"),
                role="patient",
                contact_number=fake.phone_number()[:15],
                active=True,
                blacklisted=False
            )
            db.session.add(user)
            db.session.flush()

            patient = Patient(
                id=user.id,
                dob=fake.date_time_between(start_date="-70y", end_date="-18y", tzinfo=timezone.utc),
                contact=fake.phone_number()[:15],
                medical_record_number=f"MRN-{fake.unique.random_int(10000,99999)}",
                doctor_id=random.choice(doctors).id
            )
            patients.append(patient)

        db.session.add_all(patients)
        db.session.commit()

        print("Creating appointments, histories, and prescriptions...")
        statuses = ["scheduled", "completed", "cancelled"]
        for patient in patients:
            for _ in range(random.randint(1, 3)):
                doctor = random.choice(doctors)
                department = doctor.department

                appointment_date = fake.date_time_between(start_date="-90d", end_date="+10d", tzinfo=timezone.utc)

                appointment = Appointment(
                    patient_id=patient.id,
                    doctor_id=doctor.id,
                    department_id=department.id,
                    appointment_date=appointment_date,
                    status=random.choice(statuses),
                )
                db.session.add(appointment)
                db.session.flush()

                history = PatientHistory(
                    patient_id=patient.id,
                    doctor_id=doctor.id,
                    department_id=department.id,
                    appointment_id=appointment.id,
                    visit_type=random.choice(["Consultation", "Follow-up"]),
                    visit_date=appointment_date,
                    diagnosis=fake.sentence(nb_words=6)
                )
                db.session.add(history)
                db.session.flush()

                prescription = Prescription(
                    history_id=history.id,
                    medicines=f"{fake.word()} {random.randint(100,500)}mg",
                    dosage=f"{random.randint(1,3)} times/day",
                    instructions=fake.sentence()
                )
                db.session.add(prescription)

        db.session.commit()

        print("Creating availability slots for doctors...")
        for doctor in doctors:
            for day_offset in range(-5, 6):
                slot_date = datetime.now(timezone.utc) + timedelta(days=day_offset)
                slot = AvailabilitySlot(
                    doctor_id=doctor.id,
                    available_date=slot_date,
                    time_slot=f"{random.randint(8,17)}:00-{random.randint(18,20)}:00",
                    status=random.choice(["available", "booked"])
                )
                db.session.add(slot)

        db.session.commit()

        print("Database seeded successfully!")
        print("\n=== Login Credentials ===")
        print("Admin: admin@iitm.ac.in / Admin@123")
        print("Doctor: doctor1@hospital.com / Doctor@123")
        print("Patient: patient1@example.com / Patient@123")


if __name__ == "__main__":
    seed_data()
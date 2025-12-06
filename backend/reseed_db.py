import uuid
import random
from datetime import datetime, timedelta, timezone

from faker import Faker
from flask_security.utils import hash_password
from backend import extensions
from backend.extensions import db
from backend.models import (
    User, Role, UserRoles,
    Doctor, Patient, Department,
    Appointment, PatientHistory, Prescription, AvailabilitySlot,
    Billing, Payment
)
from backend.app import app  
from flask_security.datastore import SQLAlchemyUserDatastore


fake = Faker()

def seed_data():
    with app.app_context():
        datastore: SQLAlchemyUserDatastore = extensions.user_datastore

        db.drop_all()
        db.create_all()

        print("Creating roles...")
        # Create roles
        admin_role = Role(name="admin", description="Administrator")
        doctor_role = Role(name="doctor", description="Medical Doctor")
        patient_role = Role(name="patient", description="Registered Patient")

        db.session.add_all([admin_role, doctor_role, patient_role])
        db.session.commit()

        print("Creating admin user...")
        # Create Admin user
        admin_user = User(
            name="Admin User",
            email="admin@iitm.ac.in",
            password=hash_password("Admin@123"),
            role="admin",
            fs_uniquifier=str(uuid.uuid4())
        )
        db.session.add(admin_user)
        db.session.commit()

        admin_user_role = UserRoles(user_id=admin_user.id, role_id=admin_role.id)
        db.session.add(admin_user_role)
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
                fs_uniquifier=str(uuid.uuid4()),
                contact_number=fake.phone_number()[:15],
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
            db.session.add(UserRoles(user_id=user.id, role_id=doctor_role.id))

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
                fs_uniquifier=str(uuid.uuid4()),
                contact_number=fake.phone_number()[:15],
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
            db.session.add(UserRoles(user_id=user.id, role_id=patient_role.id))

        db.session.add_all(patients)
        db.session.commit()

        print("Creating appointments, histories, prescriptions, bills, and payments...")
        statuses = ["scheduled", "completed", "cancelled"]
        
        for patient in patients:
            for _ in range(random.randint(1, 3)):
                doctor = random.choice(doctors)
                department = doctor.department

                appointment_date = fake.date_time_between(start_date="-90d", end_date="+10d", tzinfo=timezone.utc)
                status = random.choice(statuses)

                appointment = Appointment(
                    patient_id=patient.id,
                    doctor_id=doctor.id,
                    department_id=department.id,
                    appointment_date=appointment_date,
                    status=status,
                )
                db.session.add(appointment)
                db.session.flush()

                # History & Prescription (Only for completed or some scheduled)
                if status == "completed":
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

                # Billing & Payments (For most appointments)
                if status != "cancelled":
                    amount = 100.0 # Fixed amount as per requirement
                    bill_status = 'paid' if status == 'completed' or random.choice([True, False]) else 'pending'
                    
                    billing = Billing(
                        patient_id=patient.id,
                        appointment_id=appointment.id,
                        total_amount=amount,
                        status=bill_status,
                        due_date=appointment_date
                    )
                    db.session.add(billing)
                    db.session.flush()

                    if bill_status == 'paid':
                        payment = Payment(
                            billing_id=billing.id,
                            amount_paid=amount,
                            payment_date=appointment_date,
                            payment_method=random.choice(["Card", "Cash", "UPI"]),
                            transaction_id=f"TXN-{fake.uuid4()[:8]}"
                        )
                        db.session.add(payment)

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

        print("Database reseeded successfully!")
        print("\n=== Login Credentials ===")
        print("Admin: admin@iitm.ac.in / Admin@123")
        print("Doctor: doctor1@hospital.com / Doctor@123")
        print("Patient: patient1@example.com / Patient@123")


if __name__ == "__main__":
    seed_data()

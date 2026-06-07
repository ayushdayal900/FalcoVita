import os
import sys
import base64
from sqlalchemy import text

# Ensure backend directory is in the path
basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if basedir not in sys.path:
    sys.path.insert(0, basedir)

from backend.app import app
from backend.extensions import db
from backend.models import PatientHistory, Prescription, Patient, Doctor, Department, Appointment

def run_tests():
    print("Initializing Flask App Context...")
    with app.app_context():
        # 1. Setup VERNAM_KEY if not already set
        test_key = "test-vernam-key-12345"
        if not os.environ.get("VERNAM_KEY"):
            print(f"Setting temporary VERNAM_KEY for testing: {test_key}")
            os.environ["VERNAM_KEY"] = test_key
        else:
            print(f"Using existing VERNAM_KEY: {os.environ.get('VERNAM_KEY')}")

        # 2. Find or create dummy relations to satisfy foreign keys
        print("Finding doctor, patient, department, and appointment...")
        doctor = Doctor.query.first()
        patient = Patient.query.first()
        department = Department.query.first()
        appointment = Appointment.query.first()

        if not (doctor and patient and department and appointment):
            print("ERROR: Test requires a seeded database with at least one doctor, patient, department, and appointment.")
            print("Please run backend/scripts/seed_db.py first.")
            sys.exit(1)

        # 3. Create test data
        test_diagnosis = "Influenza A with secondary acute bronchitis"
        test_vitals = '{"bp": "118/75", "hr": 78, "temp": 101.2}'
        test_medicines = "Oseltamivir 75mg, Albuterol inhaler"
        test_dosage = "Oseltamivir: twice daily for 5 days; Albuterol: 2 puffs every 4 hours"
        test_instructions = "Take Oseltamivir with food. Inhale Albuterol as needed."

        print("Creating PatientHistory record...")
        history = PatientHistory(
            patient_id=patient.id,
            doctor_id=doctor.id,
            department_id=department.id,
            appointment_id=appointment.id,
            visit_type="Consultation",
            visit_date=appointment.appointment_date,
            diagnosis=test_diagnosis,
            vitals=test_vitals
        )
        db.session.add(history)
        db.session.flush() # Get history ID

        print("Creating Prescription record...")
        prescription = Prescription(
            history_id=history.id,
            medicines=test_medicines,
            dosage=test_dosage,
            instructions=test_instructions
        )
        db.session.add(prescription)
        db.session.commit()

        history_id = history.id
        prescription_id = prescription.id
        print(f"Created PatientHistory ID: {history_id}, Prescription ID: {prescription_id}")

        # 4. Query DB directly using raw SQL to verify that stored values are encrypted
        print("\nVerifying database-level encryption (Raw SQL)...")
        history_row = db.session.execute(
            text("SELECT diagnosis, vitals FROM patient_history WHERE id = :id"),
            {"id": history_id}
        ).fetchone()
        
        prescription_row = db.session.execute(
            text("SELECT medicines, dosage, instructions FROM prescription WHERE id = :id"),
            {"id": prescription_id}
        ).fetchone()

        db_diagnosis = history_row[0]
        db_vitals = history_row[1]
        db_medicines = prescription_row[0]
        db_dosage = prescription_row[1]
        db_instructions = prescription_row[2]

        print(f"Stored diagnosis in DB:  {db_diagnosis}")
        print(f"Stored vitals in DB:     {db_vitals}")
        print(f"Stored medicines in DB:  {db_medicines}")
        print(f"Stored dosage in DB:     {db_dosage}")
        print(f"Stored instructions:     {db_instructions}")

        assert db_diagnosis.startswith("vernam::"), f"Diagnosis does not start with vernam::"
        assert db_vitals.startswith("vernam::"), f"Vitals does not start with vernam::"
        assert db_medicines.startswith("vernam::"), f"Medicines does not start with vernam::"
        assert db_dosage.startswith("vernam::"), f"Dosage does not start with vernam::"
        assert db_instructions.startswith("vernam::"), f"Instructions does not start with vernam::"

        assert db_diagnosis != test_diagnosis, "Diagnosis stored in plaintext!"
        assert db_vitals != test_vitals, "Vitals stored in plaintext!"
        
        print("SUCCESS: Database-level encryption verified (records are prefixed with 'vernam::' and encrypted).")

        # 5. Query DB using SQLAlchemy models to verify they are decrypted
        print("\nVerifying model-level decryption (SQLAlchemy)...")
        decrypted_history = PatientHistory.query.get(history_id)
        decrypted_prescription = Prescription.query.get(prescription_id)

        print(f"Decrypted diagnosis:  {decrypted_history.diagnosis}")
        print(f"Decrypted vitals:     {decrypted_history.vitals}")
        print(f"Decrypted medicines:  {decrypted_prescription.medicines}")
        print(f"Decrypted dosage:     {decrypted_prescription.dosage}")
        print(f"Decrypted instructions: {decrypted_prescription.instructions}")

        assert decrypted_history.diagnosis == test_diagnosis, "Decrypted diagnosis mismatch!"
        assert decrypted_history.vitals == test_vitals, "Decrypted vitals mismatch!"
        assert decrypted_prescription.medicines == test_medicines, "Decrypted medicines mismatch!"
        assert decrypted_prescription.dosage == test_dosage, "Decrypted dosage mismatch!"
        assert decrypted_prescription.instructions == test_instructions, "Decrypted instructions mismatch!"

        print("SUCCESS: Model-level decryption verified (original plaintext values are retrieved).")

        # 6. Verify Backwards Compatibility with plaintext records
        print("\nVerifying backwards compatibility with plaintext...")
        # Manually insert a plaintext record using raw SQL to bypass SQLAlchemy TypeDecorator
        raw_diagnosis = "Classic plaintext diagnosis"
        db.session.execute(
            text("INSERT INTO patient_history (patient_id, doctor_id, department_id, visit_type, visit_date, diagnosis, vitals) "
                 "VALUES (:p_id, :d_id, :dept_id, 'Consultation', :v_date, :diag, NULL)"),
            {
                "p_id": patient.id,
                "d_id": doctor.id,
                "dept_id": department.id,
                "v_date": appointment.appointment_date,
                "diag": raw_diagnosis
            }
        )
        db.session.commit()
        
        # Get the ID of the manually inserted row
        plaintext_row_id = db.session.execute(text("SELECT last_insert_rowid()")).scalar()
        print(f"Manually inserted plaintext PatientHistory ID: {plaintext_row_id}")

        # Fetch through SQLAlchemy
        plaintext_history = PatientHistory.query.get(plaintext_row_id)
        print(f"Retrieved manual diagnosis: {plaintext_history.diagnosis}")
        assert plaintext_history.diagnosis == raw_diagnosis, "Backwards compatibility check failed! Plaintext diagnosis was modified."
        print("SUCCESS: Backwards compatibility verified (unprefixed database entries are read as plaintext).")

        # Clean up
        print("\nCleaning up test records...")
        db.session.delete(decrypted_history)
        db.session.delete(decrypted_prescription)
        db.session.delete(plaintext_history)
        db.session.commit()
        print("Cleanup completed successfully.")
        print("\n--- ALL TESTS PASSED SUCCESSFULLY! ---")

if __name__ == "__main__":
    run_tests()

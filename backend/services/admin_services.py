from backend.models import User, Doctor, Patient
from backend.services.service_errors import ServiceError
from backend.extensions import db
from datetime import datetime
import uuid


class AdminService:

    # --------------------------------------------
    # GET LISTS
    # --------------------------------------------
    @staticmethod
    def get_all_doctors():
        doctors = User.query.filter_by(role='doctor').all()
        if not doctors:
            raise ServiceError("No doctors found")
        return [doctor.to_dict() for doctor in doctors]

    @staticmethod
    def get_all_patients():
        patients = User.query.filter_by(role='patient').all()
        if not patients:
            raise ServiceError("No patients found")
        return [patient.to_dict() for patient in patients]


    # --------------------------------------------
    # CREATE DOCTOR / PATIENT
    # --------------------------------------------
    @staticmethod
    def create_doctor(data):
        if User.query.filter_by(email=data['email']).first():
            raise ServiceError("User with this email already exists")

        new_user = User(
            name=data['name'],
            email=data['email'],
            password=data['password'],  # hash in real world
            role='doctor',
            contact_number=data.get('contact_number'),
            fs_uniquifier=str(uuid.uuid4())
        )

        db.session.add(new_user)
        db.session.commit()

        new_doctor = Doctor(
            id=new_user.id,
            department_id=data['department_id'],
            specialization=data['specialization'],
            qualifications=data.get('qualifications'),
            experience=data.get('experience')
        )
        db.session.add(new_doctor)
        db.session.commit()
        return new_doctor

    @staticmethod
    def create_patient(data):
        if User.query.filter_by(email=data['email']).first():
            raise ServiceError("User with this email already exists")

        new_user = User(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            role='patient',
            contact_number=data.get('contact_number'),
            fs_uniquifier=str(uuid.uuid4())
        )

        db.session.add(new_user)
        db.session.commit()

        dob_val = data['dob']
        if isinstance(dob_val, str):
            dob_val = datetime.fromisoformat(dob_val)

        new_patient = Patient(
            id=new_user.id,
            dob=dob_val,
            contact=data['contact'],
            medical_record_number=data['medical_record_number'],
            doctor_id=data.get('doctor_id')
        )

        db.session.add(new_patient)
        db.session.commit()
        return new_patient


    # --------------------------------------------
    # DELETE DOCTOR / PATIENT
    # --------------------------------------------
    @staticmethod
    def delete_doctor_by_id(doctor_id):
        doctor_user = User.query.filter_by(id=doctor_id, role='doctor').first()
        if not doctor_user:
            raise ServiceError("Doctor not found")
        
        doctor = doctor_user.doctor
        if doctor:
            # Cascade delete:
            # 1. Delete appointments
            for appointment in doctor.appointments:
                db.session.delete(appointment)
            
            # 2. Delete medical histories (and their prescriptions)
            for history in doctor.histories:
                # Prescriptions cascade from history usually, but let's be safe if not configured
                for prescription in history.prescriptions:
                    db.session.delete(prescription)
                db.session.delete(history)
            
            # 3. Unlink patients
            for patient in doctor.patients:
                patient.doctor_id = None
            
            # 4. Delete availabilities (cascade usually handles this but explicit is fine)
            for slot in doctor.availabilities:
                db.session.delete(slot)

        db.session.delete(doctor_user)
        db.session.commit()

    @staticmethod
    def delete_patient_by_id(patient_id):
        patient_user = User.query.filter_by(id=patient_id, role='patient').first()
        if not patient_user:
            raise ServiceError("Patient not found")
        
        patient = patient_user.patient
        if patient:
            # Cascade delete:
            # 1. Delete appointments
            for appointment in patient.appointments:
                db.session.delete(appointment)
            
            # 2. Delete medical histories (and their prescriptions)
            for history in patient.histories:
                # Delete prescriptions associated with this history
                for prescription in history.prescriptions:
                    db.session.delete(prescription)
                db.session.delete(history)
        
        db.session.delete(patient_user)
        db.session.commit()


    # --------------------------------------------
    # UPDATE DOCTOR
    # --------------------------------------------
    @staticmethod
    def update_doctor(data):
        doctor = Doctor.query.filter_by(id=data.get('id')).first()
        if not doctor:
            raise ServiceError("Doctor not found")

        user = doctor.user

        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.contact_number = data.get('contact_number', user.contact_number)

        doctor.department_id = data.get('department_id', doctor.department_id)
        doctor.specialization = data.get('specialization', doctor.specialization)
        doctor.qualifications = data.get('qualifications', doctor.qualifications)
        doctor.experience = data.get('experience', doctor.experience)

        db.session.commit()
        return doctor


    # --------------------------------------------
    # UPDATE PATIENT
    # --------------------------------------------
    @staticmethod
    def update_patient(data):
        patient = Patient.query.filter_by(id=data.get('id')).first()
        if not patient:
            raise ServiceError("Patient not found")

        user = patient.user

        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.contact_number = data.get('contact_number', user.contact_number)

        if "dob" in data:
            dob_val = data["dob"]
            if isinstance(dob_val, str):
                dob_val = datetime.fromisoformat(dob_val)
            patient.dob = dob_val

        patient.contact = data.get('contact', patient.contact)
        patient.medical_record_number = data.get('medical_record_number', patient.medical_record_number)
        patient.doctor_id = data.get('doctor_id', patient.doctor_id)

        db.session.commit()
        return patient

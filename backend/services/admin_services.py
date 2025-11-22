from backend.models import User, Doctor, Patient
from backend.services.service_errors import ServiceError
from backend.extensions import db

class AdminService:

    @staticmethod
    def get_user_by_name(name):
        return User.query.filter_by(name=name).all()


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


    @staticmethod
    def create_doctor(data):
        if User.query.filter_by(email=data['email']).first():
            raise ServiceError(f"User with email {data['email']} already exists")
        
        new_user = User(
            name=data['name'],
            email=data['email'],
            password=data['password'],  # In real application, hash the password
            role='doctor',
            contact_number=data.get('contact_number')
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
            raise ServiceError(f"User with email {data['email']} already exists")
        
        new_user = User(
            name=data['name'],
            email=data['email'],
            password=data['password'],  # In real application, hash the password
            role='patient',
            contact_number=data.get('contact_number')
        )
        db.session.add(new_user)
        db.session.commit()

        new_patient = Patient(
            id=new_user.id,
            dob=data['dob'],
            contact=data['contact'],
            medical_record_number=data['medical_record_number'],
            doctor_id=data.get('doctor_id')
        )
        db.session.add(new_patient)
        db.session.commit()
        return new_patient



    @staticmethod
    def delete_doctor_by_id(doctor_id):
        doctor = User.query.filter_by(id=doctor_id, role='doctor').first()
        if not doctor:
            raise ServiceError(f"Doctor with id {doctor_id} not found")
        db.session.delete(doctor)
        db.session.commit()
        return True

    @staticmethod
    def delete_patient_by_id(patient_id):
        patient = User.query.filter_by(id=patient_id, role='patient').first()
        if not patient:
            raise ServiceError(f"Patient with id {patient_id} not found")
        db.session.delete(patient)
        db.session.commit()
        return True
    
    @staticmethod
    def update_doctor(data):
        doctor = Doctor.query.filter_by(id=data.get('id')).first()
        if not doctor:
            raise ServiceError(f"Doctor with id {data.get('id')} not found")    
            
        doctor.user.name = data.get('name', doctor.user.name)
        doctor.user.email = data.get('email', doctor.user.email)
        doctor.user.contact_number = data.get('contact_number', doctor.user.contact_number)

        doctor.department_id = data.get('department_id', doctor.department_id)
        doctor.specialization = data.get('specialization', doctor.specialization)
        doctor.qualifications = data.get('qualifications', doctor.qualifications)
        doctor.experience = data.get('experience', doctor.experience)
        
        db.session.commit()
        return doctor
    
    @staticmethod
    def update_patient(data):
        patient = Patient.query.filter_by(id=data.get('id')).first()
        if not patient:
            raise ServiceError(f"Patient with id {data.get('id')} not found")

        patient.user.name = data.get('name', patient.user.name)
        patient.user.email = data.get('email', patient.user.email)
        patient.user.contact_number = data.get('contact_number', patient.user.contact_number)

        patient.dob = data.get('dob', patient.dob)
        patient.contact = data.get('contact', patient.contact)
        patient.medical_record_number = data.get('medical_record_number', patient.medical_record_number)
        patient.doctor_id = data.get('doctor_id', patient.doctor_id)
        patient.experience = data.get('experience', patient.experience)

        db.session.commit()
        return patient
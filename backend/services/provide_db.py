from models import User, Doctor
from services.service_errors import ServiceError
from extensions import db

class DoctorService:
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_all():
        doctors = User.query.filter_by(role='doctor').all()
        if not doctors:
            raise ServiceError("No doctors found")
        return doctors

    @staticmethod
    def delete_by_id(doctor_id):
        doctor = User.query.filter_by(id=doctor_id, role='doctor').first()
        if not doctor:
            raise ServiceError(f"Doctor with id {doctor_id} not found")
        db.session.delete(doctor)
        db.session.commit()
        return True
    
    @staticmethod
    def update(data):
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
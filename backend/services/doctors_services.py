from backend.models import User, Doctor
from backend.services.service_errors import ServiceError
from backend.extensions import db

class DoctorService:

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    def get_by_id(id):
        return Doctor.query.filter_by(id=id).first()

    @staticmethod
    def get_all(include_blocked=False, department_id=None):
        from sqlalchemy.orm import joinedload
        # Always use joinedload to eagerly load the user relationship
        query = Doctor.query.options(joinedload(Doctor.user), joinedload(Doctor.department))
        
        # Only filter out blacklisted users if include_blocked is False
        if not include_blocked:
            query = query.filter(Doctor.user.has(blacklisted=False))
            
        if department_id:
            query = query.filter(Doctor.department_id == department_id)
            
        doctors = query.all()
        return [doctor.to_dict() for doctor in doctors]

    @staticmethod
    def create(data):
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
        
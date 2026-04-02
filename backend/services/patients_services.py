from backend.models import User, Patient
from backend.services.service_errors import ServiceError
from backend.extensions import db
from datetime import datetime

class PatientService:

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(id):
        return Patient.query.filter_by(id=id).first()

    @staticmethod
    def get_all(limit=None, offset=None, search=None):
        from sqlalchemy.orm import joinedload
        query = Patient.query.options(joinedload(Patient.user), joinedload(Patient.billings))
        
        if search:
            query = query.join(User).filter(User.name.ilike(f'%{search}%'))
            
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
            
        patients = query.all()
        return [patient.to_dict() for patient in patients]

    @staticmethod
    def get_patients_for_doctor(doctor_id, limit=None, offset=None, search=None):
        from backend.models import Appointment
        from sqlalchemy.orm import joinedload
        
        query = Patient.query.join(Appointment).filter(
            Appointment.doctor_id == doctor_id
        ).options(joinedload(Patient.user)).distinct()
        
        if search:
            query = query.join(User).filter(User.name.ilike(f'%{search}%'))
            
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
            
        patients = query.all()
        return [patient.to_dict() for patient in patients]

    @staticmethod
    def create(data):
        # Check duplicate email
        if User.query.filter_by(email=data['email']).first():
            raise ServiceError(f"User with email {data['email']} already exists")

        # Create USER
        new_user = User(
            name=data['name'],
            email=data['email'],
            password=data['password'],   # same as doctor service (not hashed)
            role='patient',
            contact_number=data.get('contact_number')
        )
        db.session.add(new_user)
        db.session.commit()

        # Convert DOB if needed
        dob_value = data['dob']
        if isinstance(dob_value, str):
            dob_value = datetime.fromisoformat(dob_value)

        # Create PATIENT
        mrn = data.get('medical_record_number')
        if not mrn:
            import uuid
            mrn = f"MRN-{str(uuid.uuid4())[:8].upper()}"

        new_patient = Patient(
            id=new_user.id,
            dob=dob_value,
            contact=data['contact'],
            medical_record_number=mrn,
            doctor_id=data.get('doctor_id')   # optional
        )
        
        db.session.add(new_patient)
        db.session.commit()

        return new_patient

    @staticmethod
    def delete_by_id(patient_id):
        user = User.query.filter_by(id=patient_id, role='patient').first()
        if not user:
            raise ServiceError(f"Patient with id {patient_id} not found")
        db.session.delete(user)
        db.session.commit()
        return True

    @staticmethod
    def update(data):
        patient = Patient.query.filter_by(id=data.get('id')).first()
        if not patient:
            raise ServiceError(f"Patient with id {data.get('id')} not found")

        # Update USER fields
        patient.user.name = data.get('name', patient.user.name)
        patient.user.email = data.get('email', patient.user.email)
        patient.user.contact_number = data.get('contact_number', patient.user.contact_number)

        # Update PATIENT fields
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

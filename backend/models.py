from backend.extensions import db
from datetime import datetime, timezone

# abstract class for all models to inherit from
class BaseModel(db.Model):

    # tells sqlalchemy to not create a table for this BaseModel class
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    # datetime.now(timezone.utc) value will be assigned and stored at the time of object creation.
    # we use a lambda to ensure that the function is called at each time of the object creation.
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict_base(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class User(BaseModel):
    __tablename__ = 'user'

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(15), nullable=True)
    blacklisted = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    # One-to-one with Doctor & Patient
    doctor = db.relationship('Doctor', back_populates='user', uselist=False, cascade="all, delete-orphan")
    patient = db.relationship('Patient', back_populates='user', uselist=False, cascade="all, delete-orphan")

    # uselist is a parameter in db.relationship() that tells SQLAlchemy whether the relationship should return a list of objects or a single object.

    def to_dict(self):
        data = self.to_dict_base()
        data.update({
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "contact_number": self.contact_number,
            "active": self.active,
            "blacklisted": self.blacklisted,
        })
        if self.doctor:
            data["doctor"] = self.doctor.to_dict_basic()
        if self.patient:
            data["patient"] = self.patient.to_dict_basic()
        return data


class Doctor(BaseModel):

    __tablename__ = 'doctor'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    qualifications = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)

    # One-to-one with Doctor & Patient
    user = db.relationship('User', back_populates='doctor', uselist=False)
    department = db.relationship('Department', back_populates='doctors')
    availabilities = db.relationship('AvailabilitySlot', back_populates='doctor', cascade='all, delete-orphan')
    appointments = db.relationship('Appointment', back_populates='doctor')
    histories = db.relationship('PatientHistory', back_populates='doctor')
    patients = db.relationship('Patient', back_populates='doctor')

    def to_dict(self):
        data = self.to_dict_base()
        data.update({
            "department_id": self.department_id,
            "specialization": self.specialization,
            "qualifications": self.qualifications,
            "experience": self.experience,
            "user": self.user.to_dict() if self.user else None,
            "department": self.department.to_dict() if self.department else None,
        })
        return data

    def to_dict_basic(self):
        """Lightweight version to avoid recursion in user.to_dict()."""
        return {
            "id": self.id,
            "specialization": self.specialization,
            "qualifications": self.qualifications,
            "experience": self.experience,
        }

# we can create a section table so that if we want to change something then we can send request to admin for same through section table
# like cardiology, neurology etc

class Patient(BaseModel):
    __tablename__ = 'patient'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    dob = db.Column(db.DateTime(timezone=True), nullable=False)
    contact = db.Column(db.String(15), unique=True, nullable=False)
    medical_record_number = db.Column(db.String(100), unique=True, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))

    # One-to-one with User
    user = db.relationship('User', back_populates='patient', uselist=False)

    # One-to-many relationships
    appointments = db.relationship('Appointment', back_populates='patient')
    histories = db.relationship('PatientHistory', back_populates='patient')
    doctor = db.relationship('Doctor', back_populates='patients')

    def to_dict(self):
        data = self.to_dict_base()
        data.update({
            "dob": self.dob.isoformat() if self.dob else None,
            "contact": self.contact,
            "medical_record_number": self.medical_record_number,
            "doctor_id": self.doctor_id,
            "user": self.user.to_dict() if self.user else None,
        })
        return data

        
    def to_dict_basic(self):
        return {
            "id": self.id,
            "contact": self.contact,
            "medical_record_number": self.medical_record_number,
        }


class Department(BaseModel):
    __tablename__ = 'department'

    name = db.Column(db.String(100), unique=True, nullable=False)
    overview = db.Column(db.String(100), nullable=True)

    # relationships
    doctors = db.relationship('Doctor', back_populates='department')
    appointments = db.relationship('Appointment', back_populates='department')
    histories = db.relationship('PatientHistory', back_populates='department')

    def to_dict(self):
        data = self.to_dict_base()
        data.update({
            "name": self.name,
            "overview": self.overview,
        })
        return data

class Appointment(BaseModel):
    __tablename__ = 'appointment'

    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    appointment_date = db.Column(db.DateTime(timezone=True), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # e.g., scheduled, completed, canceled

    # relationships
    patient = db.relationship('Patient', back_populates='appointments')
    doctor = db.relationship('Doctor', back_populates='appointments')
    department = db.relationship('Department', back_populates='appointments')
    history = db.relationship('PatientHistory', back_populates='appointment', uselist=False)

    def to_dict(self):
        data = self.to_dict_base()
        
        # Ensure appointment_date is timezone aware (assume UTC if naive)
        appt_date = self.appointment_date
        if appt_date and appt_date.tzinfo is None:
            appt_date = appt_date.replace(tzinfo=timezone.utc)

        data.update({
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "department_id": self.department_id,
            "appointment_date": appt_date.isoformat() if appt_date else None,
            "status": self.status,
            "patient": self.patient.to_dict() if self.patient else None,
            "doctor": self.doctor.to_dict() if self.doctor else None,
            "department": self.department.to_dict() if self.department else None,
        })
        return data

class PatientHistory(BaseModel):
    __tablename__ = 'patient_history'

    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    visit_type = db.Column(db.String(100), nullable=False)  # e.g., consultation, follow-up
    visit_date = db.Column(db.DateTime(timezone=True), nullable=False)
    diagnosis = db.Column(db.String(255), nullable=True)

    # relationships
    patient = db.relationship('Patient', back_populates='histories')
    doctor = db.relationship('Doctor', back_populates='histories')
    department = db.relationship('Department', back_populates='histories')
    appointment = db.relationship('Appointment', back_populates='history')
    prescriptions = db.relationship('Prescription', back_populates='history')

    def to_dict(self):
        data = self.to_dict_base()
        data.update({
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "department_id": self.department_id,
            "appointment_id": self.appointment_id,
            "visit_type": self.visit_type,
            "visit_date": self.visit_date.isoformat() if self.visit_date else None,
            "diagnosis": self.diagnosis,
            "prescriptions": [p.to_dict() for p in self.prescriptions],
            "doctor": self.doctor.to_dict() if self.doctor else None,
            "department": self.department.to_dict() if self.department else None,
        })
        return data

class Prescription(BaseModel):
    __tablename__ = 'prescription'

    history_id = db.Column(db.Integer, db.ForeignKey('patient_history.id'), nullable=False)
    medicines = db.Column(db.String(255), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.String(255), nullable=True)

    # relationship
    history = db.relationship('PatientHistory', back_populates='prescriptions')

    def to_dict(self):
        data = self.to_dict_base()
        data.update({
            "history_id": self.history_id,
            "medicines": self.medicines,
            "dosage": self.dosage,
            "instructions": self.instructions,
        })
        return data


class AvailabilitySlot(BaseModel):
    __tablename__ = 'availability_slot'

    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    available_date = db.Column(db.DateTime(timezone=True), nullable=False)
    time_slot = db.Column(db.String(50), nullable=False)  # e.g., "09:00-10:00"
    status = db.Column(db.Enum('available', 'booked', name='slot_status'), default='available', nullable=False)

    # relationship
    doctor = db.relationship('Doctor', back_populates='availabilities')

    def to_dict(self):
        data = self.to_dict_base()
        data.update({
            "doctor_id": self.doctor_id,
            "available_date": self.available_date.isoformat() if self.available_date else None,
            "time_slot": self.time_slot,
            "status": self.status,
        })
        return data
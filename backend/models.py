from backend.extensions import db
from datetime import datetime, timezone
from flask_security.core import UserMixin, RoleMixin
import os
import base64
import random
from sqlalchemy.types import TypeDecorator, Text

class VernamEncryptedString(TypeDecorator):
    """Custom SQLAlchemy TypeDecorator that encrypts text using a Vernam stream cipher
    before saving to the database, and decrypts it when reading."""
    
    impl = Text

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_key(self):
        key = os.environ.get("VERNAM_KEY")
        if not key:
            key = os.environ.get("SECRET_KEY", "default-vernam-key")
        return key

    def _vernam_cipher_bytes(self, data_bytes, key):
        if not data_bytes:
            return b""
        prng = random.Random(key)
        keystream = bytes(prng.randint(0, 255) for _ in range(len(data_bytes)))
        return bytes(t ^ k for t, k in zip(data_bytes, keystream))

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if not isinstance(value, str):
            value = str(value)
        if value.startswith("vernam::"):
            return value

        key = self._get_key()
        utf8_bytes = value.encode('utf-8')
        encrypted_bytes = self._vernam_cipher_bytes(utf8_bytes, key)
        base64_str = base64.b64encode(encrypted_bytes).decode('utf-8')
        return f"vernam::{base64_str}"

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if not value.startswith("vernam::"):
            return value

        try:
            base64_str = value[len("vernam::"):]
            encrypted_bytes = base64.b64decode(base64_str.encode('utf-8'))
            key = self._get_key()
            decrypted_bytes = self._vernam_cipher_bytes(encrypted_bytes, key)
            return decrypted_bytes.decode('utf-8')
        except Exception:
            return value


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


class User(BaseModel, UserMixin):
    __tablename__ = 'user'

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(50), nullable=True)
    blacklisted = db.Column(db.Boolean, default=False)

    # One-to-one with Doctor & Patient
    doctor = db.relationship('Doctor', back_populates='user', uselist=False, cascade="all, delete-orphan")
    patient = db.relationship('Patient', back_populates='user', uselist=False, cascade="all, delete-orphan")

    # uselist is a parameter in db.relationship() that tells SQLAlchemy whether the relationship should return a list of objects or a single object.

    # for flask-security-too
    fs_uniquifier = db.Column(db.String, unique = True, nullable =False)
    active = db.Column(db.Boolean, default = True) # False, then the user will not be able to login
    roles = db.Relationship('Role', backref = 'bearers', secondary='user_roles') 

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


# patient, doctor, admin etc
class Role(BaseModel, RoleMixin):
    name = db.Column(db.String, unique = True, nullable = False)
    description = db.Column(db.String, nullable = True)


# which user has which role
class UserRoles (BaseModel) :
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db. Integer, db.ForeignKey('role.id'))

    
    def to_dict(self):
        data = self.to_dict_base()
        data.update({
            "user_id": self.user_id,
            "role_id": self.role_id,
        })
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
            "patient_count": len(self.patients) if self.patients else 0,
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
    contact = db.Column(db.String(50), unique=True, nullable=False)
    medical_record_number = db.Column(db.String(100), unique=True, nullable=False)
    gender = db.Column(db.String(10), default='Other', nullable=False)
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
            "gender": self.gender,
            "doctor_id": self.doctor_id,
            "user": self.user.to_dict() if self.user else None,
            "paid_billings_count": sum(1 for b in self.billings if b.status == 'paid') if self.billings else 0,
            "unpaid_billings_count": sum(1 for b in self.billings if b.status in ['pending', 'overdue']) if self.billings else 0,
            "total_unpaid_amount": sum(b.total_amount for b in self.billings if b.status in ['pending', 'overdue']) if self.billings else 0.0,
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
            "has_feedback": bool(self.feedback)
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
    diagnosis = db.Column(VernamEncryptedString, nullable=True)
    vitals = db.Column(VernamEncryptedString, nullable=True) # JSON format string: {"bp": "120/80", "hr": 72, "temp": 98.6}

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
            "vitals": self.vitals,
            "prescriptions": [p.to_dict() for p in self.prescriptions],
            "doctor": self.doctor.to_dict() if self.doctor else None,
            "department": self.department.to_dict() if self.department else None,
            "appointment": self.appointment.to_dict() if self.appointment else None,
        })
        return data

class Prescription(BaseModel):
    __tablename__ = 'prescription'

    history_id = db.Column(db.Integer, db.ForeignKey('patient_history.id'), nullable=False)
    medicines = db.Column(VernamEncryptedString, nullable=False)
    dosage = db.Column(VernamEncryptedString, nullable=False)
    instructions = db.Column(VernamEncryptedString, nullable=True)

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

class Billing(BaseModel):
    __tablename__ = 'billing'

    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=True)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending', nullable=False)  # pending, paid, overdue
    due_date = db.Column(db.DateTime(timezone=True), nullable=True)

    # Relationships
    patient = db.relationship('Patient', backref='billings')
    appointment = db.relationship('Appointment', backref='billing')
    payments = db.relationship('Payment', back_populates='billing', cascade='all, delete-orphan')

    def to_dict(self):
        data = self.to_dict_base()

        # Helper to get patient name safely
        p_name = "Unknown"
        p_uhid = "N/A"
        p_contact = "N/A"
        if self.patient and self.patient.user:
            p_name = self.patient.user.name
            p_uhid = self.patient.medical_record_number or f"P-{self.patient.id}"
            p_contact = self.patient.contact

        # Helper to get doctor info
        doc_name = "N/A"
        dept_name = "General"
        if self.appointment and self.appointment.doctor and self.appointment.doctor.user:
            doc_name = self.appointment.doctor.user.name
            if self.appointment.department:
                dept_name = self.appointment.department.name

        data.update({
            "patient_id": self.patient_id,
            "appointment_id": self.appointment_id,
            "total_amount": self.total_amount,
            "status": self.status,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "payments": [p.to_dict() for p in self.payments],
            "extra_details": {
                "patient_name": p_name,
                "patient_uhid": p_uhid,
                "patient_contact": p_contact,
                "doctor_name": doc_name,
                "department": dept_name,
                "visit_type": "OPD Consultation",
                "appointment_date": self.appointment.appointment_date.isoformat() if self.appointment and self.appointment.appointment_date else None
            }
        })
        return data

class Payment(BaseModel):
    __tablename__ = 'payment'

    billing_id = db.Column(db.Integer, db.ForeignKey('billing.id'), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    payment_method = db.Column(db.String(50), nullable=False) # cash, card, insurance
    transaction_id = db.Column(db.String(100), nullable=True)

    # Relationship
    billing = db.relationship('Billing', back_populates='payments')

    def to_dict(self):
        data = self.to_dict_base()
        data.update({
            "billing_id": self.billing_id,
            "amount_paid": self.amount_paid,
            "payment_date": self.payment_date.isoformat(),
            "payment_method": self.payment_method,
            "transaction_id": self.transaction_id
        })
        return data

class Inventory(BaseModel):
    __tablename__ = 'inventory_item'

    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False) # medicine, equipment, consumable
    quantity = db.Column(db.Integer, default=0, nullable=False)
    reorder_level = db.Column(db.Integer, default=10, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    supplier = db.Column(db.String(100), nullable=True)
    last_restocked = db.Column(db.DateTime(timezone=True), nullable=True)

    def to_dict(self):
        data = self.to_dict_base()
        data.update({
            "name": self.name,
            "category": self.category,
            "quantity": self.quantity,
            "reorder_level": self.reorder_level,
            "unit_price": self.unit_price,
            "supplier": self.supplier,
            "last_restocked": self.last_restocked.isoformat() if self.last_restocked else None
        })
        return data

class ChatMessage(BaseModel):
    __tablename__ = 'chat_message'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    action_data = db.Column(db.Text, nullable=True) # JSON string of action if any
    
    # Relationship
    user = db.relationship('User', backref='chat_history')

    def to_dict(self):
        data = self.to_dict_base()
        data.update({
            "user_id": self.user_id,
            "role": self.role,
            "content": self.content,
            "action_data": self.action_data
        })
        return data

class EscalationTicket(BaseModel):
    __tablename__ = 'escalation_ticket'

    ticket_id = db.Column(db.String(50), unique=True, nullable=False)
    requested_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Optional, can be anonymous
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open') # open, resolved, closed

    def to_dict(self):
        data = self.to_dict_base()
        data.update({
            "ticket_id": self.ticket_id,
            "requested_by": self.requested_by,
            "reason": self.reason,
            "status": self.status
        })
        return data

class HospitalGoal(BaseModel):
    __tablename__ = 'hospital_goal'

    name = db.Column(db.String(100), nullable=False) # e.g., "Monthly Revenue", "Patient Satisfaction"
    target_value = db.Column(db.Float, nullable=False)
    current_value = db.Column(db.Float, default=0.0, nullable=False)
    period = db.Column(db.String(50), default="Monthly") 
    unit = db.Column(db.String(20), default="") # e.g., "$", "%"

    def to_dict(self):
        data = self.to_dict_base()
        data.update({
            "name": self.name,
            "target_value": self.target_value,
            "current_value": self.current_value,
            "period": self.period,
            "unit": self.unit
        })
        return data

class Feedback(BaseModel):
    __tablename__ = 'feedback'

    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), unique=True, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text, nullable=True)

    # Relationships
    appointment = db.relationship('Appointment', backref=db.backref('feedback', uselist=False))
    doctor = db.relationship('Doctor', backref='feedbacks')
    patient = db.relationship('Patient', backref='feedbacks')

    def to_dict(self):
        data = self.to_dict_base()
        data.update({
            "appointment_id": self.appointment_id,
            "doctor_id": self.doctor_id,
            "patient_id": self.patient_id,
            "rating": self.rating,
            "comment": self.comment,
            # optional expansions
            "patient_name": self.patient.user.name if self.patient and self.patient.user else "Anonymous"
        })
        return data
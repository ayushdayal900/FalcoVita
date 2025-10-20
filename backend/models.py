from extensions import db
from datetime import datetime, timezone
from flask_security.core import UserMixin, RoleMixin

# abstract class for all models to inherit from
class BaseModel(db.Model):

    # tells sqlalchemy to not create a table for this BaseModel class
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    # datetime.now(timezone.utc) value will be assigned and stored at the time of object creation.
    # we use a lambda to ensure that the function is called at each time of the object creation.
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class User(BaseModel, UserMixin):
    __tablename__ = 'user'

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    contact_number = db.Column(db.String(15), nullable=True)

    # One-to-one with Doctor & Patient
    doctor = db.relationship('Doctor', back_populates='user', uselist=False)
    patient = db.relationship('Patient', back_populates='user', uselist=False)
    # uselist is a parameter in db.relationship() that tells SQLAlchemy whether the relationship should return a list of objects or a single object.


    # for flask-security-too
    fs_uniquifier = db.Column(db.String, unique = True, nullable =False)
    active = db.Column(db.Boolean, default = True) # False, then the user will not be able to login
    roles = db.Relationship('Role', backref = 'bearers', secondary='user_roles') 



# patient, doctor, admin etc
class Role(BaseModel, RoleMixin):
    name = db.Column(db.String, unique = True, nullable = False)
    description = db.Column(db.String, nullable = True)


# which user has which role
class UserRoles (BaseModel) :
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db. Integer, db.ForeignKey('role.id'))



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


class Department(BaseModel):
    __tablename__ = 'department'

    name = db.Column(db.String(100), unique=True, nullable=False)
    overview = db.Column(db.String(100), nullable=True)

    # relationships
    doctors = db.relationship('Doctor', back_populates='department')
    appointments = db.relationship('Appointment', back_populates='department')
    histories = db.relationship('PatientHistory', back_populates='department')


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


class Prescription(BaseModel):
    __tablename__ = 'prescription'

    history_id = db.Column(db.Integer, db.ForeignKey('patient_history.id'), nullable=False)
    medicines = db.Column(db.String(255), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.String(255), nullable=True)

    # relationship
    history = db.relationship('PatientHistory', back_populates='prescriptions')


class AvailabilitySlot(BaseModel):
    __tablename__ = 'availability_slot'

    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    available_date = db.Column(db.DateTime(timezone=True), nullable=False)
    time_slot = db.Column(db.String(50), nullable=False)  # e.g., "09:00-10:00"
    status = db.Column(db.Enum('available', 'booked', name='slot_status'), default='available', nullable=False)

    # relationship
    doctor = db.relationship('Doctor', back_populates='availabilities')

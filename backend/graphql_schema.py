import graphene
from datetime import datetime, timezone
from backend.models import User as UserModel, Doctor as DoctorModel, Patient as PatientModel, Appointment as AppointmentModel, Department as DepartmentModel, Billing as BillingModel
from backend.extensions import db

class UserType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    email = graphene.String()
    role = graphene.String()
    contact_number = graphene.String()
    active = graphene.Boolean()
    blacklisted = graphene.Boolean()

class DepartmentType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    overview = graphene.String()

class DoctorType(graphene.ObjectType):
    id = graphene.Int()
    specialization = graphene.String()
    qualifications = graphene.String()
    experience = graphene.Int()
    user = graphene.Field(UserType)
    department = graphene.Field(DepartmentType)

    def resolve_user(parent, info):
        return parent.user

    def resolve_department(parent, info):
        return parent.department

class PatientType(graphene.ObjectType):
    id = graphene.Int()
    dob = graphene.String()
    contact = graphene.String()
    medical_record_number = graphene.String()
    gender = graphene.String()
    user = graphene.Field(UserType)
    doctor = graphene.Field(DoctorType)

    def resolve_dob(parent, info):
        return parent.dob.isoformat() if parent.dob else None

    def resolve_user(parent, info):
        return parent.user

    def resolve_doctor(parent, info):
        return parent.doctor

class AppointmentType(graphene.ObjectType):
    id = graphene.Int()
    appointment_date = graphene.String()
    status = graphene.String()
    patient = graphene.Field(PatientType)
    doctor = graphene.Field(DoctorType)
    department = graphene.Field(DepartmentType)

    def resolve_appointment_date(parent, info):
        return parent.appointment_date.isoformat() if parent.appointment_date else None

    def resolve_patient(parent, info):
        return parent.patient

    def resolve_doctor(parent, info):
        return parent.doctor

    def resolve_department(parent, info):
        return parent.department

class BillingType(graphene.ObjectType):
    id = graphene.Int()
    total_amount = graphene.Float()
    status = graphene.String()
    due_date = graphene.String()
    patient = graphene.Field(PatientType)
    appointment = graphene.Field(AppointmentType)

    def resolve_due_date(parent, info):
        return parent.due_date.isoformat() if parent.due_date else None

    def resolve_patient(parent, info):
        return parent.patient

    def resolve_appointment(parent, info):
        return parent.appointment


class Query(graphene.ObjectType):
    doctors = graphene.List(DoctorType, search=graphene.String(), specialization=graphene.String())
    doctor = graphene.Field(DoctorType, id=graphene.Int(required=True))
    patients = graphene.List(PatientType)
    patient = graphene.Field(PatientType, id=graphene.Int(required=True))
    appointments = graphene.List(AppointmentType)
    billings = graphene.List(BillingType)

    def resolve_doctors(parent, info, search=None, specialization=None):
        query = DoctorModel.query
        if specialization:
            query = query.filter(DoctorModel.specialization.ilike(f"%{specialization}%"))
        if search:
            query = query.join(UserModel).filter(UserModel.name.ilike(f"%{search}%"))
        return query.all()

    def resolve_doctor(parent, info, id):
        return DoctorModel.query.filter_by(id=id).first()

    def resolve_patients(parent, info):
        return PatientModel.query.all()

    def resolve_patient(parent, info, id):
        return PatientModel.query.filter_by(id=id).first()

    def resolve_appointments(parent, info):
        return AppointmentModel.query.all()

    def resolve_billings(parent, info):
        return BillingModel.query.all()


class CreateAppointment(graphene.Mutation):
    class Arguments:
        patient_id = graphene.Int(required=True)
        doctor_id = graphene.Int(required=True)
        department_id = graphene.Int(required=True)
        appointment_date = graphene.String(required=True)

    appointment = graphene.Field(AppointmentType)
    success = graphene.Boolean()

    def mutate(parent, info, patient_id, doctor_id, department_id, appointment_date):
        try:
            # Parse ISO date (e.g. 2026-06-16T18:00:00)
            if appointment_date.endswith("Z"):
                appointment_date = appointment_date[:-1] + "+00:00"
            appt_dt = datetime.fromisoformat(appointment_date)
            if appt_dt.tzinfo is None:
                appt_dt = appt_dt.replace(tzinfo=timezone.utc)
        except ValueError:
            raise Exception("Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)")
        
        appt = AppointmentModel(
            patient_id=patient_id,
            doctor_id=doctor_id,
            department_id=department_id,
            appointment_date=appt_dt,
            status="scheduled"
        )
        db.session.add(appt)
        db.session.commit()
        return CreateAppointment(appointment=appt, success=True)


class UpdateAppointmentStatus(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        status = graphene.String(required=True)

    appointment = graphene.Field(AppointmentType)
    success = graphene.Boolean()

    def mutate(parent, info, id, status):
        appt = AppointmentModel.query.filter_by(id=id).first()
        if not appt:
            raise Exception("Appointment not found")
        appt.status = status
        db.session.commit()
        return UpdateAppointmentStatus(appointment=appt, success=True)


class Mutation(graphene.ObjectType):
    create_appointment = CreateAppointment.Field()
    update_appointment_status = UpdateAppointmentStatus.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

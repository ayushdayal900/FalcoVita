from backend.models import Appointment, Patient, Doctor, Department
from backend.services.service_errors import ServiceError
from backend.extensions import db
from datetime import datetime


class AppointmentService:

    # ----------------------------------------
    # GET appointment by ID
    # ----------------------------------------
    @staticmethod
    def get_by_id(appointment_id):
        return Appointment.query.filter_by(id=appointment_id).first()

    # ----------------------------------------
    # LIST all appointments
    # ----------------------------------------
    @staticmethod
    def get_all():
        appointments = Appointment.query.all()
        if not appointments:
            raise ServiceError("No appointments found")
        return [a.to_dict() for a in appointments]

    # ----------------------------------------
    # CREATE appointment
    # ----------------------------------------
    @staticmethod
    def create(data):
        required_fields = ["patient_id", "doctor_id", "department_id", "appointment_date", "status"]

        for f in required_fields:
            if f not in data:
                raise ServiceError(f"Missing required field: {f}")

        # Validate FK
        if not Patient.query.filter_by(id=data["patient_id"]).first():
            raise ServiceError("Invalid patient_id")

        if not Doctor.query.filter_by(id=data["doctor_id"]).first():
            raise ServiceError("Invalid doctor_id")

        if not Department.query.filter_by(id=data["department_id"]).first():
            raise ServiceError("Invalid department_id")

        # Convert appointment_date
        try:
            appt_date = datetime.fromisoformat(data["appointment_date"])
        except:
            raise ServiceError("Invalid date format. Use YYYY-MM-DDTHH:MM:SS")

        new_appt = Appointment(
            patient_id=data["patient_id"],
            doctor_id=data["doctor_id"],
            department_id=data["department_id"],
            appointment_date=appt_date,
            status=data["status"]
        )

        db.session.add(new_appt)
        db.session.commit()

        return new_appt

    # ----------------------------------------
    # UPDATE appointment
    # ----------------------------------------
    @staticmethod
    def update(data):
        appt = Appointment.query.filter_by(id=data.get("id")).first()
        if not appt:
            raise ServiceError(f"Appointment with id {data.get('id')} not found")

        # Update fields
        if "appointment_date" in data:
            try:
                appt.appointment_date = datetime.fromisoformat(data["appointment_date"])
            except:
                raise ServiceError("Invalid date format for appointment_date")

        appt.status = data.get("status", appt.status)
        appt.department_id = data.get("department_id", appt.department_id)
        appt.doctor_id = data.get("doctor_id", appt.doctor_id)
        appt.patient_id = data.get("patient_id", appt.patient_id)

        db.session.commit()
        return appt

    # ----------------------------------------
    # DELETE appointment
    # ----------------------------------------
    @staticmethod
    def delete_by_id(appointment_id):
        appt = Appointment.query.filter_by(id=appointment_id).first()
        if not appt:
            raise ServiceError(f"Appointment with id {appointment_id} not found")

        db.session.delete(appt)
        db.session.commit()
        return True

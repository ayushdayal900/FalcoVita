from backend.models import PatientHistory, Patient, Doctor, Department, Appointment
from backend.services.service_errors import ServiceError
from backend.extensions import db
from datetime import datetime

class PatientHistoryService:

    # ------------------------------------
    # GET history by ID
    # ------------------------------------
    @staticmethod
    def get_by_id(history_id):
        return PatientHistory.query.filter_by(id=history_id).first()

    # ------------------------------------
    # LIST all histories
    # ------------------------------------
    @staticmethod
    def get_all():
        histories = PatientHistory.query.all()
        if not histories:
            raise ServiceError("No patient histories found")
        return [h.to_dict() for h in histories]

    # ------------------------------------
    # GET all histories for a patient
    # ------------------------------------
    @staticmethod
    def get_by_patient(patient_id):
        from sqlalchemy.orm import joinedload
        histories = PatientHistory.query.options(
            joinedload(PatientHistory.prescriptions),
            joinedload(PatientHistory.doctor).joinedload(Doctor.user),
            joinedload(PatientHistory.department)
        ).filter_by(patient_id=patient_id).all()
        
        if not histories:
            # It's not necessarily an error if a patient has no history, just return empty list
            return []
        return [h.to_dict() for h in histories]

    # ------------------------------------
    # CREATE Patient History Entry
    # ------------------------------------
    @staticmethod
    def create(data):
        required = ["patient_id", "doctor_id", "department_id", "visit_type", "visit_date"]
        for field in required:
            if field not in data:
                raise ServiceError(f"Missing required field: {field}")

        # Validate patient
        if not Patient.query.filter_by(id=data["patient_id"]).first():
            raise ServiceError("Invalid patient_id")

        # Validate doctor
        if not Doctor.query.filter_by(id=data["doctor_id"]).first():
            raise ServiceError("Invalid doctor_id")

        # Validate department
        if not Department.query.filter_by(id=data["department_id"]).first():
            raise ServiceError("Invalid department_id")

        # Validate appointment (optional)
        appt_id = data.get("appointment_id")
        if appt_id and not Appointment.query.filter_by(id=appt_id).first():
            raise ServiceError("Invalid appointment_id")

        # Parse date
        visit_date_val = data["visit_date"]
        if isinstance(visit_date_val, str):
            try:
                visit_date_val = datetime.fromisoformat(visit_date_val)
            except:
                raise ServiceError("Invalid visit_date format (use YYYY-MM-DDTHH:MM:SS)")

        new_history = PatientHistory(
            patient_id=data["patient_id"],
            doctor_id=data["doctor_id"],
            department_id=data["department_id"],
            appointment_id=appt_id,
            visit_type=data["visit_type"],
            visit_date=visit_date_val,
            diagnosis=data.get("diagnosis", "")
        )

        db.session.add(new_history)
        db.session.commit()

        return new_history

    # ------------------------------------
    # UPDATE patient history
    # ------------------------------------
    @staticmethod
    def update(data):
        history = PatientHistory.query.filter_by(id=data.get("id")).first()
        if not history:
            raise ServiceError(f"History entry {data.get('id')} not found")

        if "visit_date" in data:
            date_val = data["visit_date"]
            if isinstance(date_val, str):
                date_val = datetime.fromisoformat(date_val)
            history.visit_date = date_val

        history.visit_type = data.get("visit_type", history.visit_type)
        history.diagnosis = data.get("diagnosis", history.diagnosis)
        history.appointment_id = data.get("appointment_id", history.appointment_id)

        db.session.commit()
        return history

    # ------------------------------------
    # DELETE Patient History
    # ------------------------------------
    @staticmethod
    def delete_by_id(history_id):
        history = PatientHistory.query.filter_by(id=history_id).first()
        if not history:
            raise ServiceError(f"History entry {history_id} not found")
        db.session.delete(history)
        db.session.commit()
        return True

from backend.models import Prescription, PatientHistory
from backend.extensions import db
from backend.services.service_errors import ServiceError


class PrescriptionService:

    # -------------------------------------------------------
    #   GET prescription by ID
    # -------------------------------------------------------
    @staticmethod
    def get_by_id(prescription_id):
        return Prescription.query.filter_by(id=prescription_id).first()

    # -------------------------------------------------------
    #   LIST prescriptions (all or filtered by history)
    # -------------------------------------------------------
    @staticmethod
    def get_all(history_id=None):
        if history_id:
            return [p.to_dict() for p in Prescription.query.filter_by(history_id=history_id).all()]

        prescriptions = Prescription.query.all()
        return [p.to_dict() for p in prescriptions]

    # -------------------------------------------------------
    #   CREATE Prescription
    # -------------------------------------------------------
    @staticmethod
    def create(data):

        required_fields = ["history_id", "medicines", "dosage"]

        for field in required_fields:
            if field not in data:
                raise ServiceError(f"Missing required field: {field}")

        # Validate history
        history = PatientHistory.query.filter_by(id=data["history_id"]).first()
        if not history:
            raise ServiceError(f"PatientHistory with ID {data['history_id']} does not exist")

        new_prescription = Prescription(
            history_id=data["history_id"],
            medicines=data["medicines"],
            dosage=data["dosage"],
            instructions=data.get("instructions")
        )

        db.session.add(new_prescription)
        db.session.commit()

        return new_prescription

    # -------------------------------------------------------
    #   DELETE Prescription
    # -------------------------------------------------------
    @staticmethod
    def delete_by_id(prescription_id):
        prescription = Prescription.query.filter_by(id=prescription_id).first()
        if not prescription:
            raise ServiceError(f"Prescription with id {prescription_id} not found")

        db.session.delete(prescription)
        db.session.commit()
        return True

    # -------------------------------------------------------
    #   UPDATE Prescription
    # -------------------------------------------------------
    @staticmethod
    def update(data):
        prescription = Prescription.query.filter_by(id=data.get("id")).first()
        if not prescription:
            raise ServiceError(f"Prescription with id {data.get('id')} not found")

        prescription.medicines = data.get("medicines", prescription.medicines)
        prescription.dosage = data.get("dosage", prescription.dosage)
        prescription.instructions = data.get("instructions", prescription.instructions)

        db.session.commit()
        return prescription

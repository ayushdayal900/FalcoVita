from backend.models import AvailabilitySlot, Doctor
from backend.services.service_errors import ServiceError
from backend.extensions import db
from datetime import datetime

class AvailabilitySlotService:

    # -----------------------------
    # GET SLOT BY ID
    # -----------------------------
    @staticmethod
    def get_by_id(slot_id):
        return AvailabilitySlot.query.filter_by(id=slot_id).first()

    # -----------------------------
    # LIST ALL SLOTS
    # -----------------------------
    @staticmethod
    def get_all():
        slots = AvailabilitySlot.query.all()
        if not slots:
            raise ServiceError("No availability slots found")
        return [slot.to_dict() for slot in slots]

    # -----------------------------
    # GET SLOTS FOR A SPECIFIC DOCTOR
    # -----------------------------
    @staticmethod
    def get_by_doctor(doctor_id):
        slots = AvailabilitySlot.query.filter_by(doctor_id=doctor_id).all()
        if not slots:
            raise ServiceError(f"No availability slots found for doctor {doctor_id}")
        return [slot.to_dict() for slot in slots]

    # -----------------------------
    # CREATE SLOT
    # -----------------------------
    @staticmethod
    def create(data):

        required = ["doctor_id", "available_date", "time_slot"]
        for field in required:
            if field not in data:
                raise ServiceError(f"Missing required field: {field}")

        # Validate doctor exists
        doctor = Doctor.query.filter_by(id=data["doctor_id"]).first()
        if not doctor:
            raise ServiceError("Invalid doctor_id")

        # Parse date
        date_val = data["available_date"]
        if isinstance(date_val, str):
            try:
                date_val = datetime.fromisoformat(date_val)
            except:
                raise ServiceError("Invalid available_date format. Use YYYY-MM-DDTHH:MM:SS")

        new_slot = AvailabilitySlot(
            doctor_id=data["doctor_id"],
            available_date=date_val,
            time_slot=data["time_slot"],
            status=data.get("status", "available")
        )

        db.session.add(new_slot)
        db.session.commit()

        return new_slot

    # -----------------------------
    # UPDATE SLOT
    # -----------------------------
    @staticmethod
    def update(data):
        slot = AvailabilitySlot.query.filter_by(id=data.get("id")).first()
        if not slot:
            raise ServiceError(f"Availability slot with id {data.get('id')} not found")

        if "available_date" in data:
            date_val = data["available_date"]
            if isinstance(date_val, str):
                date_val = datetime.fromisoformat(date_val)
            slot.available_date = date_val

        slot.time_slot = data.get("time_slot", slot.time_slot)
        slot.status = data.get("status", slot.status)

        db.session.commit()
        return slot

    # -----------------------------
    # DELETE SLOT
    # -----------------------------
    @staticmethod
    def delete_by_id(slot_id):
        slot = AvailabilitySlot.query.filter_by(id=slot_id).first()
        if not slot:
            raise ServiceError(f"Availability slot {slot_id} not found")

        db.session.delete(slot)
        db.session.commit()
        return True

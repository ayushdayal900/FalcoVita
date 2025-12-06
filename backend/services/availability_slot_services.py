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

    @staticmethod
    def create(data):
        """
        Create availability slot(s).
        
        Single slot mode (backward compatible):
        - Requires: doctor_id, available_date, time_slot
        
        Recurring weekly mode (new):
        - Requires: doctor_id, time_slot, days, weeks_ahead
        - days: array of day numbers (0=Sunday, 1=Monday, ..., 6=Saturday)
        - weeks_ahead: number of weeks to generate slots for
        """
        
        # Check if this is recurring mode (has 'days' field)
        if 'days' in data and isinstance(data['days'], list):
            return AvailabilitySlotService._create_recurring(data)
        
        # Single slot mode (original behavior)
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
    
    @staticmethod
    def _create_recurring(data):
        """
        Create multiple slots for recurring weekly pattern.
        
        Args:
            data: {
                doctor_id: int,
                time_slot: str (e.g., "13:00-14:00"),
                days: list[int] (e.g., [1, 3, 5] for Mon/Wed/Fri),
                weeks_ahead: int (default: 4),
                status: str (default: "available")
            }
        
        Returns:
            dict with created_count and first slot
        """
        from datetime import timedelta
        
        required = ["doctor_id", "time_slot", "days"]
        for field in required:
            if field not in data:
                raise ServiceError(f"Missing required field: {field}")
        
        # Validate doctor exists
        doctor = Doctor.query.filter_by(id=data["doctor_id"]).first()
        if not doctor:
            raise ServiceError("Invalid doctor_id")
        
        # Validate days array
        days = data["days"]
        if not days or not all(isinstance(d, int) and 0 <= d <= 6 for d in days):
            raise ServiceError("days must be an array of integers between 0-6 (0=Sunday, 6=Saturday)")
        
        weeks_ahead = data.get("weeks_ahead", 4)
        time_slot = data["time_slot"]
        status = data.get("status", "available")
        
        # Get start time from time_slot (e.g., "13:00" from "13:00-14:00")
        try:
            start_time_str = time_slot.split('-')[0].strip()
            hour, minute = map(int, start_time_str.split(':'))
        except:
            raise ServiceError("Invalid time_slot format. Use HH:MM-HH:MM (e.g., '13:00-14:00')")
        
        # Generate slots
        created_slots = []
        today = datetime.now().date()
        
        for week in range(weeks_ahead):
            for day_num in days:
                # Calculate the date for this day in this week
                days_until_target = (day_num - today.weekday() + 7) % 7
                if days_until_target == 0 and week == 0:
                    days_until_target = 7  # Skip today, start from next week
                
                target_date = today + timedelta(days=days_until_target + (week * 7))
                
                # Create datetime with the specified time
                slot_datetime = datetime.combine(target_date, datetime.min.time())
                slot_datetime = slot_datetime.replace(hour=hour, minute=minute)
                
                # Create the slot
                new_slot = AvailabilitySlot(
                    doctor_id=data["doctor_id"],
                    available_date=slot_datetime,
                    time_slot=time_slot,
                    status=status
                )
                
                db.session.add(new_slot)
                created_slots.append(new_slot)
        
        db.session.commit()
        
        # Return summary
        return {
            "created_count": len(created_slots),
            "first_slot": created_slots[0].to_dict() if created_slots else None,
            "message": f"Created {len(created_slots)} availability slots"
        }

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

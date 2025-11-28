from backend.models import Appointment, Patient, Doctor, Department
from backend.services.service_errors import ServiceError
from backend.extensions import db
from datetime import datetime, timedelta, timezone


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
        from sqlalchemy.orm import joinedload
        appointments = Appointment.query.options(
            joinedload(Appointment.patient).joinedload(Patient.user),
            joinedload(Appointment.doctor).joinedload(Doctor.user),
            joinedload(Appointment.department)
        ).all()
        if not appointments:
            raise ServiceError("No appointments found")
        return [a.to_dict() for a in appointments]

    # ----------------------------------------
    # GET doctor's upcoming appointments
    # ----------------------------------------
    @staticmethod
    def get_doctor_upcoming(doctor_id, time_range='week'):
        """
        Get upcoming appointments for a specific doctor
        
        Args:
            doctor_id: ID of the doctor
            time_range: 'today', 'week', or 'all'
        
        Returns:
            List of appointment dictionaries
        """
        from sqlalchemy.orm import joinedload
        
        # Base query - get scheduled appointments for this doctor
        now = datetime.now(timezone.utc)
        query = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status == 'scheduled',
            Appointment.appointment_date >= now
        )
        
        # Apply time range filter
        if time_range == 'today':
            # Get appointments for today only
            end_of_day = now.replace(hour=23, minute=59, second=59)
            query = query.filter(Appointment.appointment_date <= end_of_day)
        elif time_range == 'week':
            # Get appointments for the next 7 days
            end_of_week = now + timedelta(days=7)
            query = query.filter(Appointment.appointment_date <= end_of_week)
        # 'all' - no additional filter
        
        # Load related data and order by date
        appointments = query.options(
            joinedload(Appointment.patient).joinedload(Patient.user),
            joinedload(Appointment.doctor).joinedload(Doctor.user),
            joinedload(Appointment.department)
        ).order_by(Appointment.appointment_date.asc()).all()
        
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

        # Handle availability slot if provided
        availability_slot_id = data.get("availability_slot_id")
        if availability_slot_id:
            from backend.models import AvailabilitySlot
            slot = AvailabilitySlot.query.filter_by(id=availability_slot_id).first()
            if not slot:
                raise ServiceError("Invalid availability_slot_id")
            if slot.status == 'booked':
                raise ServiceError("This slot is already booked")
            # Mark slot as booked
            slot.status = 'booked'

        new_appt = Appointment(
            patient_id=data["patient_id"],
            doctor_id=data["doctor_id"],
            department_id=data["department_id"],
            appointment_date=appt_date,
            status=data["status"],
            availability_slot_id=availability_slot_id
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

        # Track old slot for potential release
        old_slot_id = appt.availability_slot_id
        new_status = data.get("status")
        new_slot_id = data.get("availability_slot_id")

        # Handle slot changes
        from backend.models import AvailabilitySlot
        
        # Release old slot if appointment is being cancelled
        if new_status == "cancelled" and old_slot_id:
            old_slot = AvailabilitySlot.query.filter_by(id=old_slot_id).first()
            if old_slot:
                old_slot.status = 'available'
            appt.availability_slot_id = None
        
        # Handle rescheduling (changing slot)
        elif new_slot_id and new_slot_id != old_slot_id:
            # Release old slot
            if old_slot_id:
                old_slot = AvailabilitySlot.query.filter_by(id=old_slot_id).first()
                if old_slot:
                    old_slot.status = 'available'
            
            # Book new slot
            new_slot = AvailabilitySlot.query.filter_by(id=new_slot_id).first()
            if not new_slot:
                raise ServiceError("Invalid availability_slot_id")
            if new_slot.status == 'booked':
                raise ServiceError("This slot is already booked")
            new_slot.status = 'booked'
            appt.availability_slot_id = new_slot_id

        # Update fields
        if "appointment_date" in data:
            try:
                appt.appointment_date = datetime.fromisoformat(data["appointment_date"])
            except:
                raise ServiceError("Invalid date format for appointment_date")

        if new_status == "completed" and appt.status != "completed":
            # Generate History and Prescription
            from backend.models import PatientHistory, Prescription
            
            diagnosis = data.get("diagnosis", "Routine Checkup (Auto-generated)")
            
            history = PatientHistory(
                patient_id=appt.patient_id,
                doctor_id=appt.doctor_id,
                department_id=appt.department_id,
                appointment_id=appt.id,
                visit_type="Consultation",
                visit_date=datetime.now(),
                diagnosis=diagnosis
            )
            db.session.add(history)
            db.session.flush() # Get ID

            prescription_data = data.get("prescription", {})
            medicines = prescription_data.get("medicines", "General Health Supplements")
            dosage = prescription_data.get("dosage", "1 tablet daily")
            instructions = prescription_data.get("instructions", "Take after meals")

            prescription = Prescription(
                history_id=history.id,
                medicines=medicines,
                dosage=dosage,
                instructions=instructions
            )
            db.session.add(prescription)

        appt.status = new_status if new_status else appt.status
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

        # Release the linked slot if exists
        if appt.availability_slot_id:
            from backend.models import AvailabilitySlot
            slot = AvailabilitySlot.query.filter_by(id=appt.availability_slot_id).first()
            if slot:
                slot.status = 'available'

        db.session.delete(appt)
        db.session.commit()
        return True

from backend.models import Appointment, Patient, Doctor, Department, Billing, Payment
from backend.services.service_errors import ServiceError
from backend.extensions import db
from datetime import datetime, timedelta


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
    def get_all(limit=None, offset=None, doctor_id=None, patient_id=None, status=None, start_date=None, end_date=None):
        from sqlalchemy.orm import joinedload
        query = Appointment.query.options(
            joinedload(Appointment.patient).joinedload(Patient.user),
            joinedload(Appointment.doctor).joinedload(Doctor.user),
            joinedload(Appointment.department)
        )
        
        if doctor_id:
            query = query.filter(Appointment.doctor_id == doctor_id)
        if patient_id:
            query = query.filter(Appointment.patient_id == patient_id)
        if status:
            query = query.filter(Appointment.status == status)
        if start_date:
            try:
                sd = datetime.fromisoformat(start_date)
                query = query.filter(Appointment.appointment_date >= sd)
            except ValueError:
                pass
        if end_date:
            try:
                ed = datetime.fromisoformat(end_date)
                query = query.filter(Appointment.appointment_date <= ed)
            except ValueError:
                pass
                
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
            
        appointments = query.all()
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

        # Handle Payment if provided
        if "payment_details" in data:
            payment_info = data["payment_details"]
            amount = float(payment_info.get("amount", 0))
            
            if amount > 0:
                # Create Booking/Bill
                # Create Booking/Bill
                is_pay_later = payment_info.get("method") == "Pay Later"
                bill_status = 'pending' if is_pay_later else 'paid'
                
                new_bill = Billing(
                    patient_id=data["patient_id"],
                    appointment_id=new_appt.id,
                    total_amount=amount,
                    due_date=datetime.now() + timedelta(days=7), # Due in 7 days
                    status=bill_status
                )
                db.session.add(new_bill)
                db.session.flush() # Get ID

                # Create Payment ONLY if not paying later
                if not is_pay_later:
                    new_payment = Payment(
                        billing_id=new_bill.id,
                        amount_paid=amount,
                        payment_method=payment_info.get("method", "Online"),
                        transaction_id=f"TXN-{int(datetime.now().timestamp())}",
                        payment_date=datetime.now()
                    )
                    db.session.add(new_payment)
                
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

        new_status = data.get("status")
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

        db.session.delete(appt)
        db.session.commit()
        return True

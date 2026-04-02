from backend.models import Billing, Payment, Patient, Appointment
from backend.extensions import db
from datetime import datetime, timezone
from backend.services.service_errors import ServiceError

class BillingService:
    @staticmethod
    def get_by_id(billing_id):
        return Billing.query.get(billing_id)

    
    @staticmethod
    def get_all():
        """Admin: Get all billing records with patient details."""
        return [b.to_dict() for b in Billing.query.order_by(Billing.created_at.desc()).all()]

    @staticmethod
    def get_by_patient(user_id):
        """Patient: Get bills for a specific user (via Patient record)."""
        patient = Patient.query.filter_by(id=user_id).first()
        if not patient:
            raise ServiceError("Patient record not found for this user.")
        
        return [b.to_dict() for b in Billing.query.filter_by(patient_id=patient.id).order_by(Billing.created_at.desc()).all()]

    @staticmethod
    def create_bill(data):
        """Admin/System: Create a new bill."""
        required = ['patient_id', 'total_amount', 'due_date']
        for r in required:
            if r not in data:
                raise ServiceError(f"Missing field: {r}")

        # Optional: Verify Appointment
        appt_id = data.get('appointment_id')
        if appt_id:
            if not Appointment.query.get(appt_id):
                 raise ServiceError("Invalid appointment ID")

        new_bill = Billing(
            patient_id=data['patient_id'],
            appointment_id=appt_id,
            total_amount=float(data['total_amount']),
            due_date=datetime.fromisoformat(data['due_date']),
            status='pending'
        )
        
        db.session.add(new_bill)
        db.session.commit()
        return new_bill

    @staticmethod
    def process_payment(billing_id, data):
        """Process a payment for a bill."""
        bill = Billing.query.get(billing_id)
        if not bill:
            raise ServiceError("Bill not found")
        
        if bill.status == 'paid':
             raise ServiceError("Bill is already fully paid.")

        amount = float(data.get('amount_paid', 0))
        if amount <= 0:
            raise ServiceError("Invalid payment amount")
            
        # Create Payment Record
        payment = Payment(
            billing_id=bill.id,
            amount_paid=amount,
            payment_method=data.get('payment_method', 'online'),
            transaction_id=f"TXN-{int(datetime.now().timestamp())}", # Mock transaction ID
            payment_date=datetime.now(timezone.utc)
        )
        db.session.add(payment)
        
        # Update Bill Status
        # Simple logic: if total paid >= total amount -> paid
        total_paid = sum([p.amount_paid for p in bill.payments]) + amount
        
        if total_paid >= bill.total_amount:
            bill.status = 'paid'
        else:
             bill.status = 'partial'
             
        db.session.commit()
        return payment

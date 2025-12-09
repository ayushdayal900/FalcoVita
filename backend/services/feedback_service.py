from backend.models import Feedback, Appointment, Doctor
from backend.services.service_errors import ServiceError
from backend.extensions import db
from sqlalchemy import func

class FeedbackService:
    @staticmethod
    def create(data):
        required_fields = ["appointment_id", "rating"]
        for f in required_fields:
            if f not in data:
                raise ServiceError(f"Missing required field: {f}")

        appt = Appointment.query.get(data["appointment_id"])
        if not appt:
            raise ServiceError("Appointment not found")
        
        if appt.status != 'completed':
            raise ServiceError("Feedback can only be given for completed appointments")
            
        # Check if already exists
        if Feedback.query.filter_by(appointment_id=data["appointment_id"]).first():
             raise ServiceError("Feedback already exists for this appointment")

        feedback = Feedback(
            appointment_id=appt.id,
            doctor_id=appt.doctor_id,
            patient_id=appt.patient_id,
            rating=int(data["rating"]),
            comment=data.get("comment", "")
        )
        db.session.add(feedback)
        db.session.commit()
        return feedback
        
    @staticmethod
    def get_all():
        return [f.to_dict() for f in Feedback.query.all()]

    @staticmethod
    def get_doctor_stats():
        """
        Returns average rating per doctor.
        """
        results = db.session.query(
            Feedback.doctor_id,
            func.avg(Feedback.rating).label('average_rating'),
            func.count(Feedback.id).label('review_count')
        ).group_by(Feedback.doctor_id).all()
        
        stats = []
        for r in results:
            doc = Doctor.query.get(r.doctor_id)
            stats.append({
                "doctor_id": r.doctor_id,
                "doctor_name": doc.user.name if doc and doc.user else "Unknown",
                "average_rating": round(float(r.average_rating), 1),
                "review_count": r.review_count
            })
            
        return stats

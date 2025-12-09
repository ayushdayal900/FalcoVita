from backend.extensions import db
from backend.models import (
    Doctor, Patient, Appointment, Department, 
    PatientHistory, Billing, Inventory, HospitalGoal
)
from sqlalchemy import func, case
from datetime import datetime, timedelta

class AnalyticsService:
    
    @staticmethod
    def get_dashboard_summary():
        """
        Global counts for dashboard badges
        """
        return {
            "doctor_count": Doctor.query.count(),
            "patient_count": Patient.query.count(),
            "appointment_count": Appointment.query.count(),
            "revenue": db.session.query(func.sum(Billing.total_amount)).filter_by(status='paid').scalar() or 0.0
        }

    @staticmethod
    def get_patient_demographics():
        """
        Gender and Age distribution
        """
        # Gender
        gender_stats = db.session.query(
            Patient.gender, func.count(Patient.id)
        ).group_by(Patient.gender).all()
        
        # Age
        # SQLite specific date diff logic or manual calculation
        # Since we load all for age calc usually, let's keep it simple or do logic here. 
        # For efficiency with massive scale we'd use SQL, but here iteration is fine for <1000 users.
        # But let's try to stick to SQL if possible or return raw DOBs.
        # Let's return counts by age group: 0-18, 19-35, 36-60, 60+
        patients = Patient.query.with_entities(Patient.dob).all()
        age_groups = {"0-18": 0, "19-35": 0, "36-60": 0, "60+": 0}
        
        now = datetime.now()
        for p in patients:
            if p.dob:
                # Naive age calc
                age = (now - p.dob.replace(tzinfo=None)).days // 365
                if age <= 18: age_groups["0-18"] += 1
                elif age <= 35: age_groups["19-35"] += 1
                elif age <= 60: age_groups["36-60"] += 1
                else: age_groups["60+"] += 1
                
        return {
            "gender_distribution": {g: c for g, c in gender_stats},
            "age_distribution": age_groups
        }

    @staticmethod
    def get_appointment_trends():
        """
        Appointments over last 7 days + status breakdown
        """
        # Status breakdown
        status_counts = db.session.query(
            Appointment.status, func.count(Appointment.id)
        ).group_by(Appointment.status).all()
        
        # Last 7 days trend
        today = datetime.now()
        seven_days_ago = today - timedelta(days=6)
        
        # SQLite date formatting
        trends = db.session.query(
            func.date(Appointment.appointment_date), func.count(Appointment.id)
        ).filter(Appointment.appointment_date >= seven_days_ago)\
         .group_by(func.date(Appointment.appointment_date)).all()
         
        return {
            "status_distribution": {s: c for s, c in status_counts},
            "weekly_trend": {d: c for d, c in trends}
        }

    @staticmethod
    def get_financial_analytics():
        """
        Revenue trends, unpaid balance
        """
        # Unpaid by patient (Top 5)
        top_unpaid = db.session.query(
            Billing.patient_id, func.sum(Billing.total_amount)
        ).filter(Billing.status.in_(['pending', 'overdue']))\
         .group_by(Billing.patient_id)\
         .order_by(func.sum(Billing.total_amount).desc())\
         .limit(10).all()
         
        unpaid_data = []
        for pid, amt in top_unpaid:
             pat = Patient.query.get(pid)
             name = pat.user.name if pat and pat.user else f"Unknown ({pid})"
             unpaid_data.append({"patient": name, "amount": amt})

        # Revenue Breakdown by Department (via Appointment)
        dept_revenue = db.session.query(
            Department.name, func.sum(Billing.total_amount)
        ).join(Appointment, Billing.appointment_id == Appointment.id)\
         .join(Department, Appointment.department_id == Department.id)\
         .filter(Billing.status == 'paid')\
         .group_by(Department.name).all()

        return {
            "top_unpaid_patients": unpaid_data,
            "department_revenue": {d: a for d, a in dept_revenue}
        }

    @staticmethod
    def get_inventory_status():
        """
        Low stock items + Category value
        """
        low_stock = Inventory.query.filter(Inventory.quantity <= Inventory.reorder_level).all()
        
        category_value = db.session.query(
            Inventory.category, func.sum(Inventory.quantity * Inventory.unit_price)
        ).group_by(Inventory.category).all()
        
        return {
            "low_stock_items": [i.to_dict() for i in low_stock],
            "category_value": {c: v for c, v in category_value}
        }

    @staticmethod
    def get_goals():
        return [g.to_dict() for g in HospitalGoal.query.all()]

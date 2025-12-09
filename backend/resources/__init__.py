from .auth_resource import auth_bp
from .doctors_resource import doctor_bp
from .patients_resource import patient_bp
from .appointment_resource import appointment_bp
from .availability_slots_resource import availability_bp
from .patient_history_resources import history_bp
from .prescription_resources import prescription_bp
from .admin_resource import admin_bp
from .department_resource import department_bp
from .export_resource import export_bp
from .chatbot import chatbot_bp
from .billing_resource import billing_bp
from .feedback_resource import feedback_bp

from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

__all__ = [
    "auth_bp",
    "api_bp",
    "api",
    "doctor_bp",
    "patient_bp",
    "appointment_bp",
    "availability_bp",
    "history_bp",
    "prescription_bp",
    "admin_bp",
    "department_bp",
    "export_bp",
    "chatbot_bp",
    "billing_bp",
    "feedback_bp",
    "analytics_bp"
]

from flask import Blueprint
from flask_restful import Api

# Define Analytics Blueprint separately to avoid circular imports or messy single-file logic
# Ideally this should be in analytics_resource.py but for consistency with others:
from .analytics_resource import (
    AnalyticsDashboardResource, AnalyticsDemographicsResource,
    AnalyticsAppointmentsResource, AnalyticsFinancialResource,
    AnalyticsInventoryResource, AnalyticsGoalsResource
)

analytics_bp = Blueprint('analytics_bp', __name__)
analytics_api = Api(analytics_bp)

analytics_api.add_resource(AnalyticsDashboardResource, '/api/analytics/dashboard')
analytics_api.add_resource(AnalyticsDemographicsResource, '/api/analytics/demographics')
analytics_api.add_resource(AnalyticsAppointmentsResource, '/api/analytics/appointments')
analytics_api.add_resource(AnalyticsFinancialResource, '/api/analytics/financial')
analytics_api.add_resource(AnalyticsInventoryResource, '/api/analytics/inventory')
analytics_api.add_resource(AnalyticsGoalsResource, '/api/analytics/goals')
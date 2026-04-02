from flask_restful import Resource
from flask_security import auth_required, roles_accepted
from backend.services.analytics_service import AnalyticsService

class AnalyticsDashboardResource(Resource):
    @auth_required('token', 'session')
    @roles_accepted('admin')
    def get(self):
        return AnalyticsService.get_dashboard_summary(), 200

class AnalyticsDemographicsResource(Resource):
    @auth_required('token', 'session')
    @roles_accepted('admin')
    def get(self):
        return AnalyticsService.get_patient_demographics(), 200

class AnalyticsAppointmentsResource(Resource):
    @auth_required('token', 'session')
    @roles_accepted('admin', 'doctor') # Maybe doctors can see trends
    def get(self):
        return AnalyticsService.get_appointment_trends(), 200

class AnalyticsFinancialResource(Resource):
    @auth_required('token', 'session')
    @roles_accepted('admin')
    def get(self):
        return AnalyticsService.get_financial_analytics(), 200

class AnalyticsInventoryResource(Resource):
    @auth_required('token', 'session')
    @roles_accepted('admin')
    def get(self):
        return AnalyticsService.get_inventory_status(), 200

class AnalyticsGoalsResource(Resource):
    @auth_required('token', 'session')
    @roles_accepted('admin')
    def get(self):
        return AnalyticsService.get_goals(), 200

from flask_restful import Resource
from backend.services.analytics_service import AnalyticsService

class AnalyticsDashboardResource(Resource):
    def get(self):
        return AnalyticsService.get_dashboard_summary(), 200

class AnalyticsDemographicsResource(Resource):
    def get(self):
        return AnalyticsService.get_patient_demographics(), 200

class AnalyticsAppointmentsResource(Resource):
    def get(self):
        return AnalyticsService.get_appointment_trends(), 200

class AnalyticsFinancialResource(Resource):
    def get(self):
        return AnalyticsService.get_financial_analytics(), 200

class AnalyticsInventoryResource(Resource):
    def get(self):
        return AnalyticsService.get_inventory_status(), 200

class AnalyticsGoalsResource(Resource):
    def get(self):
        return AnalyticsService.get_goals(), 200

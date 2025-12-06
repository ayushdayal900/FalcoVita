from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from flask_security import auth_required, current_user, roles_accepted
from backend.services.billing_service import BillingService
from backend.services.service_errors import ServiceError

billing_bp = Blueprint("billing_bp", __name__, url_prefix="/api/billing")
billing_api = Api(billing_bp)

class BillingListResource(Resource):
    @auth_required()
    def get(self):
        """Get all bills (Admin) or My Bills (Patient)"""
        try:
            if current_user.has_role('admin'):
                return BillingService.get_all(), 200
            elif current_user.has_role('patient'):
                return BillingService.get_by_patient(current_user.id), 200
            else:
                return {"message": "Unauthorized"}, 403
        except ServiceError as e:
             return {"message": str(e)}, 400

    @auth_required()
    @roles_accepted('admin')
    def post(self):
        """Create a new bill (Admin only)"""
        data = request.get_json()
        try:
            bill = BillingService.create_bill(data)
            return bill.to_dict(), 201
        except ServiceError as e:
            return {"message": str(e)}, 400

class PaymentResource(Resource):
    @auth_required()
    def post(self, billing_id):
        """Make a payment for a specific bill"""
        data = request.get_json()
        try:
            # In a real app, verify user owns this bill
            payment = BillingService.process_payment(billing_id, data)
            return payment.to_dict(), 201
        except ServiceError as e:
            return {"message": str(e)}, 400

billing_api.add_resource(BillingListResource, "/")
billing_api.add_resource(PaymentResource, "/<int:billing_id>/pay")

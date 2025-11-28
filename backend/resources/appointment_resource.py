from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from backend.services.appointment_services import AppointmentService
from backend.services.service_errors import ServiceError
from backend.extensions import cache
from backend.jwt_utils import token_required

appointment_bp = Blueprint("appointment_bp", __name__, url_prefix="/api/appointments")
appointment_api = Api(appointment_bp)

# ------------------------------------
# /api/appointments/<id>
# ------------------------------------
class AppointmentResource(Resource):
    method_decorators = [token_required]

    def get(self, id):
        appt = AppointmentService.get_by_id(id)
        if not appt:
            return {"message": "Appointment not found"}, 404
        return appt.to_dict(), 200

    def put(self, id):
        data = request.get_json()
        data["id"] = id
        try:
            updated = AppointmentService.update(data)
            return updated.to_dict(), 200
        except ServiceError as e:
            return {"message": str(e)}, 400

    def delete(self, id):
        try:
            AppointmentService.delete_by_id(id)
            return {"message": "Appointment deleted"}, 200
        except ServiceError as e:
            return {"message": str(e)}, 404


# ------------------------------------
# /api/appointments
# ------------------------------------
class AppointmentListResource(Resource):
    method_decorators = [token_required]

    def get(self):
        try:
            return AppointmentService.get_all(), 200
        except ServiceError as e:
            return {"message": str(e)}, 404

    def post(self):
        data = request.get_json()
        try:
            appt = AppointmentService.create(data)
            return appt.to_dict(), 201
        except ServiceError as e:
            return {"message": str(e)}, 400


# Register routes
appointment_api.add_resource(AppointmentListResource, "/")
appointment_api.add_resource(AppointmentResource, "/<int:id>")

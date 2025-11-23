from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from backend.services import AvailabilitySlotService, ServiceError

availability_bp = Blueprint("availability_bp", __name__, url_prefix="/api/availability")
availability_api = Api(availability_bp)


# ------------------------------------
# GET /api/availability/<id>
# PUT /api/availability/<id>
# DELETE /api/availability/<id>
# ------------------------------------
class AvailabilitySlotResource(Resource):
    def get(self, id):
        slot = AvailabilitySlotService.get_by_id(id)
        if not slot:
            return {"message": "Availability slot not found"}, 404
        return slot.to_dict(), 200

    def put(self, id):
        data = request.get_json()
        data["id"] = id
        try:
            updated = AvailabilitySlotService.update(data)
            return updated.to_dict(), 200
        except ServiceError as e:
            return {"message": str(e)}, 400

    def delete(self, id):
        try:
            AvailabilitySlotService.delete_by_id(id)
            return {"message": "Availability slot deleted"}, 200
        except ServiceError as e:
            return {"message": str(e)}, 404


# ------------------------------------
# GET /api/availability/
# POST /api/availability/
# ------------------------------------
class AvailabilitySlotListResource(Resource):
    def get(self):
        try:
            return AvailabilitySlotService.get_all(), 200
        except ServiceError as e:
            return {"message": str(e)}, 404

    def post(self):
        data = request.get_json()
        try:
            slot = AvailabilitySlotService.create(data)
            return slot.to_dict(), 201
        except ServiceError as e:
            return {"message": str(e)}, 400


# ------------------------------------
# GET /api/availability/doctor/<doctor_id>
# ------------------------------------
class AvailabilityByDoctorResource(Resource):
    def get(self, doctor_id):
        try:
            return AvailabilitySlotService.get_by_doctor(doctor_id), 200
        except ServiceError as e:
            return {"message": str(e)}, 404


# Register routes
availability_api.add_resource(AvailabilitySlotListResource, "/")
availability_api.add_resource(AvailabilitySlotResource, "/<int:id>")
availability_api.add_resource(AvailabilityByDoctorResource, "/doctor/<int:doctor_id>")

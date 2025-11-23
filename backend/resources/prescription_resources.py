from flask import Blueprint, request
from flask_restful import Resource, Api
from backend.services.prescription_services import PrescriptionService
from backend.services.service_errors import ServiceError

prescription_bp = Blueprint("prescription_bp", __name__, url_prefix="/api/prescriptions")
prescription_api = Api(prescription_bp)


# ----------------------------------------------------------
#   GET, PUT, DELETE prescription by ID
# ----------------------------------------------------------
class PrescriptionResource(Resource):

    def get(self, id):
        prescription = PrescriptionService.get_by_id(id)
        if not prescription:
            return {"message": "Prescription not found"}, 404
        return prescription.to_dict(), 200

    def put(self, id):
        data = request.get_json()
        data["id"] = id
        try:
            updated = PrescriptionService.update(data)
            return updated.to_dict(), 200
        except ServiceError as e:
            return {"message": str(e)}, 400

    def delete(self, id):
        try:
            PrescriptionService.delete_by_id(id)
            return {"message": "Prescription deleted"}, 200
        except ServiceError as e:
            return {"message": str(e)}, 404


# ----------------------------------------------------------
#   LIST + CREATE prescriptions
# ----------------------------------------------------------
class PrescriptionListResource(Resource):

    def get(self):
        history_id = request.args.get("history_id")  # optional filter
        data = PrescriptionService.get_all(history_id)
        return data, 200

    def post(self):
        data = request.get_json()
        try:
            prescription = PrescriptionService.create(data)
            return prescription.to_dict(), 201
        except ServiceError as e:
            return {"message": str(e)}, 400


# Register routes
prescription_api.add_resource(PrescriptionListResource, "/")
prescription_api.add_resource(PrescriptionResource, "/<int:id>")

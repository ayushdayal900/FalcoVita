from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from backend.services import PatientHistoryService, ServiceError

history_bp = Blueprint("history_bp", __name__, url_prefix="/api/history")
history_api = Api(history_bp)

# ------------------------------------
# GET /api/history/<id>
# PUT /api/history/<id>
# DELETE /api/history/<id>
# ------------------------------------
class PatientHistoryResource(Resource):
    def get(self, id):
        history = PatientHistoryService.get_by_id(id)
        if not history:
            return {"message": "History entry not found"}, 404
        return history.to_dict(), 200

    def put(self, id):
        data = request.get_json()
        data["id"] = id
        try:
            updated = PatientHistoryService.update(data)
            return updated.to_dict(), 200
        except ServiceError as e:
            return {"message": str(e)}, 400

    def delete(self, id):
        try:
            PatientHistoryService.delete_by_id(id)
            return {"message": "History entry deleted"}, 200
        except ServiceError as e:
            return {"message": str(e)}, 404


# ------------------------------------
# GET /api/history/
# POST /api/history/
# ------------------------------------
class PatientHistoryListResource(Resource):
    def get(self):
        try:
            return PatientHistoryService.get_all(), 200
        except ServiceError as e:
            return {"message": str(e)}, 404

    def post(self):
        data = request.get_json()
        try:
            history = PatientHistoryService.create(data)
            return history.to_dict(), 201
        except ServiceError as e:
            return {"message": str(e)}, 400


# ------------------------------------
# GET /api/history/patient/<patient_id>
# ------------------------------------
class PatientHistoryByPatientResource(Resource):
    def get(self, patient_id):
        try:
            return PatientHistoryService.get_by_patient(patient_id), 200
        except ServiceError as e:
            return {"message": str(e)}, 404


# Register routes
history_api.add_resource(PatientHistoryListResource, "/")
history_api.add_resource(PatientHistoryResource, "/<int:id>")
history_api.add_resource(PatientHistoryByPatientResource, "/patient/<int:patient_id>")

from flask import Blueprint, request
from flask_restful import Resource, Api
from backend.services import PatientService, ServiceError
from backend.extensions import cache

patient_bp = Blueprint("patient_bp", __name__, url_prefix="/api/patients")
patient_api = Api(patient_bp)


# --------------------------------------
#    GET / PUT / PATCH / DELETE
# --------------------------------------
# --------------------------------------
#    GET / PUT / PATCH / DELETE
# --------------------------------------
class PatientResource(Resource):
    def get(self, id):
        patient = PatientService.get_by_id(id)
        if not patient:
            return {"message": "Patient not found"}, 404
        return patient.to_dict(), 200

    def put(self, id):
        """Full update"""
        data = request.get_json()
        data["id"] = id

        try:
            updated_patient = PatientService.update(data)
            cache.delete_memoized(PatientListResource.get)
            return updated_patient.to_dict(), 200
        except ServiceError as e:
            return {"message": str(e)}, 400

    def patch(self, id):
        """Partial update"""
        data = request.get_json()
        data["id"] = id

        try:
            updated_patient = PatientService.update(data)
            cache.delete_memoized(PatientListResource.get)
            return updated_patient.to_dict(), 200
        except ServiceError as e:
            return {"message": str(e)}, 400

    def delete(self, id):
        try:
            PatientService.delete_by_id(id)
            cache.delete_memoized(PatientListResource.get)
            return {"message": "Patient deleted successfully"}, 200
        except ServiceError as e:
            return {"message": str(e)}, 404


# --------------------------------------
#   GET patient by email
# --------------------------------------
class PatientByEmailResource(Resource):
    def get(self, email):
        user = PatientService.get_by_email(email)
        if not user or not user.patient:
            return {"message": "Patient not found"}, 404
        return user.patient.to_dict(), 200


# --------------------------------------
#     LIST + CREATE
# --------------------------------------
class PatientListResource(Resource):

    @cache.cached(timeout=60, query_string=True)
    def get(self):
        """Get all patients or filter by doctor"""
        doctor_id = request.args.get('doctor_id')
        try:
            if doctor_id:
                patients = PatientService.get_patients_for_doctor(doctor_id)
            else:
                patients = PatientService.get_all()
            return patients, 200
        except ServiceError as e:
            return {"message": str(e)}, 404

    def post(self):
        """Create user + patient"""
        data = request.get_json()
        try:
            patient = PatientService.create(data)
            cache.delete_memoized(PatientListResource.get)
            return patient.to_dict(), 201
        except ServiceError as e:
            return {"message": str(e)}, 400


# --------------------------------------
#      REGISTER ROUTES
# --------------------------------------
patient_api.add_resource(PatientListResource, "/")
patient_api.add_resource(PatientResource, "/<int:id>")
patient_api.add_resource(PatientByEmailResource, "/email/<string:email>")

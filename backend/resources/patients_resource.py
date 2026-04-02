from flask import Blueprint, request
from flask_restful import Resource, Api
from flask_security import auth_required, roles_accepted, current_user
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
    @auth_required('token', 'session')
    def get(self, id):
        # Isolation: A patient can only view themselves
        if current_user.role == 'patient' and current_user.id != id:
            return {"message": "Forbidden"}, 403
            
        patient = PatientService.get_by_id(id)
        if not patient:
            return {"message": "Patient not found"}, 404
        return patient.to_dict(), 200

    @auth_required('token', 'session')
    @roles_accepted('admin', 'patient')
    def put(self, id):
        """Full update"""
        if current_user.role == 'patient' and current_user.id != id:
            return {"message": "Forbidden"}, 403
            
        data = request.get_json()
        data["id"] = id

        try:
            updated_patient = PatientService.update(data)
            cache.delete_memoized(PatientListResource.get)
            return updated_patient.to_dict(), 200
        except ServiceError as e:
            return {"message": str(e)}, 400

    @auth_required('token', 'session')
    @roles_accepted('admin', 'patient')
    def patch(self, id):
        """Partial update"""
        if current_user.role == 'patient' and current_user.id != id:
            return {"message": "Forbidden"}, 403
            
        data = request.get_json()
        data["id"] = id

        try:
            updated_patient = PatientService.update(data)
            cache.delete_memoized(PatientListResource.get)
            return updated_patient.to_dict(), 200
        except ServiceError as e:
            return {"message": str(e)}, 400

    @auth_required('token', 'session')
    @roles_accepted('admin')
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
    @auth_required('token', 'session')
    @roles_accepted('admin', 'doctor')
    def get(self, email):
        user = PatientService.get_by_email(email)
        if not user or not user.patient:
            return {"message": "Patient not found"}, 404
        return user.patient.to_dict(), 200


# --------------------------------------
#     LIST + CREATE
# --------------------------------------
class PatientListResource(Resource):

    @auth_required('token', 'session')
    @roles_accepted('admin', 'doctor')
    @cache.cached(timeout=60, query_string=True)
    def get(self):
        """Get all patients or filter by doctor"""
        doctor_id = request.args.get('doctor_id')
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int)
        search = request.args.get('search')
        
        # Isolation: A doctor should only see their own patients
        if current_user.role == 'doctor':
            doctor_id = current_user.id
            
        try:
            if doctor_id:
                patients = PatientService.get_patients_for_doctor(doctor_id, limit, offset, search)
            else:
                patients = PatientService.get_all(limit, offset, search)
            return patients, 200
        except ServiceError as e:
            return {"message": str(e)}, 404

    @auth_required('token', 'session')
    @roles_accepted('admin')
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

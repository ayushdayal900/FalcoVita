from flask import Blueprint, request
from flask_restful import Resource, Api
from flask_security import auth_required, roles_accepted, current_user
from backend.services import DoctorService, ServiceError
from backend.extensions import cache

doctor_bp = Blueprint("doctor_bp", __name__, url_prefix="/api/doctors")
doctor_api = Api(doctor_bp)


class DoctorResource(Resource):
    @auth_required('token', 'session')
    @cache.cached(timeout=300)
    def get(self, id):
        doctor = DoctorService.get_by_id(id)
        if not doctor:
            return {"message": "Doctor not found"}, 404
        return doctor.to_dict(), 200

    @auth_required('token', 'session')
    @roles_accepted('admin', 'doctor')
    def put(self, id):
        """Full update"""
        if current_user.role == 'doctor' and current_user.id != id:
            return {"message": "Forbidden"}, 403
            
        data = request.get_json()
        data["id"] = id

        try:
            updated_doctor = DoctorService.update(data)
            cache.delete_memoized(DoctorListResource.get)
            cache.delete_memoized(DoctorResource.get, id=id)
            return updated_doctor.to_dict(), 200
        except ServiceError as e:
            return {"message": str(e)}, 400

    @auth_required('token', 'session')
    @roles_accepted('admin', 'doctor')
    def patch(self, id):
        """Partial update"""
        if current_user.role == 'doctor' and current_user.id != id:
            return {"message": "Forbidden"}, 403
            
        data = request.get_json()
        data["id"] = id

        try:
            updated_doctor = DoctorService.update(data)
            cache.delete_memoized(DoctorListResource.get)
            cache.delete_memoized(DoctorResource.get, id=id)
            return updated_doctor.to_dict(), 200
        except ServiceError as e:
            return {"message": str(e)}, 400

    @auth_required('token', 'session')
    @roles_accepted('admin')
    def delete(self, id):
        try:
            DoctorService.delete_by_id(id)
            cache.delete_memoized(DoctorListResource.get)
            cache.delete_memoized(DoctorResource.get, id=id)
            return {"message": "Doctor deleted successfully"}, 200
        except ServiceError as e:
            return {"message": str(e)}, 404


# ---------------------------
# GET doctor by email
# ---------------------------
class DoctorByEmailResource(Resource):
    @auth_required('token', 'session')
    @roles_accepted('admin')
    def get(self, email):
        user = DoctorService.get_by_email(email)  # returns User
        if not user or not user.doctor:
            return {"message": "Doctor not found"}, 404

        return user.doctor.to_dict(), 200


# ---------------------------
# LIST + CREATE
# ---------------------------

# ---------------------------
# LIST + CREATE
# ---------------------------
class DoctorListResource(Resource):

    @auth_required('token', 'session')
    @cache.cached(timeout=60, query_string=True)
    def get(self):
        """Get all doctors"""
        try:
            include_blocked = request.args.get('include_blocked', 'false').lower() == 'true'
            department_id = request.args.get('department_id')
            limit = request.args.get('limit', type=int)
            offset = request.args.get('offset', type=int)
            search = request.args.get('search')
            
            doctors = DoctorService.get_all(
                include_blocked=include_blocked, 
                department_id=department_id,
                limit=limit,
                offset=offset,
                search=search
            )
            return doctors, 200
        except ServiceError as e:
            return {"message": str(e)}, 404

    @auth_required('token', 'session')
    @roles_accepted('admin')
    def post(self):
        """Create new doctor (user + doctor table)"""
        data = request.get_json()

        try:
            doctor = DoctorService.create(data)
            cache.delete_memoized(DoctorListResource.get)
            return doctor.to_dict(), 201
        except ServiceError as e:
            return {"message": str(e)}, 400


# ---------------------------
#   REGISTER ENDPOINTS
# ---------------------------
doctor_api.add_resource(DoctorListResource, "/")
doctor_api.add_resource(DoctorResource, "/<int:id>")
doctor_api.add_resource(DoctorByEmailResource, "/email/<string:email>")

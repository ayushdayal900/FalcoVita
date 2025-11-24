from flask import Blueprint, request
from flask_restful import Resource, Api
from backend.services import DoctorService, ServiceError
from backend.extensions import cache

doctor_bp = Blueprint("doctor_bp", __name__, url_prefix="/api/doctors")
doctor_api = Api(doctor_bp)


class DoctorResource(Resource):
    def get(self, id):
        doctor = DoctorService.get_by_id(id)
        if not doctor:
            return {"message": "Doctor not found"}, 404
        return doctor.to_dict(), 200

    def put(self, id):
        """Full update"""
        data = request.get_json()
        data["id"] = id

        try:
            updated_doctor = DoctorService.update(data)
            return updated_doctor.to_dict(), 200
        except ServiceError as e:
            return {"message": str(e)}, 400

    def patch(self, id):
        """Partial update"""
        data = request.get_json()
        data["id"] = id

        try:
            updated_doctor = DoctorService.update(data)
            return updated_doctor.to_dict(), 200
        except ServiceError as e:
            return {"message": str(e)}, 400

    def delete(self, id):
        try:
            DoctorService.delete_by_id(id)
            return {"message": "Doctor deleted successfully"}, 200
        except ServiceError as e:
            return {"message": str(e)}, 404


# ---------------------------
# GET doctor by email
# ---------------------------
class DoctorByEmailResource(Resource):
    def get(self, email):
        user = DoctorService.get_by_email(email)  # returns User
        if not user or not user.doctor:
            return {"message": "Doctor not found"}, 404

        return user.doctor.to_dict(), 200


# ---------------------------
# LIST + CREATE
# ---------------------------
class DoctorListResource(Resource):

    def get(self):
        """Get all doctors"""
        try:
            doctors = DoctorService.get_all()
            return doctors, 200
        except ServiceError as e:
            return {"message": str(e)}, 404

    def post(self):
        """Create new doctor (user + doctor table)"""
        data = request.get_json()

        try:
            doctor = DoctorService.create(data)
            return doctor.to_dict(), 201
        except ServiceError as e:
            return {"message": str(e)}, 400


# ---------------------------
#   REGISTER ENDPOINTS
# ---------------------------
doctor_api.add_resource(DoctorListResource, "/")
doctor_api.add_resource(DoctorResource, "/<int:id>")
doctor_api.add_resource(DoctorByEmailResource, "/email/<string:email>")

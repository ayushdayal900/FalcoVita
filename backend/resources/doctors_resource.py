from flask import request, jsonify
from flask_restful import Resource
from backend.services import DoctorService, ServiceError
from backend.models import Doctor
from backend.extensions import db

# /api/doctors/:id
class DoctorResource(Resource):
    def get(self, email):
        doctor = DoctorService.get_by_email(email)
        if not doctor:
            return jsonify({"message": "Doctor not found"}), 404
        return jsonify(doctor.to_dict())

    def get(self, id):
        doctor = DoctorService.get_by_id(id)
        if not doctor:
            return jsonify({"message": "Doctor not found"}), 404
        return jsonify(doctor.to_dict())





# /api/doctors  -> get method, post method
class DoctorListResource(Resource):
    def get(self):
        return jsonify(DoctorService.get_all())

from flask import Blueprint, request, jsonify, current_app as app
from flask_restful import Resource, Api


from backend.resources.auth_resource import auth_bp
from .doctors_resource import DoctorResource, DoctorListResource


api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

api.add_resource(DoctorResource, '/doctor/<int:id>', endpoint='doctor_by_id')
api.add_resource(DoctorResource, '/doctor/email/<string:email>', endpoint='doctor_by_email')


api.add_resource(DoctorListResource, '/doctors')
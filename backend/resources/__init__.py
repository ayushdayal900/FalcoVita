from flask import Blueprint, request, jsonify, current_app as app
from flask_restful import Resource, Api



from backend.resources.auth_resource import auth_bp


api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

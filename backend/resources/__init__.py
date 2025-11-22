from .auth_resource import auth_bp
from .doctors_resource import doctor_bp

from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

__all__ = [
    "auth_bp",
    "api_bp",
    "api",
    "doctor_bp"
]

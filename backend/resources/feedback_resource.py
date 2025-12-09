from flask import Blueprint, request
from flask_restful import Resource, Api
from backend.services.feedback_service import FeedbackService
from backend.services.service_errors import ServiceError

feedback_bp = Blueprint("feedback_bp", __name__, url_prefix="/api/feedback")
feedback_api = Api(feedback_bp)

class FeedbackResource(Resource):
    def post(self):
        data = request.get_json()
        try:
            feedback = FeedbackService.create(data)
            return feedback.to_dict(), 201
        except ServiceError as e:
            return {"message": str(e)}, 400

    def get(self):
        try:
            return FeedbackService.get_all(), 200
        except ServiceError as e:
            return {"message": str(e)}, 400

class FeedbackStatsResource(Resource):
    def get(self):
        try:
            return FeedbackService.get_doctor_stats(), 200
        except ServiceError as e:
            return {"message": str(e)}, 400

feedback_api.add_resource(FeedbackResource, "/")
feedback_api.add_resource(FeedbackStatsResource, "/stats")

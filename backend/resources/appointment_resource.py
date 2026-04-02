from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from flask_security import auth_required, roles_accepted, current_user
from backend.services.appointment_services import AppointmentService
from backend.services.service_errors import ServiceError
from backend.extensions import cache

appointment_bp = Blueprint("appointment_bp", __name__, url_prefix="/api/appointments")
appointment_api = Api(appointment_bp)

# ----------------------------------
# /api/appointments/<id>
# ----------------------------------
class AppointmentResource(Resource):
    @auth_required('token', 'session')
    def get(self, id):
        appt = AppointmentService.get_by_id(id)
        if not appt:
            return {"message": "Appointment not found"}, 404
            
        if current_user.role == 'patient' and appt.patient_id != current_user.id:
            return {"message": "Forbidden"}, 403
        if current_user.role == 'doctor' and appt.doctor_id != current_user.id:
            return {"message": "Forbidden"}, 403
            
        return appt.to_dict(), 200

    @auth_required('token', 'session')
    def put(self, id):
        appt = AppointmentService.get_by_id(id)
        if not appt:
            return {"message": "Appointment not found"}, 404
            
        if current_user.role == 'patient' and appt.patient_id != current_user.id:
            return {"message": "Forbidden"}, 403
        if current_user.role == 'doctor' and appt.doctor_id != current_user.id:
            return {"message": "Forbidden"}, 403
            
        data = request.get_json()
        data["id"] = id
        try:
            updated = AppointmentService.update(data)
            return updated.to_dict(), 200
        except ServiceError as e:
            return {"message": str(e)}, 400

    @auth_required('token', 'session')
    @roles_accepted('admin', 'patient')
    def delete(self, id):
        appt = AppointmentService.get_by_id(id)
        if not appt:
             return {"message": "Appointment not found"}, 404
             
        if current_user.role == 'patient' and appt.patient_id != current_user.id:
             return {"message": "Forbidden"}, 403
             
        try:
            AppointmentService.delete_by_id(id)
            return {"message": "Appointment deleted"}, 200
        except ServiceError as e:
            return {"message": str(e)}, 404


# ------------------------------------
# /api/appointments
# ------------------------------------
class AppointmentListResource(Resource):
    @auth_required('token', 'session')
    def get(self):
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int)
        doctor_id = request.args.get('doctor_id', type=int)
        patient_id = request.args.get('patient_id', type=int)
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Enforce limits based on role
        if current_user.role == 'patient':
            patient_id = current_user.id
        elif current_user.role == 'doctor':
            doctor_id = current_user.id

        try:
            return AppointmentService.get_all(limit, offset, doctor_id, patient_id, status, start_date, end_date), 200
        except ServiceError as e:
            return {"message": str(e)}, 404

    @auth_required('token', 'session')
    def post(self):
        data = request.get_json()
        
        if current_user.role == 'patient':
            data['patient_id'] = current_user.id
            
        try:
            appt = AppointmentService.create(data)
            return appt.to_dict(), 201
        except ServiceError as e:
            return {"message": str(e)}, 400


# Register routes
appointment_api.add_resource(AppointmentListResource, "/")
appointment_api.add_resource(AppointmentResource, "/<int:id>")

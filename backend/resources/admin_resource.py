from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from backend.services.admin_services import AdminService
from backend.services.service_errors import ServiceError

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/api/admin")
admin_api = Api(admin_bp)


# ------------------------------------
# GET /api/admin/dashboard
# ------------------------------------
class AdminDashboardResource(Resource):
    def get(self):
        """Get dashboard statistics"""
        try:
            from backend.models import User, Appointment
            
            total_doctors = User.query.filter_by(role='doctor').count()
            total_patients = User.query.filter_by(role='patient').count()
            total_appointments = Appointment.query.count()
            upcoming_appointments = Appointment.query.filter_by(status='scheduled').count()
            
            return {
                "total_doctors": total_doctors,
                "total_patients": total_patients,
                "total_appointments": total_appointments,
                "upcoming_appointments": upcoming_appointments
            }, 200
        except Exception as e:
            return {"message": str(e)}, 500


# ------------------------------------
# GET/POST /api/admin/doctors
# ------------------------------------
class AdminDoctorsResource(Resource):
    def get(self):
        """List all doctors"""
        try:
            return AdminService.get_all_doctors(), 200
        except ServiceError as e:
            return {"message": str(e)}, 404

    def post(self):
        """Create new doctor"""
        data = request.get_json()
        try:
            doctor = AdminService.create_doctor(data)
            return doctor.to_dict(), 201
        except ServiceError as e:
            return {"message": str(e)}, 400


# ------------------------------------
# GET/PUT/DELETE /api/admin/doctors/<id>
# ------------------------------------
class AdminDoctorResource(Resource):
    def get(self, id):
        from backend.models import Doctor
        doctor = Doctor.query.filter_by(id=id).first()
        if not doctor:
            return {"message": "Doctor not found"}, 404
        return doctor.to_dict(), 200

    def put(self, id):
        data = request.get_json()
        data['id'] = id
        try:
            doctor = AdminService.update_doctor(data)
            return doctor.to_dict(), 200
        except ServiceError as e:
            return {"message": str(e)}, 400

    def delete(self, id):
        try:
            AdminService.delete_doctor_by_id(id)
            return {"message": "Doctor deleted successfully"}, 200
        except ServiceError as e:
            return {"message": str(e)}, 404


# ------------------------------------
# GET/POST /api/admin/patients
# ------------------------------------
class AdminPatientsResource(Resource):
    def get(self):
        """List all patients"""
        try:
            return AdminService.get_all_patients(), 200
        except ServiceError as e:
            return {"message": str(e)}, 404

    def post(self):
        """Create new patient"""
        data = request.get_json()
        try:
            patient = AdminService.create_patient(data)
            return patient.to_dict(), 201
        except ServiceError as e:
            return {"message": str(e)}, 400


# ------------------------------------
# GET/PUT/DELETE /api/admin/patients/<id>
# ------------------------------------
class AdminPatientResource(Resource):
    def get(self, id):
        from backend.models import Patient
        patient = Patient.query.filter_by(id=id).first()
        if not patient:
            return {"message": "Patient not found"}, 404
        return patient.to_dict(), 200

    def put(self, id):
        data = request.get_json()
        data['id'] = id
        try:
            patient = AdminService.update_patient(data)
            return patient.to_dict(), 200
        except ServiceError as e:
            return {"message": str(e)}, 400

    def delete(self, id):
        try:
            AdminService.delete_patient_by_id(id)
            return {"message": "Patient deleted successfully"}, 200
        except ServiceError as e:
            return {"message": str(e)}, 404


# ------------------------------------
# GET /api/admin/search
# ------------------------------------
class AdminSearchResource(Resource):
    def get(self):
        """Search doctors and patients"""
        query = request.args.get('q', '')
        search_type = request.args.get('type', 'all')  # all, doctor, patient
        
        if not query:
            return {"message": "Query parameter required"}, 400
        
        from backend.models import User, Doctor, Patient
        
        results = {
            "doctors": [],
            "patients": []
        }
        
        if search_type in ['all', 'doctor']:
            doctors = User.query.filter(
                User.role == 'doctor',
                User.name.ilike(f'%{query}%')
            ).all()
            results['doctors'] = [u.to_dict() for u in doctors]
        
        if search_type in ['all', 'patient']:
            patients = User.query.filter(
                User.role == 'patient',
                User.name.ilike(f'%{query}%')
            ).all()
            results['patients'] = [u.to_dict() for u in patients]
        
        return results, 200


# ------------------------------------
# POST /api/admin/blacklist/<user_id>
# ------------------------------------
class AdminBlacklistResource(Resource):
    def post(self, user_id):
        """Blacklist a user"""
        from backend.models import User
        from backend.extensions import db
        
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {"message": "User not found"}, 404
        
        user.blacklisted = True
        db.session.commit()
        
        return {"message": f"User {user.name} blacklisted successfully"}, 200

    def delete(self, user_id):
        """Remove from blacklist"""
        from backend.models import User
        from backend.extensions import db
        
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {"message": "User not found"}, 404
        
        user.blacklisted = False
        db.session.commit()
        
        return {"message": f"User {user.name} removed from blacklist"}, 200


# Register routes
admin_api.add_resource(AdminDashboardResource, "/dashboard")
admin_api.add_resource(AdminDoctorsResource, "/doctors")
admin_api.add_resource(AdminDoctorResource, "/doctors/<int:id>")
admin_api.add_resource(AdminPatientsResource, "/patients")
admin_api.add_resource(AdminPatientResource, "/patients/<int:id>")
admin_api.add_resource(AdminSearchResource, "/search")
admin_api.add_resource(AdminBlacklistResource, "/blacklist/<int:user_id>")
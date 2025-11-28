from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from backend.services import PatientHistoryService, ServiceError
from backend.jwt_utils import token_required, role_required

history_bp = Blueprint("history_bp", __name__, url_prefix="/api/history")
history_api = Api(history_bp)

# ------------------------------------
# GET /api/history/<id>
# PUT /api/history/<id>
# DELETE /api/history/<id>
# ------------------------------------
class PatientHistoryResource(Resource):
    method_decorators = {
        'get': [token_required],
        'put': [role_required('admin', 'doctor'), token_required],
        'delete': [role_required('admin', 'doctor'), token_required]
    }
    
    def get(self, id):
        history = PatientHistoryService.get_by_id(id)
        if not history:
            return {"message": "History entry not found"}, 404
        return history.to_dict(), 200

    def put(self, id):
        data = request.get_json()
        data["id"] = id
        try:
            updated = PatientHistoryService.update(data)
            return updated.to_dict(), 200
        except ServiceError as e:
            return {"message": str(e)}, 400

    def delete(self, id):
        try:
            PatientHistoryService.delete_by_id(id)
            return {"message": "History entry deleted"}, 200
        except ServiceError as e:
            return {"message": str(e)}, 404


# ------------------------------------
# GET /api/history/
# POST /api/history/
# ------------------------------------
class PatientHistoryListResource(Resource):
    method_decorators = {
        'get': [token_required],
        'post': [role_required('admin', 'doctor'), token_required]
    }
    
    def get(self):
        try:
            return PatientHistoryService.get_all(), 200
        except ServiceError as e:
            return {"message": str(e)}, 404

    def post(self):
        data = request.get_json()
        try:
            history = PatientHistoryService.create(data)
            return history.to_dict(), 201
        except ServiceError as e:
            return {"message": str(e)}, 400


# ------------------------------------
# GET /api/history/patient/<patient_id>
# ------------------------------------
class PatientHistoryByPatientResource(Resource):
    method_decorators = [token_required]
    
    def get(self, patient_id):
        try:
            return PatientHistoryService.get_by_patient(patient_id), 200
        except ServiceError as e:
            return {"message": str(e)}, 404


class PatientHistoryExportResource(Resource):
    method_decorators = [token_required]
    
    def get(self, patient_id):
        from backend.models import PatientHistory, Prescription, Appointment, Patient
        from flask import make_response
        import csv
        import io
        
        try:
            # Verify patient exists
            patient = Patient.query.filter_by(id=patient_id).first()
            if not patient:
                return {"message": "Patient not found"}, 404
            
            # Get all history records
            histories = PatientHistory.query.filter_by(patient_id=patient_id).all()
            
            # Create CSV in memory
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow([
                'Patient ID',
                'Patient Name',
                'Medical Record Number',
                'Doctor Name',
                'Department',
                'Appointment Date',
                'Visit Type',
                'Diagnosis',
                'Medicines',
                'Dosage',
                'Instructions'
            ])
            
            # Write data
            for history in histories:
                appointment = Appointment.query.filter_by(id=history.appointment_id).first()
                prescriptions = Prescription.query.filter_by(history_id=history.id).all()
                
                # Combine all prescriptions
                medicines = '; '.join([p.medicines for p in prescriptions]) if prescriptions else 'N/A'
                dosages = '; '.join([p.dosage for p in prescriptions]) if prescriptions else 'N/A'
                instructions = '; '.join([p.instructions or '' for p in prescriptions]) if prescriptions else 'N/A'
                
                writer.writerow([
                    patient.id,
                    patient.user.name if patient.user else 'Unknown',
                    patient.medical_record_number,
                    history.doctor.user.name if history.doctor and history.doctor.user else 'Unknown',
                    history.department.name if history.department else 'Unknown',
                    appointment.appointment_date.strftime('%Y-%m-%d %H:%M') if appointment else 'N/A',
                    history.visit_type,
                    history.diagnosis or 'N/A',
                    medicines,
                    dosages,
                    instructions
                ])
            
            # Create response
            csv_content = output.getvalue()
            output.close()
            
            response = make_response(csv_content)
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = f'attachment; filename=patient_{patient_id}_history.csv'
            
            return response
            
        except Exception as e:
            return {"message": f"Export failed: {str(e)}"}, 500


# Register routes
history_api.add_resource(PatientHistoryListResource, "/")
history_api.add_resource(PatientHistoryResource, "/<int:id>")
history_api.add_resource(PatientHistoryByPatientResource, "/patient/<int:patient_id>")
history_api.add_resource(PatientHistoryExportResource, "/export/<int:patient_id>")

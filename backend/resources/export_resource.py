from flask import Blueprint, request, send_file
from flask_restful import Resource, Api
from backend.models import PatientHistory, Prescription, Patient, Doctor, Appointment
import csv
import io
from datetime import datetime

export_bp = Blueprint("export_bp", __name__, url_prefix="/api/export")
export_api = Api(export_bp)


class ExportPatientHistoryResource(Resource):
    def get(self, patient_id):
        """Export patient history as CSV"""
        
        # Verify patient exists
        patient = Patient.query.filter_by(id=patient_id).first()
        if not patient:
            return {"message": "Patient not found"}, 404
        
        # Get all history records with related data
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
            'Instructions',
            'Next Visit Suggested'
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
                instructions,
                'N/A'  # This would require additional field in model
            ])
        
        # Prepare file for download
        output.seek(0)
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'patient_{patient_id}_history_{datetime.now().strftime("%Y%m%d")}.csv'
        )


class ExportAllAppointmentsResource(Resource):
    def get(self):
        """Export all appointments as CSV (Admin only)"""
        
        appointments = Appointment.query.all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow([
            'Appointment ID',
            'Patient Name',
            'Doctor Name',
            'Department',
            'Date',
            'Status'
        ])
        
        for appt in appointments:
            writer.writerow([
                appt.id,
                appt.patient.user.name if appt.patient and appt.patient.user else 'Unknown',
                appt.doctor.user.name if appt.doctor and appt.doctor.user else 'Unknown',
                appt.department.name if appt.department else 'Unknown',
                appt.appointment_date.strftime('%Y-%m-%d %H:%M'),
                appt.status
            ])
        
        output.seek(0)
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'appointments_{datetime.now().strftime("%Y%m%d")}.csv'
        )


# Register routes
export_api.add_resource(ExportPatientHistoryResource, "/patient-history/<int:patient_id>")
export_api.add_resource(ExportAllAppointmentsResource, "/appointments")
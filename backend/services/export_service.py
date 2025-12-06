import csv
import io
import json
from backend.models import User, Appointment, Department, PatientHistory, Prescription
from backend.services.service_errors import ServiceError


class ExportService:

    # ---------------------------------------------------
    # EXPORT ANY QUERYSET AS CSV
    # ---------------------------------------------------
    @staticmethod
    def export_csv(data_list):
        if not data_list:
            raise ServiceError("No data available for export")

        output = io.StringIO()
        writer = None

        for item in data_list:
            if writer is None:
                # Write header once
                writer = csv.DictWriter(output, fieldnames=item.keys())
                writer.writeheader()
            writer.writerow(item)

        return output.getvalue()

    # ---------------------------------------------------
    # EXPORT ANY QUERYSET AS JSON
    # ---------------------------------------------------
    @staticmethod
    def export_json(data_list):
        if not data_list:
            raise ServiceError("No data available for export")
        return json.dumps(data_list, indent=4)


    # ---------------------------------------------------
    # SPECIFIC EXPORT RESOLVERS
    # ---------------------------------------------------
    @staticmethod
    def get_patients():
        patients = User.query.filter_by(role="patient").all()
        return [p.to_dict() for p in patients]

    @staticmethod
    def get_doctors():
        doctors = User.query.filter_by(role="doctor").all()
        return [d.to_dict() for d in doctors]

    @staticmethod
    def get_appointments():
        data = Appointment.query.all()
        return [a.to_dict() for a in data]

    @staticmethod
    def get_departments():
        data = Department.query.all()
        return [d.to_dict() for d in data]

    @staticmethod
    def get_histories():
        data = PatientHistory.query.all()
        return [h.to_dict() for h in data]

    @staticmethod
    def get_prescriptions():
        data = Prescription.query.all()
        return [p.to_dict() for p in data]

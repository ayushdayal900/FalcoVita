from backend.app import app
from backend.services.appointment_services import AppointmentService
from backend.services.service_errors import ServiceError
import traceback

def debug_create():
    with app.app_context():
        data = {
            "doctor_id": 62, 
            "department_id": 1,
            "patient_id": 12,
            "appointment_date": "2025-11-25T10:00:00.000Z",
            "status": "scheduled"
        }
        print(f"Attempting to create appointment with data: {data}")
        try:
            appt = AppointmentService.create(data)
            print(f"Success! Appointment created with ID: {appt.id}")
        except ServiceError as e:
            print(f"ServiceError: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    debug_create()

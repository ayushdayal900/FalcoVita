import requests
import time

BASE_URL = "http://localhost:5000/api"

def reproduce():
    session = requests.Session()
    try:
        # 1. Login as admin
        login_resp = session.post(f"{BASE_URL}/auth/login", json={
            "email": "admin@iitm.ac.in",
            "password": "Admin@123" 
        })
        if login_resp.status_code != 200:
            print("Failed to login as admin:", login_resp.text)
            return

        print("Logged in as admin.")
        
        timestamp = int(time.time())
        
        # 2. Create a dummy doctor
        doctor_email = f"delete_me_{timestamp}@hospital.com"
        doctor_data = {
            "name": f"Dr. Delete Me {timestamp}",
            "email": doctor_email,
            "password": "password",
            "department_id": 1, # Assuming dept 1 exists
            "specialization": "General",
            "experience": 5,
            "qualifications": "MBBS",
            "contact_number": "1234567890"
        }
        
        create_resp = session.post(f"{BASE_URL}/admin/doctors", json=doctor_data)
        if create_resp.status_code == 201:
            doctor_id = create_resp.json()['id']
            print(f"Created doctor with ID: {doctor_id}")
        else:
            print("Failed to create doctor:", create_resp.text)
            return

        # 3. Create a dummy patient
        patient_email = f"patient_delete_{timestamp}@hospital.com"
        patient_data = {
            "name": f"Patient For Delete {timestamp}",
            "email": patient_email,
            "password": "password",
            "dob": "1990-01-01",
            "contact": f"9{timestamp}", # unique contact
            "medical_record_number": f"MRN-{timestamp}",
            "doctor_id": doctor_id
        }
        
        create_pat_resp = session.post(f"{BASE_URL}/admin/patients", json=patient_data)
        if create_pat_resp.status_code == 201:
            patient_id = create_pat_resp.json()['id']
            print(f"Created patient with ID: {patient_id}")
        else:
            print("Failed to create patient:", create_pat_resp.text)
            return

        # 4. Create an appointment
        appt_data = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "department_id": 1,
            "appointment_date": "2025-12-25T10:00:00",
            "status": "scheduled"
        }
        
        appt_resp = session.post(f"{BASE_URL}/appointments/", json=appt_data)
        if appt_resp.status_code == 201:
            appt_id = appt_resp.json()['id']
            print(f"Created appointment with ID: {appt_id}")
        else:
            print("Failed to create appointment:", appt_resp.text)
            return

        # 5. Delete Doctor
        print(f"Attempting to delete doctor {doctor_id}...")
        delete_resp = session.delete(f"{BASE_URL}/admin/doctors/{doctor_id}")
        print(f"Delete response code: {delete_resp.status_code}")
        print(f"Delete response body: {delete_resp.text}")

        if delete_resp.status_code == 200:
            print("SUCCESS: Doctor deleted successfully.")
            
            # Verify appointment is also deleted
            check_appt = session.get(f"{BASE_URL}/appointments/{appt_id}")
            if check_appt.status_code == 404:
                print("SUCCESS: Appointment was cascade deleted.")
            else:
                print(f"FAILURE: Appointment still exists (Status: {check_appt.status_code})")
        else:
            print("FAILURE: Doctor deletion failed.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    reproduce()

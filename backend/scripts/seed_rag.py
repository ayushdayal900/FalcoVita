import os
import time

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

# Initialize local embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Pinecone
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

INDEX_NAME = "falcovita-rag"

# Get existing indexes
existing_indexes = [i.name for i in pc.list_indexes()]

# Delete old incompatible index if it exists
if INDEX_NAME in existing_indexes:
    print(f"Deleting old index: {INDEX_NAME}")
    pc.delete_index(INDEX_NAME)

# Create fresh index
print(f"Creating new index: {INDEX_NAME}")

pc.create_index(
    name=INDEX_NAME,
    dimension=384,  # all-MiniLM-L6-v2 embedding dimension
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

# Wait for Pinecone to initialize index
print("Waiting for index initialization...")
time.sleep(10)

# Connect to index
index = pc.Index(INDEX_NAME)

# Hospital knowledge documents
documents = [
    {
        "id": "dept-overview",
        "text": "FalcoVita coordinates specialized care across five primary departments: Cardiology, Neurology, Orthopedics, Dermatology, and Pediatrics. Each department is headed by board-certified specialists, manages its own doctor schedules, and tracks patient history logs in the SQLite database."
    },
    {
        "id": "dept-cardiology",
        "text": "The Cardiology department at FalcoVita treats heart and cardiovascular diseases including coronary artery disease, arrhythmias, and hypertension. Diagnostic procedures include Electrocardiograms (ECG), stress tests, and echocardiograms. Specialists: Dr. Sharma, Dr. Mehta, and others assigned by Admin."
    },
    {
        "id": "dept-neurology",
        "text": "The Neurology department manages disorders affecting the brain, spinal cord, and nervous system, including epilepsy, migraines, stroke, and neuropathic pain. High-resolution MRI and EEG scanning are utilized for diagnosis and patient evaluation."
    },
    {
        "id": "dept-orthopedics",
        "text": "The Orthopedics department addresses bone, joint, ligament, tendon, and muscle issues. Standard treatments cover fracture management, joint replacement surgeries, arthritis care, and physical rehabilitation programs. Specialists are assigned to handle sports injuries and degenerative joint conditions."
    },
    {
        "id": "dept-dermatology",
        "text": "The Dermatology department provides diagnostic and therapeutic services for skin, hair, and nail disorders, including acne, eczema, psoriasis, and skin oncology screening. Medical and minor surgical cosmetic procedures are performed in dedicated treatment rooms."
    },
    {
        "id": "dept-pediatrics",
        "text": "The Pediatrics department provides comprehensive medical care for infants, children, and adolescents up to age 18. Services include routine wellness checkups, childhood immunizations, developmental screenings, and acute illness treatment. All pediatric patient records require parent or legal guardian details linked during registration."
    },
    {
        "id": "role-admin",
        "text": "The Admin role has full system clearance in FalcoVita. Admins can view complete analytics dashboards (including system stats, patient demographics, and doctor performance), manage (create, update, delete) departments, assign doctors to departments, export all system logs as CSV files, and monitor scheduled Celery tasks."
    },
    {
        "id": "role-doctor",
        "text": "The Doctor role is for medical staff. Doctors can log into their private portal to view their upcoming appointment calendars, update their time slots, declare availability schedules, review patient medical history files, and write digital prescriptions during active patient consultations."
    },
    {
        "id": "role-patient",
        "text": "The Patient role is for registered patients. Patients can view their personal profiles, book appointments with doctors based on available slots, cancel or reschedule appointments within the allowed time window, view their medical records/prescriptions history, and check billing/payment status."
    },
    {
        "id": "admin-credentials",
        "text": "For development and testing purposes, the system is seeded with a default Admin account. Login Credentials: Username/Email: admin@iitm.ac.in, Password: Admin@123. The role is configured as 'admin' in the database and guarded by Flask-Security-Too."
    },
    {
        "id": "doctor-credentials",
        "text": "Default seeded doctors have login passwords set to 'doctor123'. Doctors can log in using their unique email generated during the seed database process. Their role is configured as 'doctor' in the user_roles table."
    },
    {
        "id": "patient-credentials",
        "text": "Default seeded patients have login passwords set to 'patient123'. Patients can log in using their unique email generated by the seed database script. Their role is configured as 'patient' and their profile is linked to an auto-generated Medical Record Number (MRN)."
    },
    {
        "id": "auth-flow",
        "text": "FalcoVita uses Flask-Security-Too for role-based authentication and authorization. On login, the backend verifies credentials, generates a secure session/token, and returns user details. The frontend (Vue.js 3 + Vuex) stores the authentication state and dynamically renders portal links based on the user's role."
    },
    {
        "id": "mrn-policy",
        "text": "Every patient registered at FalcoVita is assigned a unique Medical Record Number (MRN) to track all medical encounters. The MRN is auto-generated during registration in the format MRN-XXXXX (where X represents digits, e.g., MRN-12345). The MRN is permanent and cannot be altered by patients or doctors."
    },
    {
        "id": "appointment-booking",
        "text": "To book an appointment, patients log in, navigate to the Booking section, select a department, select an available doctor, and choose an open date/time slot from the doctor's AvailabilitySlot list. Once booked, the availability slot status is updated from 'available' to 'booked' in the database."
    },
    {
        "id": "appointment-cancellation",
        "text": "Appointments can be cancelled or rescheduled up to 24 hours in advance. If a patient cancels a booked appointment within this window, the slot is restored to 'available' status in the database, allowing other patients to book it, and a full refund status is logged."
    },
    {
        "id": "appointment-lateness",
        "text": "FalcoVita policy requires patients to arrive at least 10 minutes prior to their scheduled appointment time. This ensures vitals (blood pressure, temperature, heart rate) can be taken by the nursing staff before the doctor's consultation begins."
    },
    {
        "id": "reminders-workflow",
        "text": "Daily appointment reminders are automated in FalcoVita using Celery Beat. Every day, Celery Beat triggers a background task that queries the database for all appointments scheduled for the next day, compiles the details, and sends reminders via Google Chat webhooks and dummy SMTP emails."
    },
    {
        "id": "celery-redis",
        "text": "FalcoVita utilizes Celery as a distributed task queue and Redis as the message broker (typically on database 1). Celery workers run asynchronously to handle heavy tasks like sending notifications and generating reports, ensuring the main Flask application remains responsive."
    },
    {
        "id": "mailhog-testing",
        "text": "For email notifications, FalcoVita integrates Mailhog in the development environment. Outgoing emails are routed to localhost:1025 (SMTP port) and can be viewed using the Mailhog Web UI at http://localhost:8025. No real emails are sent, preventing accidental leaks."
    },
    {
        "id": "med-records",
        "text": "Medical history logs are captured in the PatientHistory table in the SQLite database. Each log entry is bound to a patient, doctor, and specific appointment, recording the visit type (Consultation or Follow-up), visit date, and clinical diagnosis."
    },
    {
        "id": "prescriptions-flow",
        "text": "When a doctor concludes an appointment, they log a diagnosis and generate a digital Prescription. The prescription is linked to the PatientHistory entry and contains details on medicines (e.g., Ibuprofen 400mg), exact dosage (e.g., 3 times/day), and specialized instructions (e.g., take after meals)."
    },
    {
        "id": "data-export",
        "text": "Admins and Patients can export historical records from the application. The system generates structured data downloads including appointment lists, diagnostic summaries, and prescription histories in CSV formats, complying with patient data accessibility guidelines."
    },
    {
        "id": "billing-payments",
        "text": "FalcoVita has a structured billing framework. Billing reports and payment status can be tracked under the Payments section. The system records invoice amounts and supports multiple payment streams: cash, card, and third-party health insurance."
    },
    {
        "id": "billing-status",
        "text": "Each medical invoice is assigned a state in the billing workflow: 'Pending' (invoice generated but unpaid), 'Paid' (payment cleared successfully), or 'Overdue' (payment window closed without clearance). Unpaid overdue invoices may restrict future non-emergency bookings."
    },
    {
        "id": "refund-policy",
        "text": "Refunds are processed automatically for appointments cancelled more than 24 hours before the slot time. Cancellations made less than 24 hours in advance are subject to a late cancellation fee, and the refunded amount is credited back to the original payment source."
    },
    {
        "id": "slots-status",
        "text": "Doctor schedules are governed by the AvailabilitySlot model, which contains a doctor_id, available_date, time_slot (e.g., '09:00-11:00'), and status ('available' or 'booked'). Doctors can manually add or delete slots through their portal."
    },
    {
        "id": "tech-frontend",
        "text": "The frontend is a Single Page Application (SPA) built using Vue.js 3, Vite, and Bootstrap 5. It uses Vuex for global state management (auth tokens, user profiles, booking states) and Chart.js for rendering analytics dashboards to Admins."
    },
    {
        "id": "tech-backend",
        "text": "The backend is built in Python using the Flask micro-framework. It leverages SQLAlchemy for database ORM, Flask-Security-Too for cryptography and role-based access, and Flask-RESTful to expose modular endpoints for the Vue frontend."
    },
    {
        "id": "database-sqlite",
        "text": "FalcoVita stores its data in an SQLite database file (`backend/db.db`). It contains tables for User, Role, UserRoles, Doctor, Patient, Department, Appointment, PatientHistory, Prescription, and AvailabilitySlot, which are automatically seeded using the seed_db script."
    },
    {
        "id": "faq-login-issues",
        "text": "FAQ - Login Issues: If you cannot log in, verify that your email format is correct and check that caps lock is off. For seeded test accounts, use 'admin@iitm.ac.in' with 'Admin@123', doctors with 'doctor123', or patients with 'patient123'. Ensure the backend Flask server is running."
    },
    {
        "id": "faq-password-reset",
        "text": "FAQ - Password Reset: Patients and doctors can request a password reset from the login screen. An automated recovery link will be sent to their registered email address, which is captured in development by the Mailhog dashboard at http://localhost:8025."
    },
    {
        "id": "faq-booking-errors",
        "text": "FAQ - Booking Errors: If an appointment slot does not appear, the doctor might not have declared availability for that date, or another patient may have already booked the slot. Refresh the page to see real-time slot statuses."
    },
    {
        "id": "faq-reminder-errors",
        "text": "FAQ - Google Chat Reminders: If reminders are not posting to your Google Chat space, verify that the `GOOGLE_CHAT_WEBHOOK_URL` in your `.env` file is valid, the Redis server is online, and the Celery Beat task scheduler is actively running."
    },
    {
        "id": "doctor-schedule-mgmt",
        "text": "Doctors manage their schedules by logging into the Doctor Portal and selecting 'My Slots'. They can select specific days of the week, input operational hours (e.g., '10:00-13:00'), and save. The system instantly generates corresponding AvailabilitySlot entries."
    },
    {
        "id": "triage-policy",
        "text": "While FalcoVita is an appointment-based hospital management system, emergency cases are routed immediately to the physical Triage unit of the hospital regardless of appointment status. Triage nurses assess severity levels, bypassing standard booking queues."
    },
    {
        "id": "intake-vitals",
        "text": "Before entering the doctor's cabin, the patient's vitals (blood pressure, heart rate, body temperature, respiratory rate) are recorded by an on-duty nurse. These vitals are logged under the pre-consultation notes and are visible to the consulting doctor."
    },
    {
        "id": "privacy-hipaa",
        "text": "FalcoVita enforces strict data privacy controls. Patient medical history, diagnoses, and prescriptions are private and encrypted. They can only be accessed by the patient themselves, their primary consulting doctor, and authorized system administrators."
    },
    {
        "id": "waitlist-policy",
        "text": "When all availability slots for a highly sought-after doctor are booked, patients can opt to join the digital Waitlist. If a booked patient cancels their appointment, the first patient on the waitlist is automatically notified via email to book the slot."
    },
    {
        "id": "telehealth-setup",
        "text": "FalcoVita supports virtual checkups. Telehealth consultation slots are marked with a video icon in the booking portal. Upon booking a telehealth slot, the patient and doctor receive an automated link containing the secure video conference room ID."
    },
    {
        "id": "lab-integration",
        "text": "Diagnostic and lab reports (blood works, radiology scans, pathology results) are uploaded directly to the database by lab technicians. Once uploaded, these reports are linked to the patient's MRN and appear on the patient's medical records portal."
    },
    {
        "id": "pharmacy-refills",
        "text": "Prescriptions generated in FalcoVita can be sent directly to the in-house pharmacy. Patients can request prescription refills online through their portal. The pharmacist receives the request, verifies the prescription validity, and flags it as 'ready for pickup'."
    },
    {
        "id": "visitor-guidelines",
        "text": "Hospital inpatient ward visiting hours are strictly restricted to 10:00 AM - 1:00 PM and 4:00 PM - 7:00 PM daily. A maximum of two visitors per patient is allowed at any given time to ensure a quiet, therapeutic environment for patient recovery."
    },
    {
        "id": "surgery-scheduling",
        "text": "Surgical procedures are scheduled exclusively by doctors or administrators. Operative slots require coordination between the surgeon, anesthesiologist, and operating room availability, and are logged under a specialized Surgery Booking calendar."
    },
    {
        "id": "pediatric-consent",
        "text": "In accordance with medical law, all patients under the age of 18 require parental or legal guardian consent for medical consultations and non-emergency surgical procedures. Guardian contact info and signatures are archived with the child's MRN."
    },
    {
        "id": "neurology-tests",
        "text": "Specialized neurological diagnostics, such as Electroencephalography (EEG) and electromyography (EMG), are scheduled through the Neurology department. These tests require a referral from a FalcoVita primary physician or neurologist."
    },
    {
        "id": "dermatology-procedures",
        "text": "The Dermatology clinic separates medical dermatology (eczema, melanoma screenings) from elective cosmetic procedures (laser therapies, chemical peels). Elective cosmetic procedures are not covered by standard insurance and require direct card or cash payment."
    },
    {
        "id": "cardiology-equipment",
        "text": "The Cardiology clinic features state-of-the-art diagnostic gear, including 12-lead Electrocardiogram (ECG) machines, holter monitors for continuous ambulatory cardiac recording, and high-resolution echocardiography systems for valvular heart assessment."
    },
    {
        "id": "orthopedics-therapy",
        "text": "Post-operative orthopedic patients are assigned to the Physical Therapy wing. Physical therapists coordinate recovery exercises for joint reconstruction, spinal injuries, and fractures, logging session progress notes directly into the patient's history timeline."
    },
    {
        "id": "outage-protocol",
        "text": "In the event of a network outage or database server down-time, hospital staff revert to offline paper charts to document patient consultations and administer medication. Once servers are restored, data is manually retrofitted into FalcoVita by the admin team."
    },
    {
        "id": "maintenance-backups",
        "text": "System maintenance is performed weekly on Sundays between 2:00 AM and 4:00 AM. During this period, automated database backups are compiled, encrypted, and uploaded to secure offline storage servers to prevent any potential data loss."
    }
]


# Generate embeddings and prepare vectors
vectors = []

for doc in documents:

    # Generate embedding
    embedding = model.encode(doc["text"]).tolist()

    vectors.append({
        "id": doc["id"],
        "values": embedding,
        "metadata": {
            "text": doc["text"]
        }
    })

# Upload vectors to Pinecone
print("Uploading vectors to Pinecone...")

index.upsert(vectors=vectors)

print(f"DONE: Seeded {len(vectors)} vectors into '{INDEX_NAME}'")
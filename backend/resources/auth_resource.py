from flask import Blueprint, request, jsonify
from backend.models import User, Doctor, Patient
from backend.extensions import db
from backend.jwt_utils import generate_token
from backend.password_utils import hash_password, verify_password
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


# ---------------------------------------------------
#                     LOGIN
# ---------------------------------------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return {"message": "Email and password are required"}, 400

    # Find user by email
    user = User.query.filter_by(email=email).first()

    if not user or not verify_password(password, user.password):
        return {"message": "Invalid credentials"}, 401

    if user.blacklisted or not user.active:
        return {"message": "Account is deactivated. Please contact support."}, 403

    # Generate JWT token
    token = generate_token(user.id, user.role, user.email, user.name)

    return {
        "message": "Login successful",
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "token": token
    }, 200


# ---------------------------------------------------
#                     REGISTER
# ---------------------------------------------------
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Base user fields
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    contact_number = data.get('contact_number')
    role = data.get('role')

    if not name or not email or not password or not role:
        return {"message": "Name, email, role and password are required"}, 400

    # Validate role
    if role not in ['admin', 'doctor', 'patient']:
        return {"message": "Invalid role. Must be admin, doctor, or patient"}, 400

    # Prevent duplicate email
    if User.query.filter_by(email=email).first():
        return {"message": "User with this email already exists"}, 409

    # Create USER with hashed password
    user = User(
        name=name,
        email=email,
        password=hash_password(password),
        contact_number=contact_number,
        role=role,
        active=True,
        blacklisted=False
    )
    db.session.add(user)
    db.session.commit()

    # ---------------------------------------------------
    #               DOCTOR REGISTRATION
    # ---------------------------------------------------
    if role == "doctor":
        department_id = data.get('department_id')
        specialization = data.get('specialization')
        qualifications = data.get('qualifications')
        experience = data.get('experience')

        if not (department_id and specialization and qualifications and experience):
            return {"message": "Missing doctor-specific fields"}, 400

        new_doctor = Doctor(
            id=user.id,
            department_id=department_id,
            specialization=specialization,
            qualifications=qualifications,
            experience=experience
        )

        db.session.add(new_doctor)
        db.session.commit()

    # ---------------------------------------------------
    #               PATIENT REGISTRATION
    # ---------------------------------------------------
    if role == "patient":
        dob = data.get('dob')
        contact = data.get('contact')
        doctor_id = data.get('doctor_id')

        if not (dob and contact):
            return {"message": "Missing patient-specific fields"}, 400

        # Convert DOB into datetime
        try:
            if isinstance(dob, str):
                dob = datetime.fromisoformat(dob)
        except:
            return {"message": "Invalid dob format. Use YYYY-MM-DD"}, 400

        import uuid
        medical_record_number = f"MRN-{str(uuid.uuid4())[:8].upper()}"

        new_patient = Patient(
            id=user.id,
            dob=dob,
            contact=contact,
            medical_record_number=medical_record_number,
            doctor_id=doctor_id
        )

        db.session.add(new_patient)
        db.session.commit()

    # ---------------------------------------------------
    #                    SUCCESS
    # ---------------------------------------------------
    return jsonify({
        "message": "User registered successfully",
        "id": user.id,
        "email": user.email,
        "role": user.role
    }), 201

import pytest
import os
import tempfile
from datetime import datetime, timezone
from backend.app import create_app
from backend.extensions import db, user_datastore
from backend.models import Role, User, Department, Doctor, Patient

@pytest.fixture(scope='session')
def app():
    # Setup temporary file for test SQLite database
    db_fd, db_path = tempfile.mkstemp()
    
    # Set environment variable so create_app() picks it up immediately
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    
    flask_app = create_app()
    flask_app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'CACHE_TYPE': 'NullCache',
        'SECURITY_PASSWORD_HASH': 'plaintext',
        'SECURITY_HASHING_SCHEMES': ['hex_md5'],
        'SECURITY_DEPRECATED_HASHING_SCHEMES': [],
    })

    with flask_app.app_context():
        db.create_all()
        # Seed roles
        admin_role = user_datastore.find_or_create_role(name='admin', description='Administrator')
        doctor_role = user_datastore.find_or_create_role(name='doctor', description='Doctor')
        patient_role = user_datastore.find_or_create_role(name='patient', description='Patient')
        
        # Create department
        dept = Department(name="Cardiology", overview="Cardiology Department")
        db.session.add(dept)
        db.session.commit()
        
        # Create users
        admin_user = user_datastore.create_user(
            name="Test Admin",
            email="admin@test.com",
            password="password",
            role="admin"
        )
        user_datastore.add_role_to_user(admin_user, admin_role)
        
        doc_user = user_datastore.create_user(
            name="Test Doctor",
            email="doctor@test.com",
            password="password",
            role="doctor"
        )
        user_datastore.add_role_to_user(doc_user, doctor_role)
        
        pat_user = user_datastore.create_user(
            name="Test Patient",
            email="patient@test.com",
            password="password",
            role="patient"
        )
        user_datastore.add_role_to_user(pat_user, patient_role)
        
        db.session.commit()
        
        # Add Doctor details
        doctor = Doctor(
            id=doc_user.id,
            department_id=dept.id,
            specialization="Cardiology",
            qualifications="MBBS, MD",
            experience=10
        )
        
        # Add Patient details
        patient = Patient(
            id=pat_user.id,
            dob=datetime(1990, 5, 20, tzinfo=timezone.utc),
            contact="9876543210",
            medical_record_number="MRN-887766"
        )
        
        db.session.add(doctor)
        db.session.add(patient)
        db.session.commit()

    yield flask_app

    # Clean up the temporary database file
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def db_session(app):
    with app.app_context():
        yield db.session
        db.session.rollback()


@pytest.fixture(scope='function', autouse=True)
def mock_cache(mocker):
    mocker.patch('backend.extensions.cache.delete_memoized', return_value=None)
    mocker.patch('backend.extensions.cache.delete', return_value=None)

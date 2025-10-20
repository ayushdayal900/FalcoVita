from app import app
from models import db

from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password

with app.app_context():
    datastore : SQLAlchemyUserDatastore = app.datastore
    admin_role = datastore.find_or_create_role(name='admin', description='Administrator with full access')
    doctor_role = datastore.find_or_create_role(name='doctor', description='Doctor with access to patient records')
    patient_role = datastore.find_or_create_role(name='patient', description='Patient with access to own records')

    if not datastore.find_user(email='admin@iitm.ac.in'):
        datastore.create_user(
            name='Admin User',
            email='admin@iitm.ac.in',
            password=hash_password('Admin@123'),
            role='admin',
            contact_number='1234567890',

            # fs_uniquifier='admin-uniquifier',
            active=True,
            roles=[admin_role]

        )

    if not datastore.find_user(email='dr1@iitm.ac.in'):
        datastore.create_user(
            name='Doctor',
            email='dr1@iitm.ac.in',
            password=hash_password('Dr1@123'),
            role='doctor',
            contact_number='1234567890',

            # fs_uniquifier='admin-uniquifier',
            active=False,
            roles=[doctor_role]

        )

    if not datastore.find_user(email='p01@iitm.ac.in'):
        datastore.create_user(
            name='patient',
            email='p01@iitm.ac.in',
            password=hash_password('p01@123'),
            role='patient',
            contact_number='1234567890',

            # fs_uniquifier='admin-uniquifier',
            active=False,
            roles=[patient_role]

        )



    try:
        db.session.commit()
        print("roles initialized")
    except:
        db.session.rollback()
        print("error while initializing roles")


    admin01 = datastore.find_user(email='admin@iitm.ac.in')
    dr01 = datastore.find_user(email='dr01@iitm.ac.in')
    p01 = datastore.find_user(email='p01@iitm.ac.in')

    admin_role = datastore.find_role('admin')
    doctor_role = datastore.find_role('doctor')
    patient_role = datastore.find_role('patient')

    datastore.add_role_to_user(admin01, admin_role)
    datastore.add_role_to_user(dr01, doctor_role)
    datastore.add_role_to_user(p01, patient_role)

    try:
        db.session.commit()
        print("roles assigned to users")
    except:
        db.session.rollback()
        print("error while assigning roles to users") 


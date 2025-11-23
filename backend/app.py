from flask import Flask
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

from backend.config import DevelopmentConfig
from backend.resources import auth_bp, api_bp, api, doctor_bp, patient_bp, appointment_bp, availability_bp, history_bp, prescription_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    app.config.from_object(DevelopmentConfig)
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SECURITY_CSRF_PROTECT_MECHANISMS"] = []
    app.config["SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'db.db')}"

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(availability_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(prescription_bp)
    


    # Initialize API
    api.init_app(app)

    # Database
    from backend.models import db, User, Role
    db.init_app(app)

    # Flask Security
    from backend.extensions import security
    from flask_security.datastore import SQLAlchemyUserDatastore
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore=datastore)
    app.datastore = datastore

    # Create DB tables
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run()

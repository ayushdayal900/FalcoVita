from flask import Flask
from dotenv import load_dotenv
import os

# Load .env
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

from backend.config import DevelopmentConfig, ProductionConfig
from backend.resources import (
    auth_bp, api_bp, api, doctor_bp, patient_bp, 
    appointment_bp, availability_bp, history_bp, prescription_bp, admin_bp, department_bp, export_bp, chatbot_bp,
    billing_bp, feedback_bp, analytics_bp
)


from celery import Celery

celery = Celery(
    "tasks",
    broker=os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.environ.get("REDIS_URL", "redis://localhost:6379/0")
)


# from backend.export_resource import export_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.route('/')
    def health_check():
        return {"status": "success", "message": "FalcoVita Backend is Live"}, 200
    
    if os.environ.get('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
        # Use DATABASE_URL if provided, else fallback to local sqlite
        if os.environ.get("DATABASE_URL"):
            app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
            if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
                app.config["SQLALCHEMY_DATABASE_URI"] = app.config["SQLALCHEMY_DATABASE_URI"].replace("postgres://", "postgresql://", 1)
        else:
            app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'db.db')}"

    app.config["SECURITY_REDIRECT_BEHAVIOR"] = "spa"
    app.config["SECURITY_FLASH_MESSAGES"] = False
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SECURITY_CSRF_PROTECT_MECHANISMS"] = []
    app.config["SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS"] = True

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(availability_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(prescription_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(department_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(billing_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(analytics_bp)

    # Initialize API
    api.init_app(app)

    # Database & Extensions
    from backend.models import User, Role
    from backend import extensions
    from flask_security import SQLAlchemyUserDatastore

    extensions.db.init_app(app)
    extensions.cache.init_app(app)

    # Setup Flask-Security
    extensions.user_datastore = SQLAlchemyUserDatastore(extensions.db, User, Role)
    extensions.security.init_app(app, extensions.user_datastore)

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
from flask import Flask, jsonify
from dotenv import load_dotenv
from backend.resources import auth_bp, api_bp, api
import os


# Load environment variables from .env file
load_dotenv()


from backend.config import DevelopmentConfig

def create_app():

    

    app = Flask(__name__)    

    # Configuration app settings
    app.config.from_object(DevelopmentConfig)
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECURITY_CSRF_PROTECT_MECHANISMS'] = []
    app.config['SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS'] = True

    
    # app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'db.db')}"



    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    
    api.init_app(app)

    # Database:  flask & flask sql alchemy
    from backend.models import db, User, Role, UserRoles, Doctor
    db.init_app(app)

    # Flask Security
    from backend.extensions import security
    from flask_security.datastore import SQLAlchemyUserDatastore
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore = datastore, )   #register_blueprint = False
    app.datastore = datastore

    # trial
    with app.app_context():
        db.create_all()

    return app

app = create_app()


if __name__ == "__main__":
    app.run()
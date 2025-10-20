from flask import Flask, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


from config import DevelopmentConfig

def create_app():

    

    app = Flask(__name__)    

    # Configuration app settings
    app.config.from_object(DevelopmentConfig)


    # Database:  flask & flask sql alchemy
    from models import db, User, Role, UserRoles, Doctor
    db.init_app(app)

    # Flask Security
    from extensions import security
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
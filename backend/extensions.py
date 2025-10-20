# file to instiantiate flask sqlalchemy and flask security

from flask_sqlalchemy import SQLAlchemy
from flask_security.core import Security

db = SQLAlchemy()
security = Security()
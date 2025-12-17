import os

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    basedir = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'db.db')}"
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", "dev-salt")

    # Redis & Celery
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    RESULT_BACKEND = "redis://localhost:6379/0"
    
    # Caching
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "redis://localhost:6379/1"
    CACHE_DEFAULT_TIMEOUT = 300
    
    # MailHog SMTP Configuration (for development/testing)
    MAIL_SERVER = os.environ.get("SMTP_SERVER", "localhost")
    MAIL_PORT = int(os.environ.get("SMTP_PORT", "1025"))
    MAIL_USE_TLS = os.environ.get("SMTP_USE_TLS", "False").lower() == "true"
    MAIL_USE_SSL = os.environ.get("SMTP_USE_SSL", "False").lower() == "true"
    MAIL_USERNAME = os.environ.get("SMTP_EMAIL", None)
    MAIL_PASSWORD = os.environ.get("SMTP_PASSWORD", None)
    MAIL_DEFAULT_SENDER = os.environ.get("SMTP_EMAIL", "noreply@hospital.com")
    
    # Google Chat Webhook (for notifications)
    GOOGLE_CHAT_WEBHOOK_URL = os.environ.get("GOOGLE_CHAT_WEBHOOK_URL", "")

    


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
    
    # Redis & Celery
    CELERY_BROKER_URL = os.environ.get("REDIS_URL")
    RESULT_BACKEND = os.environ.get("REDIS_URL")

    # Mail Config
    MAIL_SERVER = os.environ.get("SMTP_SERVER")
    MAIL_PORT = int(os.environ.get("SMTP_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("SMTP_EMAIL")
    MAIL_PASSWORD = os.environ.get("SMTP_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("SMTP_EMAIL")
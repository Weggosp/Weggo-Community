from app import app
from pathlib import Path
from dotenv import load_dotenv
import os

def Config(object):
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    SECRET_KEY = os.getenv('SECRET_KEY')

    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME="ceo@weggo.es"
    MAIL_PASSWORD=os.environ.get('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    ## AWS BUCKET CONFIGURATION
    S3_BUCKET = os.environ.get('S3_BUCKET')
    S3_LOCATION = os.environ.get('S3_LOCATION')
    S3_KEY = os.environ.get('S3_API_KEY')
    S3_SECRET = os.environ.get('S3_API_SECRET_KEY')

    # VARIABLES
    CSRF_ENABLED = None
    WTF_CSRF_ENABLED = None
    SESSION_COOKIE_SECURE = None
    SESSION_COOKIE_HTTPONLY = None
    SESSION_COOKIE_SAMESITE = None

    # SETTINGS BY DEFAULT
    DEBUG = True
    ENV = "development"
    OAUTHLIB_INSECURE_TRANSPORT = True

    ## DATABASE MONGO URI
    MONGO_URI=os.environ.get("DATABASE_LOCAL_URL")

    if object == 'deployment':
        ENV = "deployment"
        DEBUG = False
        CSRF_ENABLED = True
        WTF_CSRF_ENABLED = True

        ## SECRET KEYS
        STRIPE_PUBLIC_KEY=os.environ.get("STRIPE_REAL_API_PUBLIC_KEY")
        STRIPE_SECRET_KEY=os.environ.get("STRIPE_REAL_API_SECRET_KEY")

        ## DATABASE MONGO URI
        MONGO_URI=os.environ.get("DATABASE_REMOTE_URL")

        SESSION_COOKIE_SECURE = True
        SESSION_COOKIE_HTTPONLY = True
        SESSION_COOKIE_SAMESITE = 'NONE'
        
    elif object == 'testing':
        DEBUG = False

        ## DATABASE MONGO URI
        MONGO_URI=os.environ.get("DATABASE_TESTING_URL")

    ## APP UPDATING
    app.config.update(
        DEBUG=DEBUG,
        FLASK_ENV=ENV,
        FLASK_APP=os.environ.get('FLASK_APP'),
        SECRET_KEY=SECRET_KEY,
        MONGO_URI=MONGO_URI,
        CSRF_ENABLED=CSRF_ENABLED,
        WTF_CSRF_ENABLED=WTF_CSRF_ENABLED,
        MAIL_SERVER=MAIL_SERVER,
        MAIL_PORT=MAIL_PORT,
        MAIL_USE_TLS=MAIL_USE_TLS,
        MAIL_USERNAME=MAIL_USERNAME,
        MAIL_PASSWORD=MAIL_PASSWORD,
        MAIL_DEFAULT_SENDER=MAIL_DEFAULT_SENDER
    )
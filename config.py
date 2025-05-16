import os
from dotenv import load_dotenv
import secrets

# Load environment variables from .env file
load_dotenv()

# Get the absolute path of the directory where this file is located
basedir = os.path.abspath(os.path.dirname(__file__))
default_database_location = 'sqlite:///' + os.path.join(basedir, 'app.db')

class Config:
    # Require SECRET_KEY to be set in environment or .env file
    # In development, if not set, generate a random one (but warn)
    if not os.environ.get('SECRET_KEY'):
        if os.environ.get('FLASK_ENV') == 'production':
            raise ValueError("SECRET_KEY environment variable is not set. This is required in production.")
        else:
            print("WARNING: SECRET_KEY not set. Using a random key for this session only.")
            os.environ['SECRET_KEY'] = secrets.token_hex(16)
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or default_database_location
    SQLALCHEMY_TRACK_MODIFICATIONS = False
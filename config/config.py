import os

from datetime import timedelta
from dotenv import load_dotenv


class Config(object):
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    DEBUG = True
    DEVELOPMENT = True

    # Flask app Configuration
    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')

    # SQLAlchemy Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + os.getenv('NEURAL_USER') + ':' + os.getenv('NEURAL_KEY') + '@localhost/neuraldb'

    # Tests Configuration
    TESTS_URL = 'https://127.0.0.1:5000'

    # Mail Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    PRODUCTION_SERVER_IP = os.getenv('PRODUCTION_SERVER_IP')

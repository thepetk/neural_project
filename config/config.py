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

    # Constants - Fixed vaules for examples:
    ICON_SIDE_SIZE = 8
    ICON_MAX_LENGTH = ICON_SIDE_SIZE ** 2
    NETWORK_MAX_DEPTH = 6

    # Network settings
    BIAS = -1.8
    WEIGHT_LOW = 0.9
    WEIGHT_HIGH = 1.8

    # Basic settings of learning
    ERROR_THRESHOLD = 5.0
    INFLATION = 1.25
    DEFLATION = 0.8
    MIN_DESCENT_RATE = 0.00001
    MAX_DESCENT_RATE = 50.0
    MAX_ITERATIONS = 5000

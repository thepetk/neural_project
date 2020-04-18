import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

def create_app(**kwargs):
    app = Flask(__name__)
    app.config.from_object('config.Config')
    return app

app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

error_logger = logging.getLogger('log.error')
app.logger.handlers.extend(error_logger.handlers)

from app.routes import routes
import unittest
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from flask_cors import CORS
from app import db

login_manager = LoginManager()


class BaseTestClass(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__, instance_relative_config=True)

        self.app.secret_key = "test_secret"

        self.app.config[
            "SECRET_KEY"] = "1dafafghsdsf5378167ugfdsasdfghj98797781234741arfcshzgwffzgnssaerASXMHMRMDwefsrvs8945)(/%#"
        self.app.config['TESTING'] = True
        self.app.config['DEBUG'] = True
        self.app.config['APP_ENV'] = 'testing'
        self.app.config['WTF_CSRF_ENABLED'] = False

        CORS(self.app, supports_credentials=True)
        cors = CORS(resource={r"/*": {"origins": "*"}})

        login_manager.init_app(self.app)

        self.client = self.app.test_client()
        # Crea un contexto de aplicación
        with self.app.app_context():
            # Crea las tablas de la base de datos
            engie = create_engine(
                "mysql+pymysql://admin:tesis2022@database-1-tesis.cbzzayw2ryjl.us-east-1.rds.amazonaws.com/bd_tesis")
            Session = sessionmaker(bind=engie)
            #session = Session()
            Base = declarative_base()

    def tearDown(self):
        with self.app.app_context():
            pass

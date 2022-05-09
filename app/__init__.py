from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

application = Flask(__name__)
application.config["SECRET_KEY"] = "1dafafghsdsf5378167ugfdsasdfghj98797781234741arfcshzgwffzgnssaerASXMHMRMDwefsrvs8945)(/%#"
application.secret_key = "test_secret"
# CORS(app, supports_credentials=True)
# cors = CORS( resource={ r"/*": { "origins": "*" } } )
login_manager=LoginManager()
login_manager.init_app(application)


from app import web_service
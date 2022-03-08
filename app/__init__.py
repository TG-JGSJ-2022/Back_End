from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "test_secret"
CORS(app)

from app import web_service
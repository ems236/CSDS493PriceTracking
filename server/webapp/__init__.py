from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.config["CLIENT_ID"] = "421234127272-3bb34j7akcuuklsafvc6cuv757jd0870.apps.googleusercontent.com"
from server.webapp import routes
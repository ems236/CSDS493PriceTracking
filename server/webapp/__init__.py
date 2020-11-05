from flask import Flask

app = Flask(__name__)
app.config["CLIENT_ID"] = "421234127272-3bb34j7akcuuklsafvc6cuv757jd0870.apps.googleusercontent.com"
from server.webapp import routes
from flask import Flask

app = Flask(__name__)

from server.webapp import routes
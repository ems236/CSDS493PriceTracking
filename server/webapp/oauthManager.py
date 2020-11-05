from functools import wraps

from google.oauth2 import id_token
from google.auth.transport import requests
from flask import abort, request 

from server.webapp import app


def idForToken(request):
    if request.json is None or "token" not in request.json:
        abort(422)

    if app.config["IS_TEST"]:
        return "ems236@case.edu"

    token = request["token"]

    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), app.config["CLIENT_ID"])
        return idinfo['sub']
    except ValueError:
        abort(403)
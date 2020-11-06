from functools import wraps

from google.oauth2 import id_token
from google.auth.transport import requests
from flask import abort, request 

from server.webapp import app


def getAuthToken(request):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        #last item, sometimes the auth type isn't set and it's just a token
        return auth_header.split(" ")[-1]
    else:
        return None

def idForToken(request):
    token = getAuthToken(request)
    
    if token is None:
        if request.json is None: 
            abort(422)

        if "token" not in request.json:
            abort(403)

        token = request.json["token"]
        

    if app.config["IS_TEST"]:
        return "ems236@case.edu"

    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), app.config["CLIENT_ID"])
        return idinfo['sub']
    except ValueError:
        abort(403)
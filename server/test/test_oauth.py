import pytest
import json

from werkzeug.exceptions import HTTPException
#pytest --cov-config=.coveragerc --cov-report term-missing --cov=server --pdb
from server.webapp import app
from server.webapp.oauthManager import idForToken 

class MockRequest():
    def __init__(self, json, headers):
        self.json = json
        self.headers = headers

@pytest.fixture
def api():
    app.config["IS_TEST"] = False
    yield app

def test_no_json(api):
    try:
        idForToken(MockRequest(None, {}))
    except HTTPException as e:
        assert e.get_response().status_code == 422

#OAM-3
def test_no_token(api):
    try:
        idForToken(MockRequest({"id": 1}, {}))
    except HTTPException as e:
        assert e.get_response().status_code == 403

#OAM-2
def test_invalid_token(api):
    try:
        idForToken(MockRequest({"token": "hello"}, {}))
        assert False
    except HTTPException as e:
        assert e.get_response().status_code == 403


#Note: with current infrastructure you can't get an id token from the webserver
#you can paste one here and run the test
#OAM-1
def test_valid_token(api):
    TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImYwOTJiNjEyZTliNjQ0N2RlYjEwNjg1YmI4ZmZhOGFlNjJmNmFhOTEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI0MjEyMzQxMjcyNzItM2JiMzRqN2FrY3V1a2xzYWZ2YzZjdXY3NTdqZDA4NzAuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MjEyMzQxMjcyNzItM2JiMzRqN2FrY3V1a2xzYWZ2YzZjdXY3NTdqZDA4NzAuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTgxMzIzOTM0NjQ0OTYwMjg3ODQiLCJoZCI6ImNhc2UuZWR1IiwiZW1haWwiOiJlbXMyMzZAY2FzZS5lZHUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibm9uY2UiOiJmdzFwdmFiYmxvbndicG04b2E0dTIiLCJuYW1lIjoiRWxsaXMgU2F1cGUiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDUuZ29vZ2xldXNlcmNvbnRlbnQuY29tLy1JNnpZcWVfWnNnVS9BQUFBQUFBQUFBSS9BQUFBQUFBQUFBQS9BTVp1dWNtWFpYc0x6WHA3Z3NfelhlRFBkWUVuOVA5T0RRL3M5Ni1jL3Bob3RvLmpwZyIsImdpdmVuX25hbWUiOiJFbGxpcyIsImZhbWlseV9uYW1lIjoiU2F1cGUiLCJsb2NhbGUiOiJlbiIsImlhdCI6MTYwNDU5OTcyNywiZXhwIjoxNjA0NjAzMzI3LCJqdGkiOiI1NWYzZjFiMTcwNmRmM2FmNTNlNWZmMmViNjE3NzU3MGJkNGNhYzhkIn0.eeWIzjjrRCgifTXBeZ8lblysBJ_7xJv-Z9xUUv1nPfWHLeUithtEXKD4YdCgUYhOODt0sHDjfKBMj_vfXh9mEFNahtW2GEpLVLZN3R0hY3w88YOI2ljsbT-eN_oegRlZBKDoVQdN76pivHV25gfxVY_cZyt04zxXs4_MZKA4Mq0pCgRaLS-ZCEtWn4Vgu8bpFg80g30aseIEi2OQtBlAymHRC07_YLCQ6iP6IQfDgiK7oxVgk3GEvvDx7l3FrAf0btM5B3kDmuQPdiUL6oLspIsPJOowtuntgS7KXWIKSMOqnFMqOhQncTE4TkAfpl8acmIwQ5rw1zUPbNpbIxHiCA"
    try:
        id = idForToken(MockRequest({"token": TOKEN}, {}))
        assert len(id) > 0 
    except HTTPException:
        assert False
    
    try:
        id = idForToken(MockRequest(None, {"Authorization": "Bearer " + TOKEN}))
        assert len(id) > 0 
    except HTTPException:
        assert False


import pytest
import json

from werkzeug.exceptions import HTTPException
#pytest --cov-report term-missing --cov=server --pdb
from server.webapp import app
from server.webapp.oauthManager import idForToken 

class MockRequest():
    def __init__(self, json):
        self.json = json

@pytest.fixture
def api():
    app.config["IS_TEST"] = False
    yield app

def test_no_json(api):
    try:
        idForToken(MockRequest(None))
    except HTTPException as e:
        assert e.get_response().status_code == 422

def test_no_token(api):
    try:
        idForToken(MockRequest({"id": 1}))
    except HTTPException as e:
        assert e.get_response().status_code == 403

def test_invalid_token(api):
    try:
        idForToken(MockRequest({"token": "hello"}))
        assert False
    except HTTPException as e:
        assert e.get_response().status_code == 403


#Note: with current infrastructure you can't get an id token from the webserver
#you can paste one here and run the test
def test_valid_token(api):
    TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImYwOTJiNjEyZTliNjQ0N2RlYjEwNjg1YmI4ZmZhOGFlNjJmNmFhOTEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI0MjEyMzQxMjcyNzItM2JiMzRqN2FrY3V1a2xzYWZ2YzZjdXY3NTdqZDA4NzAuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MjEyMzQxMjcyNzItM2JiMzRqN2FrY3V1a2xzYWZ2YzZjdXY3NTdqZDA4NzAuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTgxMzIzOTM0NjQ0OTYwMjg3ODQiLCJoZCI6ImNhc2UuZWR1IiwiZW1haWwiOiJlbXMyMzZAY2FzZS5lZHUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibm9uY2UiOiJmdzFwdmFiYmxvbndicG04b2E0dTIiLCJuYW1lIjoiRWxsaXMgU2F1cGUiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDUuZ29vZ2xldXNlcmNvbnRlbnQuY29tLy1JNnpZcWVfWnNnVS9BQUFBQUFBQUFBSS9BQUFBQUFBQUFBQS9BTVp1dWNtWFpYc0x6WHA3Z3NfelhlRFBkWUVuOVA5T0RRL3M5Ni1jL3Bob3RvLmpwZyIsImdpdmVuX25hbWUiOiJFbGxpcyIsImZhbWlseV9uYW1lIjoiU2F1cGUiLCJsb2NhbGUiOiJlbiIsImlhdCI6MTYwNDU5NTg3NywiZXhwIjoxNjA0NTk5NDc3LCJqdGkiOiI4NzFiNmE3NDI5YjYzZjc5MjlmODlkOTNhNGY2ZDc5Yjc0ZTU5N2E5In0.Hg3paz4eEW2tLDvRodsEhSSrVt9lKjLytEkhX80ttLqQpNnaszBZTKI8LaFi09vYhg_V36e6YlCAE7pfpD694d3M85ec_FC_1L3ul7LfbZAXlUE4FW7kxDybN2_R5sdGID2bZ0wwAGtW7NklwkB6EH82N6jUwaQtC6mcHl4R3GEt0OjpsPktfdiM5l9QF3mIs9WdOiyoQbxclFlIAI2fDEEo5x8KAbZf1L144lNgs-tVzx1Gkvou9DFdShj3bF4nC9Ebv8vDhSNPs3B0hryp1zfex1bnSgePcMJCb8XeXpJZG2kCeYF1t3OcYBscU3V-dmGC3_ijd-dx_ZSeKocRgQ"
    try:
        id = idForToken(MockRequest({"token": TOKEN}))
        assert len(id) > 0 
    except HTTPException:
        assert False
    


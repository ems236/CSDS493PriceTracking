import pytest
#pytest --cov-report term-missing --cov=server --pdb
from server.webapp import app

@pytest.fixture
def api():
    yield app

@pytest.fixture
def client(api):
    return api.test_client()

def test_hello(client):
    res = client.get("/hello")
    assert res.status_code == 200
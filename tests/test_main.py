import pytest
from app.main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200     # now returns HTML page

def test_api(client):
    response = client.get("/api")
    assert response.status_code == 200

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200

def test_about(client):
    response = client.get("/about")
    assert response.status_code == 200
import pytest
from app.main import app

# This sets up a test client to simulate browser requests
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# Test 1 - Check home page works
def test_home(client):
    response = client.get("/")
    assert response.status_code == 200

# Test 2 - Check health page works
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200

# Test 3 - Check about page works
def test_about(client):
    response = client.get("/about")
    assert response.status_code == 200
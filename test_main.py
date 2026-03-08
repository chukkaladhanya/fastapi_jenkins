from fastapi.testclient import TestClient
from main import app

test_app = TestClient(app)

def test_valid():
    response = test_app.get("/details")
    assert response.status_code == 200

    response = test_app.get("/female")
    assert response.status_code == 200

def test_invalid():
    response = test_app.get("/m")
    assert response.status_code == 400
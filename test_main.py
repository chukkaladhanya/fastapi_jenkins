from fastapi.testclient import TestClient
from main import app

test_app = TestClient(app)

def test_valid():
    response = test_app.get("/details")
    assert response.status_code == 200

    response = test_app.get("/students/female")
    assert response.status_code == 200

    response = test_app.get("/details?sort_by=age")
    assert response.status_code == 200


def test_invalid():
    response = test_app.get("/students/m")
    assert response.status_code == 400

    response = test_app.get("/s")
    assert response.status_code == 404

    response = test_app.get("/details?sort_by=name")
    assert response.status_code == 400

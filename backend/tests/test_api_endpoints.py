import pytest


def test_health_check_endpoint(api_client):
    response = api_client.get("/")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "online"


def test_swagger_docs_endpoint(api_client):
    response = api_client.get("/docs")
    assert response.status_code == 200


def test_auth_login_validation(api_client):
    response = api_client.post("/api/v1/auth/login", data={"username": "invalid_user", "password": "wrong_password"})
    assert response.status_code in [401, 400, 422]

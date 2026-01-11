from fastapi.testclient import TestClient
from app.api.http import app

client = TestClient(app)

def get_auth_headers(email: str):
    response = client.post(
        "/token",
        data = {
            "username": email,
            "password": "ignored"
        }
    )
    token = response.json()["access_token"]
    return {
        "Authorization": f"Bearer {token}"
    }

def test_create_user_authentication():
    headers = get_auth_headers("tester@email.com")

    response1 = client.post(
        "/users",
        json = {
            "email": "apiuser@email.com"
        },
        headers=headers
    )

    assert response1.status_code == 201
    assert response1.json()["email"] == "apiuser@email.com"

def test_create_user_requires_authentication():
    response2 = client.post(
        "/users",
        json = {
            "email": "blocked@email.com"
        }
    )

    assert response2.status_code == 401

def test_create_duplicate_user_returns_409():
    headers = get_auth_headers("tester2@email.com")

    client.post(
        "/users", 
        json = {
            "email": "dup@example.com"
        }, 
        headers = headers    
    )

    response3 = client.post(
        "/users", 
        json = {
            "email": "dup@example.com"
        }, 
        headers = headers
    )

    assert response3.status_code == 409
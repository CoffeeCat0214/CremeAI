import pytest
from fastapi.testclient import TestClient
import json

def test_auth_token_generation(test_client):
    response = test_client.post("/auth/token", params={
        "platform": "test",
        "api_key": "test-api-key"
    })
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "bearer" in response.json()["token_type"].lower()

def test_auth_token_invalid_api_key(test_client):
    response = test_client.post("/auth/token", params={
        "platform": "test",
        "api_key": "wrong-key"
    })
    
    assert response.status_code == 401
    assert "error" in response.json()
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"

def test_chat_endpoint_authorized(test_client, auth_headers):
    response = test_client.post(
        "/chat",
        headers=auth_headers,
        json={
            "message": "Hello!",
            "platform": "test"
        }
    )
    
    assert response.status_code == 200
    assert "response" in response.json()

def test_chat_endpoint_unauthorized(test_client):
    response = test_client.post(
        "/chat",
        json={
            "message": "Hello!",
            "platform": "test"
        }
    )
    
    assert response.status_code == 401
    assert "error" in response.json()

def test_rate_limiting(test_client, auth_headers):
    # Make multiple requests quickly
    for _ in range(61):  # Exceed the 60 requests per minute limit
        response = test_client.post(
            "/chat",
            headers=auth_headers,
            json={
                "message": "Hello!",
                "platform": "test"
            }
        )
    
    assert response.status_code == 429
    assert "error" in response.json()
    assert response.json()["error"]["code"] == "RATE_LIMIT_EXCEEDED" 
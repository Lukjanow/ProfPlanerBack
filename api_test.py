import pytest
from fastapi.testclient import TestClient
from API import app  # import your FastAPI app

# Setup TestClient for FastAPI
client = TestClient(app)

# Test for the index route
def test_index():
    response = client.get("/room")
    assert response.status_code == 400
    #assert "items" in response.json()
    # Some Changes to test the CI/CD pipeline

# Trigger CI/CD

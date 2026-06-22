"""Tests for the API endpoints."""

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_match_endpoint_validation():
    """Empty payloads should be rejected."""
    response = client.post("/match", json={"resume_text": "short", "jd_text": "short"})
    assert response.status_code == 422  # validation error


def test_rank_requires_resumes():
    response = client.post(
        "/rank",
        json={"jd_text": "Looking for a Python developer with ML experience.", "resumes": []},
    )
    assert response.status_code == 422

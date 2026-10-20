from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_reports_version_and_db_state():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] in ("ok", "degraded")
    assert body["version"]
    assert body["db"] in ("up", "down", "not_configured")


def test_request_id_is_echoed():
    r = client.get("/health", headers={"X-Request-ID": "test-123"})
    assert r.headers["X-Request-ID"] == "test-123"


def test_request_id_is_generated_when_absent():
    r = client.get("/health")
    assert len(r.headers["X-Request-ID"]) >= 32

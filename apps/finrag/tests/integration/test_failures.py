"""One test per row of docs/failure-modes.md (written in the harden milestone).
F9 is the only row that exists today."""

from app.main import app
from fastapi.testclient import TestClient


def test_f9_db_down_reports_degraded_not_500(monkeypatch):
    from app import config

    monkeypatch.setattr(config.settings, "database_url", "postgresql://nobody@127.0.0.1:1/x")
    monkeypatch.setattr(config.settings, "db_health_timeout_s", 1)
    r = TestClient(app).get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "degraded", "version": r.json()["version"], "db": "down"}

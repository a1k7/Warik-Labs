from fastapi.testclient import TestClient

from app.main import app


def test_liveness_probe_is_public_and_does_not_require_providers() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "alive", "service": "warik-labs-api"}

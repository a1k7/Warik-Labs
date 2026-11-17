from fastapi.testclient import TestClient

from app.api import companion as companion_api
from app.main import app


def test_chat_endpoint_returns_local_companion_response_without_provider_key(monkeypatch) -> None:
    monkeypatch.setattr(companion_api.settings, "groq_api_key", None)
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/companion/chat",
            json={"message": "Hey Warik, help me think through my day."},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["provider"] == "local"
    assert body["provider_status"] in {"not_configured", "fallback"}
    assert body["mission"] is None
    assert body["reply"]


def test_chat_endpoint_returns_a_grocery_mission_and_no_execution_claim(monkeypatch) -> None:
    monkeypatch.setattr(companion_api.settings, "groq_api_key", None)
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/companion/chat",
            json={"message": "Order 2 litres milk from Blinkit"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["mission"]["intent"] == "grocery"
    assert body["mission"]["state"] == "not_executable"
    assert "No external action was executed" in body["safety_note"]


def test_chat_endpoint_rejects_blank_messages(monkeypatch) -> None:
    monkeypatch.setattr(companion_api.settings, "groq_api_key", None)
    with TestClient(app) as client:
        response = client.post("/api/v1/companion/chat", json={"message": "   "})

    assert response.status_code == 422

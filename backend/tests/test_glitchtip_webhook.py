import pytest

from backend.config import get_settings
from backend.main import create_app


@pytest.fixture
def webhook_env(monkeypatch):
    monkeypatch.setenv("TELEGRAM_ALARM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TELEGRAM_ALARM_CHAT_ID", "404674868")
    monkeypatch.setenv("GLITCHTIP_WEBHOOK_SECRET", "expected-secret")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def client(webhook_env):
    from fastapi.testclient import TestClient

    return TestClient(create_app())


def test_webhook_disabled_without_telegram(monkeypatch):
    monkeypatch.setenv("TELEGRAM_ALARM_BOT_TOKEN", "")
    monkeypatch.setenv("TELEGRAM_ALARM_CHAT_ID", "")
    monkeypatch.setenv("GLITCHTIP_ALERT_EMAIL_TO", "")
    monkeypatch.setenv("SMTP_HOST", "")
    get_settings.cache_clear()

    app = create_app()
    paths = [getattr(r, "path", "") for r in app.routes]
    assert "/webhooks/glitchtip" not in paths
    assert "/webhooks/glitchtip/email" not in paths
    get_settings.cache_clear()


def test_webhook_forbidden_wrong_secret(client):
    response = client.post(
        "/webhooks/glitchtip?secret=wrong",
        json={"text": "alert"},
    )
    assert response.status_code == 403


def test_webhook_probe_returns_ok(client):
    response = client.get("/webhooks/glitchtip?secret=expected-secret")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_webhook_sends_to_telegram(client, monkeypatch):
    calls: list[tuple[str, str, str]] = []

    def fake_send(token: str, chat_id: str, text: str) -> None:
        calls.append((token, chat_id, text))

    monkeypatch.setattr("backend.glitchtip_webhook.send_telegram", fake_send)

    response = client.post(
        "/webhooks/glitchtip?secret=expected-secret",
        json={
            "attachments": [
                {
                    "title": "Test error",
                    "title_link": "https://eu.glitchtip.com/issues/1",
                    "text": "details",
                }
            ]
        },
    )

    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert len(calls) == 1
    assert calls[0][0] == "test-token"
    assert calls[0][1] == "404674868"
    assert "Test error" in calls[0][2]

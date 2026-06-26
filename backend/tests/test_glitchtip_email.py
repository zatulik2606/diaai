import pytest
from email.message import EmailMessage

from backend.config import get_settings
from backend.glitchtip_email import alert_subject, send_alert_email
from backend.main import create_app


@pytest.fixture
def email_env(monkeypatch):
    monkeypatch.setenv("GLITCHTIP_ALERT_EMAIL_TO", "alerts@example.com")
    monkeypatch.setenv("GLITCHTIP_ALERT_EMAIL_FROM", "diaai@example.com")
    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SMTP_USER", "smtp-user")
    monkeypatch.setenv("SMTP_PASSWORD", "smtp-pass")
    monkeypatch.setenv("GLITCHTIP_WEBHOOK_SECRET", "expected-secret")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def client(email_env):
    from fastapi.testclient import TestClient

    return TestClient(create_app())


def test_alert_subject_from_attachment():
    subject = alert_subject(
        {"attachments": [{"title": "ValueError: bad input", "text": "details"}]}
    )
    assert subject == "GlitchTip: ValueError: bad input"


def test_send_alert_email_ssl(monkeypatch):
    monkeypatch.setenv("GLITCHTIP_ALERT_EMAIL_TO", "alerts@example.com")
    monkeypatch.setenv("GLITCHTIP_ALERT_EMAIL_FROM", "diaai@example.com")
    monkeypatch.setenv("SMTP_HOST", "smtp.yandex.ru")
    monkeypatch.setenv("SMTP_PORT", "465")
    monkeypatch.setenv("SMTP_USER", "smtp-user")
    monkeypatch.setenv("SMTP_PASSWORD", "smtp-pass")
    monkeypatch.setenv("SMTP_USE_TLS", "false")
    get_settings.cache_clear()
    settings = get_settings()
    sent: list[EmailMessage] = []

    class FakeSMTPSSL:
        def __init__(self, host, port, timeout=15):
            self.port = port

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def login(self, user, password):
            assert user == settings.smtp_user

        def send_message(self, message):
            sent.append(message)

    monkeypatch.setattr("backend.glitchtip_email.smtplib.SMTP_SSL", FakeSMTPSSL)

    send_alert_email(settings, "GlitchTip: test", "body text")
    assert len(sent) == 1
    get_settings.cache_clear()


def test_send_alert_email(email_env, monkeypatch):
    settings = get_settings()
    sent: list[EmailMessage] = []

    class FakeSMTP:
        def __init__(self, host, port, timeout=15):
            self.host = host

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def starttls(self):
            return None

        def login(self, user, password):
            assert user == settings.smtp_user

        def send_message(self, message):
            sent.append(message)

    monkeypatch.setattr("backend.glitchtip_email.smtplib.SMTP", FakeSMTP)

    send_alert_email(settings, "GlitchTip: test", "body text")
    assert len(sent) == 1
    assert sent[0]["To"] == "alerts@example.com"
    assert sent[0]["Subject"] == "GlitchTip: test"
    assert sent[0].get_content() == "body text\n"


def test_email_webhook_probe(client):
    response = client.get("/webhooks/glitchtip/email?secret=expected-secret")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_email_webhook_sends(client, monkeypatch):
    calls: list[tuple[str, str]] = []

    def fake_send(settings, subject, body):
        calls.append((subject, body))

    monkeypatch.setattr("backend.glitchtip_webhook.send_alert_email", fake_send)

    response = client.post(
        "/webhooks/glitchtip/email?secret=expected-secret",
        json={
            "attachments": [
                {
                    "title": "RuntimeError: boom",
                    "title_link": "https://eu.glitchtip.com/issues/1",
                    "text": "stack trace",
                }
            ]
        },
    )

    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert len(calls) == 1
    assert "RuntimeError" in calls[0][0]
    assert "stack trace" in calls[0][1]

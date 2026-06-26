"""GlitchTip alert delivery via SMTP (hosted GlitchTip has no custom email)."""

from __future__ import annotations

import smtplib
from email.message import EmailMessage

import httpx

from backend.config import Settings


def alert_subject(payload: dict) -> str:
    attachments = payload.get("attachments") or []
    if attachments:
        title = attachments[0].get("title") or "GlitchTip alert"
        return f"GlitchTip: {title}"
    text = payload.get("text") or ""
    if text:
        return text if text.startswith("GlitchTip") else f"GlitchTip: {text}"
    return "GlitchTip alert"


def send_alert_email(settings: Settings, subject: str, body: str) -> None:
    _validate_email_settings(settings)
    if settings.glitchtip_smtp_relay_url:
        _send_via_relay(settings, subject, body)
        return
    send_smtp_direct(settings, subject, body)


def send_smtp_direct(settings: Settings, subject: str, body: str) -> None:
    message = _build_message(settings, subject, body)
    host = settings.smtp_host
    if settings.smtp_port == 465:
        with smtplib.SMTP_SSL(host, settings.smtp_port, timeout=15) as smtp:
            _deliver(smtp, settings, message)
        return

    with smtplib.SMTP(host, settings.smtp_port, timeout=15) as smtp:
        if settings.smtp_use_tls:
            smtp.starttls()
        _deliver(smtp, settings, message)


def _validate_email_settings(settings: Settings) -> None:
    if not settings.glitchtip_alert_email_to:
        msg = "GLITCHTIP_ALERT_EMAIL_TO is not set"
        raise RuntimeError(msg)
    if not settings.smtp_host:
        msg = "SMTP_HOST is not set"
        raise RuntimeError(msg)
    from_addr = settings.glitchtip_alert_email_from or settings.smtp_user
    if not from_addr:
        msg = "Set GLITCHTIP_ALERT_EMAIL_FROM or SMTP_USER"
        raise RuntimeError(msg)


def _build_message(settings: Settings, subject: str, body: str) -> EmailMessage:
    from_addr = settings.glitchtip_alert_email_from or settings.smtp_user
    message = EmailMessage()
    message["From"] = from_addr
    message["To"] = settings.glitchtip_alert_email_to
    message["Subject"] = subject
    message.set_content(body)
    return message


def _send_via_relay(settings: Settings, subject: str, body: str) -> None:
    headers: dict[str, str] = {}
    if settings.smtp_relay_token:
        headers["Authorization"] = f"Bearer {settings.smtp_relay_token}"
    with httpx.Client(timeout=20.0) as client:
        response = client.post(
            settings.glitchtip_smtp_relay_url,
            json={"subject": subject, "body": body},
            headers=headers,
        )
        response.raise_for_status()


def _deliver(smtp: smtplib.SMTP, settings: Settings, message: EmailMessage) -> None:
    if settings.smtp_user:
        smtp.login(settings.smtp_user, settings.smtp_password)
    smtp.send_message(message)

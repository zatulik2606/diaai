"""GlitchTip Slack-compatible webhooks → Telegram / email (public :8000)."""

from __future__ import annotations

import json
import logging
import smtplib
import urllib.error
import urllib.parse
import urllib.request

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from backend.config import Settings, get_settings
from backend.glitchtip_email import alert_subject, send_alert_email

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhooks", tags=["webhooks"], include_in_schema=False)


def format_alert(payload: dict) -> str:
    attachments = payload.get("attachments") or []
    if attachments:
        att = attachments[0]
        title = att.get("title") or "GlitchTip alert"
        link = att.get("title_link") or ""
        detail = att.get("text") or ""
        lines = [f"GlitchTip: {title}"]
        if detail:
            lines.append(detail)
        if link:
            lines.append(link)
        return "\n".join(lines)

    sections = payload.get("sections") or []
    if sections:
        sec = sections[0]
        title = sec.get("activityTitle") or payload.get("text") or "GlitchTip alert"
        subtitle = sec.get("activitySubtitle") or ""
        return f"GlitchTip: {title}\n{subtitle}".strip()

    return payload.get("text") or "GlitchTip alert"


def send_telegram(token: str, chat_id: str, text: str) -> None:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    body = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    if not data.get("ok"):
        raise RuntimeError(data.get("description", "Telegram API error"))


def _check_secret(
    settings: Settings,
    secret: str | None,
    header_secret: str | None,
) -> None:
    if not settings.glitchtip_webhook_secret:
        return
    if secret == settings.glitchtip_webhook_secret:
        return
    if header_secret == settings.glitchtip_webhook_secret:
        return
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


def _webhook_ready(settings: Settings) -> None:
    if not settings.telegram_alarm_bot_token or not settings.telegram_alarm_chat_id:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Not configured")


def _email_ready(settings: Settings) -> None:
    if not settings.glitchtip_alert_email_to or not settings.smtp_host:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Not configured")


@router.api_route("/glitchtip/email", methods=["GET", "HEAD"])
async def glitchtip_email_webhook_probe(
    request: Request,
    settings: Settings = Depends(get_settings),
    secret: str | None = Query(default=None),
) -> dict[str, bool]:
    """GlitchTip validates webhook URLs with GET/HEAD before saving."""
    _email_ready(settings)
    _check_secret(settings, secret, request.headers.get("X-Webhook-Secret"))
    return {"ok": True}


@router.post("/glitchtip/email")
async def glitchtip_email_webhook(
    request: Request,
    settings: Settings = Depends(get_settings),
    secret: str | None = Query(default=None),
) -> dict[str, bool]:
    _email_ready(settings)
    _check_secret(settings, secret, request.headers.get("X-Webhook-Secret"))

    try:
        payload = await request.json()
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON") from exc

    text = format_alert(payload)
    try:
        send_alert_email(settings, alert_subject(payload), text)
    except (RuntimeError, smtplib.SMTPException, TimeoutError, OSError) as exc:
        logger.exception("email send failed")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Email delivery failed",
        ) from exc

    return {"ok": True}


@router.api_route("/glitchtip", methods=["GET", "HEAD"])
async def glitchtip_webhook_probe(
    request: Request,
    settings: Settings = Depends(get_settings),
    secret: str | None = Query(default=None),
) -> dict[str, bool]:
    """GlitchTip validates webhook URLs with GET/HEAD before saving."""
    _webhook_ready(settings)
    _check_secret(settings, secret, request.headers.get("X-Webhook-Secret"))
    return {"ok": True}


@router.post("/glitchtip")
async def glitchtip_webhook(
    request: Request,
    settings: Settings = Depends(get_settings),
    secret: str | None = Query(default=None),
) -> dict[str, bool]:
    _webhook_ready(settings)
    _check_secret(settings, secret, request.headers.get("X-Webhook-Secret"))

    try:
        payload = await request.json()
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON") from exc

    try:
        send_telegram(
            settings.telegram_alarm_bot_token,
            settings.telegram_alarm_chat_id,
            format_alert(payload),
        )
    except (RuntimeError, urllib.error.URLError, TimeoutError) as exc:
        logger.exception("telegram send failed")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Telegram delivery failed",
        ) from exc

    return {"ok": True}


def include_glitchtip_webhook(app, settings: Settings) -> None:
    telegram = settings.telegram_alarm_bot_token and settings.telegram_alarm_chat_id
    email = settings.glitchtip_alert_email_to and settings.smtp_host
    if telegram or email:
        app.include_router(router)

"""GlitchTip Slack-compatible webhook → SMTP email (MVP bridge)."""

from __future__ import annotations

import json
import logging
import os
import smtplib
import urllib.parse
from email.message import EmailMessage
from http.server import BaseHTTPRequestHandler, HTTPServer

logger = logging.getLogger(__name__)

SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
SMTP_USE_TLS = os.environ.get("SMTP_USE_TLS", "true").lower() in {"1", "true", "yes"}
EMAIL_TO = os.environ.get("GLITCHTIP_ALERT_EMAIL_TO", "")
EMAIL_FROM = os.environ.get("GLITCHTIP_ALERT_EMAIL_FROM", "") or SMTP_USER
WEBHOOK_SECRET = os.environ.get("GLITCHTIP_WEBHOOK_SECRET", "")
PORT = int(os.environ.get("PORT", "8081"))
HOST = os.environ.get("HOST", "0.0.0.0")


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


def alert_subject(payload: dict) -> str:
    attachments = payload.get("attachments") or []
    if attachments:
        title = attachments[0].get("title") or "GlitchTip alert"
        return f"GlitchTip: {title}"
    text = payload.get("text") or ""
    if text:
        return text if text.startswith("GlitchTip") else f"GlitchTip: {text}"
    return "GlitchTip alert"


def send_email(subject: str, body: str) -> None:
    if not EMAIL_TO or not SMTP_HOST or not EMAIL_FROM:
        msg = "GLITCHTIP_ALERT_EMAIL_TO, SMTP_HOST and sender must be set"
        raise RuntimeError(msg)

    message = EmailMessage()
    message["From"] = EMAIL_FROM
    message["To"] = EMAIL_TO
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as smtp:
        if SMTP_USE_TLS:
            smtp.starttls()
        if SMTP_USER:
            smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(message)


def check_secret(path: str, headers: dict) -> bool:
    if not WEBHOOK_SECRET:
        return True
    query = urllib.parse.urlparse(path).query
    params = urllib.parse.parse_qs(query)
    if params.get("secret", [None])[0] == WEBHOOK_SECRET:
        return True
    return headers.get("X-Webhook-Secret") == WEBHOOK_SECRET


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        logger.info("%s - %s", self.address_string(), fmt % args)

    def _json_response(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        if path in {"/", "/health"}:
            self._json_response(200, {"status": "ok"})
            return
        if path == "/webhook":
            if check_secret(self.path, {k: v for k, v in self.headers.items()}):
                self._json_response(200, {"ok": True})
            else:
                self._json_response(403, {"error": "forbidden"})
            return
        self._json_response(404, {"error": "not found"})

    def do_HEAD(self) -> None:
        self.do_GET()

    def do_POST(self) -> None:
        if self.path.split("?", 1)[0] != "/webhook":
            self._json_response(404, {"error": "not found"})
            return
        if not check_secret(self.path, {k: v for k, v in self.headers.items()}):
            self._json_response(403, {"error": "forbidden"})
            return

        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw.decode() or "{}")
        except json.JSONDecodeError:
            self._json_response(400, {"error": "invalid json"})
            return

        try:
            send_email(alert_subject(payload), format_alert(payload))
        except (RuntimeError, smtplib.SMTPException, TimeoutError, OSError) as exc:
            logger.exception("email send failed")
            self._json_response(502, {"error": str(exc)})
            return

        self._json_response(200, {"ok": True})


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    server = HTTPServer((HOST, PORT), Handler)
    logger.info("glitchtip-email-bridge listening on %s:%s", HOST, PORT)
    server.serve_forever()


if __name__ == "__main__":
    main()

"""GlitchTip Slack-compatible webhook → Telegram sendMessage (MVP bridge)."""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_ALARM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_ALARM_CHAT_ID", "")
WEBHOOK_SECRET = os.environ.get("GLITCHTIP_WEBHOOK_SECRET", "")
PORT = int(os.environ.get("PORT", "8080"))
HOST = os.environ.get("HOST", "0.0.0.0")
KUMA_MARKER = "[Uptime Kuma]"
GRAFANA_MARKER = "[Grafana]"


def _format_grafana(payload: dict) -> str | None:
    alerts = payload.get("alerts")
    if not isinstance(alerts, list) or "status" not in payload:
        return None

    status = payload.get("status", "firing")
    title = (payload.get("title") or payload.get("message") or "Grafana alert").strip()
    prefix = GRAFANA_MARKER if status == "firing" else f"{GRAFANA_MARKER} resolved"
    lines = [f"{prefix} {title}"]

    for alert in alerts[:3]:
        labels = alert.get("labels") or {}
        annotations = alert.get("annotations") or {}
        name = labels.get("alertname") or "alert"
        if annotations.get("summary"):
            lines.append(f"{name}: {annotations['summary']}")
        elif annotations.get("description"):
            lines.append(f"{name}: {annotations['description']}")

    return "\n".join(lines)


def format_alert(payload: dict) -> str:
    grafana = _format_grafana(payload)
    if grafana:
        return grafana

    text = (payload.get("text") or "").strip()
    if KUMA_MARKER in text:
        return text

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


def send_telegram(text: str) -> None:
    if not TOKEN or not CHAT_ID:
        msg = "TELEGRAM_ALARM_BOT_TOKEN and TELEGRAM_ALARM_CHAT_ID must be set"
        raise RuntimeError(msg)

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    body = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": text}).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    if not data.get("ok"):
        raise RuntimeError(data.get("description", "Telegram API error"))


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
        if self.path.split("?", 1)[0] in {"/", "/health"}:
            self._json_response(200, {"status": "ok"})
            return
        self._json_response(404, {"error": "not found"})

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
            send_telegram(format_alert(payload))
        except (RuntimeError, urllib.error.URLError, TimeoutError) as exc:
            logger.exception("telegram send failed")
            self._json_response(502, {"error": str(exc)})
            return

        self._json_response(200, {"ok": True})


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    server = HTTPServer((HOST, PORT), Handler)
    logger.info("glitchtip-telegram-bridge listening on %s:%s", HOST, PORT)
    server.serve_forever()


if __name__ == "__main__":
    main()

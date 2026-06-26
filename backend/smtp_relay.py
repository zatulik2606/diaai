"""Host-network SMTP relay — Timeweb blocks outbound :465/:587 from Docker."""

from __future__ import annotations

import json
import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from backend.config import get_settings
from backend.glitchtip_email import send_smtp_direct

logger = logging.getLogger(__name__)

HOST = os.environ.get("SMTP_RELAY_HOST", "0.0.0.0")
PORT = int(os.environ.get("SMTP_RELAY_PORT", "9090"))
TOKEN = os.environ.get("SMTP_RELAY_TOKEN", "")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        logger.info("%s - %s", self.address_string(), fmt % args)

    def do_GET(self) -> None:
        if self.path in {"/", "/health"}:
            self._json(200, {"status": "ok"})
            return
        self._json(404, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/send":
            self._json(404, {"error": "not found"})
            return
        if TOKEN and self.headers.get("Authorization") != f"Bearer {TOKEN}":
            self._json(403, {"error": "forbidden"})
            return

        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw.decode() or "{}")
        except json.JSONDecodeError:
            self._json(400, {"error": "invalid json"})
            return

        subject = payload.get("subject") or "GlitchTip alert"
        body = payload.get("body") or ""
        settings = get_settings()
        try:
            send_smtp_direct(settings, subject, body)
        except Exception as exc:
            logger.exception("smtp relay send failed")
            self._json(502, {"error": str(exc)})
            return
        self._json(200, {"ok": True})

    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    server = HTTPServer((HOST, PORT), Handler)
    logger.info("smtp-relay listening on %s:%s", HOST, PORT)
    server.serve_forever()


if __name__ == "__main__":
    main()

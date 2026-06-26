"""Poll GlitchTip API for new issues → Telegram (fallback when hosted webhooks lag)."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

from backend.config import Settings
from backend.glitchtip_webhook import send_telegram

logger = logging.getLogger(__name__)


class GlitchTipPoller:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._seen: set[str] = set()
        self._primed = False

    def _issues_url(self) -> str:
        base = self._settings.glitchtip_url.rstrip("/")
        return f"{base}/api/0/organizations/{self._settings.glitchtip_org}/issues/"

    async def fetch_issues(self) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                self._issues_url(),
                headers={"Authorization": f"Bearer {self._settings.glitchtip_api_token}"},
            )
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, list) else []

    @staticmethod
    def format_issue_message(issue: dict[str, Any]) -> str:
        metadata = issue.get("metadata") or {}
        exc_type = metadata.get("type") or "Exception"
        value = metadata.get("value") or exc_type
        title = f"{exc_type}: {value.split(' [')[0]}"
        link = issue.get("permalink") or ""
        lines = [f"GlitchTip: {title}"]
        if value:
            lines.append(value)
        if link:
            lines.append(link)
        return "\n".join(lines)

    async def poll_once(self) -> int:
        issues = await self.fetch_issues()
        sent = 0
        for issue in issues:
            issue_id = str(issue.get("id", ""))
            if not issue_id or issue_id in self._seen:
                continue
            self._seen.add(issue_id)
            if not self._primed:
                continue
            try:
                send_telegram(
                    self._settings.telegram_alarm_bot_token,
                    self._settings.telegram_alarm_chat_id,
                    self.format_issue_message(issue),
                )
                sent += 1
            except Exception:
                logger.exception("glitchtip poller telegram failed issue_id=%s", issue_id)
        self._primed = True
        return sent

    async def run(self) -> None:
        interval = self._settings.glitchtip_poll_interval_seconds
        logger.info(
            "GlitchTip poller started interval=%ss org=%s",
            interval,
            self._settings.glitchtip_org,
        )
        while True:
            try:
                sent = await self.poll_once()
                if sent:
                    logger.info("GlitchTip poller sent %s alert(s)", sent)
            except Exception:
                logger.exception("GlitchTip poller poll failed")
            await asyncio.sleep(interval)


def start_glitchtip_poller(settings: Settings) -> asyncio.Task[None] | None:
    if not (
        settings.glitchtip_api_token
        and settings.telegram_alarm_bot_token
        and settings.telegram_alarm_chat_id
        and settings.glitchtip_url
    ):
        return None
    poller = GlitchTipPoller(settings)
    return asyncio.create_task(poller.run())

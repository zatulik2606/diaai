#!/usr/bin/env python3
"""Configure Uptime Kuma alerts: Telegram via glitchtip-telegram-bridge webhook."""

from __future__ import annotations

import json
import os
import sys

from uptime_kuma_api import NotificationType, UptimeKumaApi, UptimeKumaException

KUMA_URL = os.environ.get("KUMA_URL", "http://127.0.0.1:3001")
KUMA_USERNAME = os.environ.get("KUMA_USERNAME", "admin")
KUMA_PASSWORD = os.environ.get("KUMA_PASSWORD", "")

TELEGRAM_BRIDGE_URL = os.environ.get(
    "KUMA_TELEGRAM_BRIDGE_URL",
    "http://glitchtip-telegram-bridge:8080/webhook",
)

# Legacy names removed on re-run (native Telegram/SMTP fail from Kuma container on VPS).
LEGACY_NAMES = ("diaai-telegram", "diaai-email")


def find_notification(notifications: list[dict], name: str) -> dict | None:
    for item in notifications:
        if item.get("name") == name:
            return item
    return None


def telegram_bridge_spec() -> dict:
    return {
        "name": "diaai-telegram-bridge",
        "type": NotificationType.WEBHOOK,
        "webhookURL": TELEGRAM_BRIDGE_URL,
        "webhookContentType": "application/json",
        "webhookCustomBody": json.dumps(
            {
                "text": "[Uptime Kuma] {{ monitor.name }}: {{ msg }}",
                "attachments": [
                    {
                        "title": "{{ monitor.name }}",
                        "text": "{{ msg }}",
                    }
                ],
            }
        ),
        "isDefault": True,
        "applyExisting": True,
    }


def remove_legacy(api: UptimeKumaApi) -> None:
    for item in api.get_notifications():
        if item.get("name") in LEGACY_NAMES:
            api.delete_notification(int(item["id"]))
            print(f"removed legacy: {item['name']}")


def ensure_notification(api: UptimeKumaApi, spec: dict) -> int:
    existing = find_notification(api.get_notifications(), spec["name"])
    if existing:
        api.edit_notification(int(existing["id"]), **spec)
        print(f"updated: {spec['name']} id={existing['id']}")
        return int(existing["id"])
    result = api.add_notification(**spec)
    notification_id = int(result["id"])
    print(f"added: {spec['name']} id={notification_id}")
    return notification_id


def test_notification(api: UptimeKumaApi, spec: dict) -> None:
    result = api.test_notification(**spec)
    msg = str(result.get("msg", result))
    ok = bool(result.get("ok")) or "success" in msg.lower()
    print(f"test {spec['name']}: ok={ok} msg={msg}")
    if not ok:
        raise UptimeKumaException(f"test failed for {spec['name']}: {msg}")


def attach_to_monitors(api: UptimeKumaApi, notification_id: int) -> None:
    wanted = {notification_id}
    for monitor in api.get_monitors():
        current: set[int] = set()
        raw = monitor.get("notificationIDList")
        if isinstance(raw, dict):
            current = {int(k) for k, enabled in raw.items() if enabled}
        elif isinstance(raw, list):
            current = {int(x) for x in raw}
        if current == wanted:
            print(f"skip notifications on: {monitor['name']}")
            continue
        api.edit_monitor(int(monitor["id"]), notificationIDList={str(notification_id): True})
        print(f"linked {spec_name()} -> {monitor['name']}")


def spec_name() -> str:
    return "diaai-telegram-bridge"


def main() -> int:
    if not KUMA_PASSWORD:
        print("KUMA_PASSWORD is required", file=sys.stderr)
        return 1

    spec = telegram_bridge_spec()

    with UptimeKumaApi(KUMA_URL) as api:
        api.login(KUMA_USERNAME, KUMA_PASSWORD)
        remove_legacy(api)
        notification_id = ensure_notification(api, spec)
        attach_to_monitors(api, notification_id)
        test_notification(api, spec)

    print("done")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except UptimeKumaException as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

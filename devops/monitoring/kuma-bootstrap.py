#!/usr/bin/env python3
"""Idempotent Uptime Kuma setup: admin (first run) + diaai monitors."""

from __future__ import annotations

import os
import sys

from uptime_kuma_api import MonitorType, UptimeKumaApi, UptimeKumaException

KUMA_URL = os.environ.get("KUMA_URL", "http://127.0.0.1:3001")
KUMA_USERNAME = os.environ.get("KUMA_USERNAME", "admin")
KUMA_PASSWORD = os.environ.get("KUMA_PASSWORD", "")

BACKEND_URL = os.environ.get(
    "KUMA_MONITOR_BACKEND_URL", "http://172.18.0.1:8000/health"
)
FRONTEND_URL = os.environ.get("KUMA_MONITOR_FRONTEND_URL", "http://web:3000/")
POSTGRES_HOST = os.environ.get("KUMA_MONITOR_POSTGRES_HOST", "postgres")
POSTGRES_PORT = int(os.environ.get("KUMA_MONITOR_POSTGRES_PORT", "5432"))
POSTGRES_DB = os.environ.get("KUMA_MONITOR_POSTGRES_DB", "diaai")
POSTGRES_USER = os.environ.get("KUMA_MONITOR_POSTGRES_USER", "diaai")
POSTGRES_PASSWORD = os.environ.get("KUMA_MONITOR_POSTGRES_PASSWORD", "diaai")

MONITORS: list[dict] = [
    {
        "name": "diaai-backend",
        "type": MonitorType.HTTP,
        "url": BACKEND_URL,
        "keyword": '"status":"ok"',
        "interval": 60,
        "maxretries": 3,
    },
    {
        "name": "diaai-frontend",
        "type": MonitorType.HTTP,
        "url": FRONTEND_URL,
        "accepted_statuscodes": ["200-299", "300-399"],
        "interval": 60,
        "maxretries": 3,
    },
    {
        "name": "diaai-postgres",
        "type": MonitorType.POSTGRES,
        "databaseConnectionString": (
            f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
            f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        ),
        "databaseQuery": "SELECT 1",
        "interval": 60,
        "maxretries": 3,
    },
]


def existing_names(api: UptimeKumaApi) -> set[str]:
    monitors = api.get_monitors()
    return {m["name"] for m in monitors}


def main() -> int:
    if not KUMA_PASSWORD:
        print("KUMA_PASSWORD is required", file=sys.stderr)
        return 1

    with UptimeKumaApi(KUMA_URL) as api:
        if api.need_setup():
            result = api.setup(KUMA_USERNAME, KUMA_PASSWORD)
            print(f"setup: {result.get('msg', result)}")
        api.login(KUMA_USERNAME, KUMA_PASSWORD)

        names = existing_names(api)
        for spec in MONITORS:
            name = spec["name"]
            if name in names:
                print(f"skip (exists): {name}")
                continue
            payload = {k: v for k, v in spec.items() if k != "name"}
            payload["name"] = name
            try:
                result = api.add_monitor(**payload)
                print(f"added: {name} -> id={result.get('monitorID')}")
            except UptimeKumaException as exc:
                print(f"error adding {name}: {exc}", file=sys.stderr)
                return 1

    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

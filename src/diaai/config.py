from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(slots=True)
class Config:
    telegram_bot_token: str
    backend_url: str
    backend_service_token: str
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Config":
        load_dotenv()
        telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").strip()
        backend_service_token = os.getenv("BACKEND_SERVICE_TOKEN", "").strip()
        log_level = os.getenv("LOG_LEVEL", "INFO").strip() or "INFO"

        missing = []
        if not telegram_bot_token:
            missing.append("TELEGRAM_BOT_TOKEN")
        if not backend_service_token:
            missing.append("BACKEND_SERVICE_TOKEN")
        if missing:
            missing_vars = ", ".join(missing)
            raise ValueError(f"Missing required environment variables: {missing_vars}")

        return cls(
            telegram_bot_token=telegram_bot_token,
            backend_url=backend_url,
            backend_service_token=backend_service_token,
            log_level=log_level.upper(),
        )

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(slots=True)
class Config:
    telegram_bot_token: str
    openrouter_api_key: str
    llm_model: str
    llm_max_history: int = 10
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Config":
        load_dotenv()
        telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        openrouter_api_key = (
            os.getenv("OPENROUTER_API_KEY", "").strip()
            or os.getenv("LLM_API_KEY", "").strip()
        )
        llm_model = os.getenv("LLM_MODEL", "").strip()
        llm_max_history = int(os.getenv("LLM_MAX_HISTORY", "10"))
        log_level = os.getenv("LOG_LEVEL", "INFO").strip() or "INFO"

        missing = []
        if not telegram_bot_token:
            missing.append("TELEGRAM_BOT_TOKEN")
        if not openrouter_api_key:
            missing.append("OPENROUTER_API_KEY or LLM_API_KEY")
        if not llm_model:
            missing.append("LLM_MODEL")
        if missing:
            missing_vars = ", ".join(missing)
            raise ValueError(f"Missing required environment variables: {missing_vars}")

        if llm_max_history < 1:
            raise ValueError("LLM_MAX_HISTORY must be greater than 0")

        return cls(
            telegram_bot_token=telegram_bot_token,
            openrouter_api_key=openrouter_api_key,
            llm_model=llm_model,
            llm_max_history=llm_max_history,
            log_level=log_level.upper(),
        )

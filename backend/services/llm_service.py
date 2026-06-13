from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from fastapi import Depends
from openai import OpenAI

from backend.config import Settings, get_settings
from backend.exceptions import AppError

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT_PATH = Path(__file__).resolve().parents[2] / "prompts" / "system.txt"


def load_system_prompt() -> str:
    return _SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()


class LlmService:
    def __init__(self, api_key: str, model: str, timeout_seconds: float = 30.0) -> None:
        self._model = model
        self._client = (
            OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1",
                timeout=timeout_seconds,
            )
            if api_key
            else None
        )

    def generate_reply(
        self, system_prompt: str, history: list[dict[str, Any]], user_content: Any
    ) -> str:
        if self._client is None:
            raise AppError(
                code="LLM_UNAVAILABLE",
                message="LLM service is not configured",
                status_code=502,
            )
        messages: list[dict[str, Any]] = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_content})

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("LLM request failed: %s", exc.__class__.__name__)
            raise AppError(
                code="LLM_UNAVAILABLE",
                message="LLM service temporarily unavailable",
                status_code=502,
            ) from exc

        content = response.choices[0].message.content if response.choices else None
        if not content:
            return "Не удалось получить ответ от модели. Попробуйте переформулировать вопрос."
        return content.strip()


def get_llm_service(settings: Settings = Depends(get_settings)) -> LlmService:
    return LlmService(
        api_key=settings.openrouter_api_key,
        model=settings.llm_model,
        timeout_seconds=settings.llm_timeout_seconds,
    )

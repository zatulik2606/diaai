from __future__ import annotations

import logging
from typing import Any

from openai import OpenAI

logger = logging.getLogger(__name__)


class LlmClient:
    def __init__(self, api_key: str, model: str, timeout_seconds: float = 30.0) -> None:
        self._client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            timeout=timeout_seconds,
        )
        self._model = model

    def generate_reply(
        self, system_prompt: str, history: list[dict[str, Any]], user_content: Any
    ) -> str:
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
            raise RuntimeError("LLM request failed") from exc

        content = response.choices[0].message.content if response.choices else None
        if not content:
            return "Не удалось получить ответ от модели. Попробуйте переформулировать вопрос."
        return content.strip()

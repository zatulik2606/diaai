from __future__ import annotations

import logging
from uuid import uuid4

import httpx

logger = logging.getLogger(__name__)

_UNAVAILABLE_MSG = "Сервис временно недоступен. Попробуйте ещё раз через минуту."
_CONFIG_MSG = "Ошибка конфигурации сервиса."
_INVALID_MSG = "Не удалось обработать сообщение."


class BackendClientError(Exception):
    """Backend call failed; user_message is safe to show in Telegram."""

    def __init__(self, user_message: str) -> None:
        self.user_message = user_message
        super().__init__(user_message)


class BackendClient:
    def __init__(
        self,
        base_url: str,
        service_token: str,
        timeout_seconds: float = 30.0,
    ) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            timeout=timeout_seconds,
        )
        self._service_token = service_token

    async def aclose(self) -> None:
        await self._client.aclose()

    async def send_assistant_message(
        self,
        telegram_id: int,
        *,
        text: str | None = None,
        image_base64: str | None = None,
        image_media_type: str = "image/jpeg",
    ) -> str:
        payload: dict[str, str | int] = {"telegram_id": telegram_id}
        if text is not None:
            payload["text"] = text
        if image_base64 is not None:
            payload["image_base64"] = image_base64
            payload["image_media_type"] = image_media_type

        headers = {
            "Authorization": f"Bearer {self._service_token}",
            "X-Request-Id": str(uuid4()),
        }

        try:
            response = await self._client.post(
                "/api/v1/assistant/messages",
                json=payload,
                headers=headers,
            )
        except httpx.RequestError as exc:
            logger.warning("Backend request failed: %s", exc.__class__.__name__)
            raise BackendClientError(_UNAVAILABLE_MSG) from exc

        if response.status_code == 200:
            data = response.json()
            reply = data.get("reply")
            if not isinstance(reply, str) or not reply.strip():
                logger.warning("Backend returned empty reply telegram_id=%s", telegram_id)
                return "Не удалось получить ответ. Попробуйте переформулировать вопрос."
            return reply.strip()

        if response.status_code in (502, 503):
            raise BackendClientError(_UNAVAILABLE_MSG)

        if response.status_code in (401, 403):
            logger.warning("Backend auth failed status=%s", response.status_code)
            raise BackendClientError(_CONFIG_MSG)

        if response.status_code in (400, 422):
            raise BackendClientError(_INVALID_MSG)

        logger.warning("Backend unexpected status=%s", response.status_code)
        raise BackendClientError(_UNAVAILABLE_MSG)

    async def transcribe_audio(
        self,
        audio_base64: str,
        *,
        media_type: str = "audio/ogg",
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self._service_token}",
            "X-Request-Id": str(uuid4()),
        }
        payload = {
            "audio_base64": audio_base64,
            "media_type": media_type,
        }

        try:
            response = await self._client.post(
                "/api/v1/media/transcribe",
                json=payload,
                headers=headers,
            )
        except httpx.RequestError as exc:
            logger.warning("Backend transcribe failed: %s", exc.__class__.__name__)
            raise BackendClientError(_UNAVAILABLE_MSG) from exc

        if response.status_code == 200:
            data = response.json()
            text = data.get("text")
            if isinstance(text, str) and text.strip():
                return text.strip()
            raise BackendClientError("Не удалось распознать. Отправьте текстом.")

        if response.status_code in (422, 400):
            raise BackendClientError("Не удалось распознать. Отправьте текстом.")

        if response.status_code in (502, 503):
            raise BackendClientError(_UNAVAILABLE_MSG)

        if response.status_code in (401, 403):
            logger.warning("Backend auth failed status=%s", response.status_code)
            raise BackendClientError(_CONFIG_MSG)

        logger.warning("Backend transcribe unexpected status=%s", response.status_code)
        raise BackendClientError(_UNAVAILABLE_MSG)

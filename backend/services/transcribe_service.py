from __future__ import annotations

import base64
import logging

import httpx
from fastapi import Depends

from backend.config import Settings, get_settings
from backend.exceptions import AppError

logger = logging.getLogger(__name__)

OPENROUTER_STT_URL = "https://openrouter.ai/api/v1/audio/transcriptions"
MAX_AUDIO_BYTES = 5 * 1024 * 1024

_MEDIA_FORMAT: dict[str, str] = {
    "audio/ogg": "ogg",
    "audio/webm": "webm",
    "audio/mpeg": "mp3",
    "audio/mp3": "mp3",
    "audio/mp4": "m4a",
    "audio/m4a": "m4a",
    "audio/wav": "wav",
    "audio/x-wav": "wav",
    "audio/flac": "flac",
    "audio/aac": "aac",
}


class TranscribeService:
    def __init__(
        self,
        api_key: str,
        model: str,
        timeout_seconds: float = 60.0,
    ) -> None:
        self._api_key = api_key
        self._model = model
        self._timeout = timeout_seconds

    def transcribe(self, audio_base64: str, media_type: str) -> str:
        if not self._api_key:
            raise AppError(
                code="STT_UNAVAILABLE",
                message="Speech-to-text service is not configured",
                status_code=502,
            )

        stripped = audio_base64.strip()
        try:
            audio_bytes = base64.b64decode(stripped, validate=True)
        except (ValueError, TypeError) as exc:
            raise AppError(
                code="BAD_REQUEST",
                message="Invalid audio_base64",
                status_code=400,
            ) from exc

        if not audio_bytes:
            raise AppError(
                code="BAD_REQUEST",
                message="Empty audio payload",
                status_code=400,
            )

        if len(audio_bytes) > MAX_AUDIO_BYTES:
            raise AppError(
                code="PAYLOAD_TOO_LARGE",
                message="Audio exceeds 5 MB limit",
                status_code=413,
            )

        media_type_key = media_type.split(";")[0].strip().lower()
        audio_format = _MEDIA_FORMAT.get(media_type_key, "ogg")

        payload = {
            "model": self._model,
            "input_audio": {
                "data": stripped,
                "format": audio_format,
            },
            "language": "ru",
        }

        try:
            response = httpx.post(
                OPENROUTER_STT_URL,
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=self._timeout,
            )
        except httpx.RequestError as exc:
            logger.warning("STT request failed: %s", exc.__class__.__name__)
            raise AppError(
                code="STT_UNAVAILABLE",
                message="Speech-to-text temporarily unavailable",
                status_code=502,
            ) from exc

        if response.status_code != 200:
            logger.warning("STT request failed status=%s", response.status_code)
            raise AppError(
                code="STT_UNAVAILABLE",
                message="Speech-to-text temporarily unavailable",
                status_code=502,
            )

        try:
            data = response.json()
        except ValueError as exc:
            raise AppError(
                code="STT_UNAVAILABLE",
                message="Speech-to-text temporarily unavailable",
                status_code=502,
            ) from exc

        text = (data.get("text") or "").strip()
        if not text:
            raise AppError(
                code="STT_EMPTY",
                message="Could not recognize speech",
                status_code=422,
            )
        return text


def get_transcribe_service(settings: Settings = Depends(get_settings)) -> TranscribeService:
    return TranscribeService(
        api_key=settings.openrouter_api_key,
        model=settings.stt_model,
        timeout_seconds=settings.stt_timeout_seconds,
    )

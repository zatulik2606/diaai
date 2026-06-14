from __future__ import annotations

import base64
import binascii

from pydantic import BaseModel, Field, field_validator

MAX_IMAGE_BYTES = 5 * 1024 * 1024

_DATA_URL_BASE64_MARKER = ";base64,"


def _normalize_image_base64(value: str) -> str:
    normalized = value.strip()
    if not normalized:
        return normalized

    if normalized.lower().startswith("data:"):
        _, _, normalized = normalized.partition(",")
        normalized = normalized.strip()
    else:
        marker_idx = normalized.lower().find(_DATA_URL_BASE64_MARKER)
        if marker_idx != -1:
            normalized = normalized[marker_idx + len(_DATA_URL_BASE64_MARKER) :].strip()
        elif ";" in normalized:
            prefix, _, rest = normalized.partition(";")
            if "/" in prefix:
                normalized = rest.strip()

    return "".join(normalized.split())


class AssistantMessageRequest(BaseModel):
    telegram_id: int
    text: str | None = Field(default=None, min_length=1)
    image_base64: str | None = None
    image_media_type: str = "image/jpeg"

    @field_validator("image_base64")
    @classmethod
    def validate_image_base64(cls, value: str | None) -> str | None:
        if value is None:
            return value
        normalized = _normalize_image_base64(value)
        if not normalized:
            return value
        try:
            decoded = base64.b64decode(normalized, validate=True)
        except binascii.Error:
            raise ValueError("image_base64 must be valid base64") from None
        if len(decoded) > MAX_IMAGE_BYTES:
            raise ValueError("image exceeds 5 MB limit") from None
        return normalized


class AssistantMessageResponse(BaseModel):
    dialog_id: str
    request_id: str
    reply: str

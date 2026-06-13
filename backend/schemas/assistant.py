from __future__ import annotations

import base64
import binascii

from pydantic import BaseModel, Field, field_validator

MAX_IMAGE_BYTES = 5 * 1024 * 1024


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
        stripped = value.strip()
        if not stripped:
            return value
        try:
            decoded = base64.b64decode(stripped, validate=True)
        except binascii.Error:
            raise ValueError("image_base64 must be valid base64") from None
        if len(decoded) > MAX_IMAGE_BYTES:
            raise ValueError("image exceeds 5 MB limit") from None
        return stripped


class AssistantMessageResponse(BaseModel):
    dialog_id: str
    request_id: str
    reply: str

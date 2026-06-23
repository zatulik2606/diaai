import base64

from pydantic import BaseModel, Field, field_validator


class TranscribeRequest(BaseModel):
    audio_base64: str = Field(min_length=1)
    media_type: str = Field(default="audio/ogg", min_length=1)

    @field_validator("audio_base64")
    @classmethod
    def validate_audio_base64(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            msg = "Empty audio_base64"
            raise ValueError(msg)
        try:
            decoded = base64.b64decode(stripped, validate=True)
        except (ValueError, TypeError) as exc:
            msg = "Invalid audio_base64"
            raise ValueError(msg) from exc
        if not decoded:
            msg = "Empty audio payload"
            raise ValueError(msg)
        return stripped


class TranscribeResponse(BaseModel):
    text: str = Field(min_length=1)

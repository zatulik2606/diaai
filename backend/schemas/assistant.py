from pydantic import BaseModel, Field


class AssistantMessageRequest(BaseModel):
    telegram_id: int
    text: str | None = Field(default=None, min_length=1)
    image_base64: str | None = None
    image_media_type: str = "image/jpeg"


class AssistantMessageResponse(BaseModel):
    dialog_id: str
    request_id: str
    reply: str

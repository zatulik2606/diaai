from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import Settings
from backend.models.request import DialogRequest
from backend.repositories.dialog import DialogRepository
from backend.repositories.request import RequestRepository
from backend.repositories.user import UserRepository
from backend.schemas.assistant import AssistantMessageRequest, AssistantMessageResponse
from backend.services.llm_service import LlmService, load_system_prompt


class AssistantService:
    def __init__(self, session: AsyncSession, llm: LlmService, settings: Settings) -> None:
        self._session = session
        self._llm = llm
        self._settings = settings
        self._users = UserRepository(session)
        self._dialogs = DialogRepository(session)
        self._requests = RequestRepository(session)

    async def handle_message(self, body: AssistantMessageRequest) -> AssistantMessageResponse:
        user = await self._users.get_or_create(body.telegram_id)
        dialog = await self._dialogs.get_or_create_active(user.id)

        history_limit = self._settings.llm_max_history * 2
        past = await self._requests.list_for_dialog(dialog.id, limit=history_limit)
        history = _build_history(past)

        has_text = body.text is not None and body.text.strip() != ""
        has_image = body.image_base64 is not None and body.image_base64.strip() != ""

        if has_image and has_text:
            request_type = "mixed"
        elif has_image:
            request_type = "photo"
        else:
            request_type = "text"

        user_content: Any
        media: dict[str, Any] | None = None
        content_for_store: str | None = body.text

        if has_image:
            text_part = (body.text or "").strip() or "Оцени состав и ориентировочные ХЕ по фото."
            content_for_store = text_part
            media = {
                "image_base64": body.image_base64,
                "image_media_type": body.image_media_type,
            }
            user_content = [
                {"type": "text", "text": text_part},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{body.image_media_type};base64,{body.image_base64}",
                    },
                },
            ]
        else:
            user_content = body.text or ""

        reply = self._llm.generate_reply(load_system_prompt(), history, user_content)

        record = await self._requests.create(
            dialog_id=dialog.id,
            user_id=user.id,
            request_type=request_type,
            content=content_for_store,
            reply=reply,
            media=media,
        )

        return AssistantMessageResponse(
            dialog_id=str(dialog.id),
            request_id=str(record.id),
            reply=reply,
        )


def _build_history(requests: list[DialogRequest]) -> list[dict[str, Any]]:
    messages: list[dict[str, Any]] = []
    for req in requests:
        if req.content:
            messages.append({"role": "user", "content": req.content})
        messages.append({"role": "assistant", "content": req.reply})
    return messages

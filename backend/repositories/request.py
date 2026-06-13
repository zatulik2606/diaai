import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.request import DialogRequest


class RequestRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, request_id: uuid.UUID) -> DialogRequest | None:
        return await self._session.get(DialogRequest, request_id)

    async def list_for_dialog(self, dialog_id: uuid.UUID, limit: int) -> list[DialogRequest]:
        result = await self._session.execute(
            select(DialogRequest)
            .where(DialogRequest.dialog_id == dialog_id)
            .order_by(DialogRequest.created_at.desc())
            .limit(limit)
        )
        rows = list(result.scalars().all())
        rows.reverse()
        return rows

    async def create(
        self,
        *,
        dialog_id: uuid.UUID,
        user_id: uuid.UUID,
        request_type: str,
        content: str | None,
        reply: str,
        media: dict[str, Any] | None = None,
    ) -> DialogRequest:
        record = DialogRequest(
            dialog_id=dialog_id,
            user_id=user_id,
            type=request_type,
            content=content,
            reply=reply,
            media=media,
        )
        self._session.add(record)
        await self._session.flush()
        return record

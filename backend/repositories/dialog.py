from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.dialog import Dialog


class DialogRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_active_for_user(self, user_id, channel: str = "telegram") -> Dialog | None:
        result = await self._session.execute(
            select(Dialog).where(
                Dialog.user_id == user_id,
                Dialog.channel == channel,
                Dialog.status == "active",
            )
        )
        return result.scalar_one_or_none()

    async def get_or_create_active(self, user_id, channel: str = "telegram") -> Dialog:
        dialog = await self.get_active_for_user(user_id, channel)
        if dialog is not None:
            return dialog
        dialog = Dialog(user_id=user_id, channel=channel, status="active")
        self._session.add(dialog)
        await self._session.flush()
        return dialog

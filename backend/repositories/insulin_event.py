import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.insulin_event import InsulinEvent


class InsulinEventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        user_id: uuid.UUID,
        dose: float,
        injected_at: datetime,
        food_event_id: uuid.UUID | None = None,
        comment: str | None = None,
    ) -> InsulinEvent:
        event = InsulinEvent(
            user_id=user_id,
            dose=dose,
            injected_at=injected_at,
            food_event_id=food_event_id,
            comment=comment,
        )
        self._session.add(event)
        await self._session.flush()
        return event

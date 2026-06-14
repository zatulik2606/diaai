import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
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

    async def sum_dose_by_user(
        self,
        user_ids: list[UUID],
        from_dt: datetime,
        to_dt: datetime,
    ) -> dict[UUID, float]:
        if not user_ids:
            return {}
        result = await self._session.execute(
            select(
                InsulinEvent.user_id,
                func.coalesce(func.sum(InsulinEvent.dose), 0),
            )
            .where(
                InsulinEvent.user_id.in_(user_ids),
                InsulinEvent.injected_at >= from_dt,
                InsulinEvent.injected_at < to_dt,
            )
            .group_by(InsulinEvent.user_id)
        )
        return {row[0]: float(row[1]) for row in result.all()}

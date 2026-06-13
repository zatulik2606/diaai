import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.food_event import FoodEvent
from backend.schemas.events import FoodSource


class FoodEventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, event_id: uuid.UUID) -> FoodEvent | None:
        return await self._session.get(FoodEvent, event_id)

    async def create(
        self,
        *,
        user_id: uuid.UUID,
        description: str,
        xe: float,
        bje: float,
        source: FoodSource,
        proteins: float | None = None,
        fats: float | None = None,
        carbs: float | None = None,
        request_id: uuid.UUID | None = None,
        comment: str | None = None,
    ) -> FoodEvent:
        event = FoodEvent(
            user_id=user_id,
            description=description,
            xe=xe,
            bje=bje,
            proteins=proteins,
            fats=fats,
            carbs=carbs,
            source=source.value,
            request_id=request_id,
            comment=comment,
        )
        self._session.add(event)
        await self._session.flush()
        return event

    async def list_for_user(
        self,
        user_id: uuid.UUID,
        from_dt: datetime | None = None,
        to_dt: datetime | None = None,
    ) -> list[FoodEvent]:
        query = select(FoodEvent).where(FoodEvent.user_id == user_id)
        if from_dt is not None:
            query = query.where(FoodEvent.recorded_at >= from_dt)
        if to_dt is not None:
            query = query.where(FoodEvent.recorded_at <= to_dt)
        query = query.order_by(FoodEvent.recorded_at.desc())
        result = await self._session.execute(query)
        return list(result.scalars().all())

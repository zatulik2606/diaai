import uuid
from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Date, cast, func, select
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

    async def count_in_window(
        self,
        user_ids: list[UUID],
        from_dt: datetime,
        to_dt: datetime,
    ) -> int:
        if not user_ids:
            return 0
        result = await self._session.scalar(
            select(func.count())
            .select_from(FoodEvent)
            .where(
                FoodEvent.user_id.in_(user_ids),
                FoodEvent.recorded_at >= from_dt,
                FoodEvent.recorded_at < to_dt,
            )
        )
        return int(result or 0)

    async def sum_xe_in_window(
        self,
        user_ids: list[UUID],
        from_dt: datetime,
        to_dt: datetime,
    ) -> float:
        if not user_ids:
            return 0.0
        result = await self._session.scalar(
            select(func.coalesce(func.sum(FoodEvent.xe), 0)).where(
                FoodEvent.user_id.in_(user_ids),
                FoodEvent.recorded_at >= from_dt,
                FoodEvent.recorded_at < to_dt,
            )
        )
        return float(result or 0)

    async def sum_nutrition_in_window(
        self,
        user_ids: list[UUID],
        from_dt: datetime,
        to_dt: datetime,
    ) -> dict[str, float | None]:
        if not user_ids:
            return {
                "xe": 0.0,
                "bje": 0.0,
                "proteins": None,
                "fats": None,
                "carbs": None,
            }
        result = await self._session.execute(
            select(
                func.coalesce(func.sum(FoodEvent.xe), 0),
                func.coalesce(func.sum(FoodEvent.bje), 0),
                func.sum(FoodEvent.proteins),
                func.sum(FoodEvent.fats),
                func.sum(FoodEvent.carbs),
            ).where(
                FoodEvent.user_id.in_(user_ids),
                FoodEvent.recorded_at >= from_dt,
                FoodEvent.recorded_at < to_dt,
            )
        )
        row = result.one()
        return {
            "xe": round(float(row[0]), 1),
            "bje": round(float(row[1]), 1),
            "proteins": round(float(row[2]), 1) if row[2] is not None else None,
            "fats": round(float(row[3]), 1) if row[3] is not None else None,
            "carbs": round(float(row[4]), 1) if row[4] is not None else None,
        }

    async def count_distinct_users_in_window(
        self,
        user_ids: list[UUID],
        from_dt: datetime,
        to_dt: datetime,
    ) -> int:
        if not user_ids:
            return 0
        result = await self._session.scalar(
            select(func.count(func.distinct(FoodEvent.user_id))).where(
                FoodEvent.user_id.in_(user_ids),
                FoodEvent.recorded_at >= from_dt,
                FoodEvent.recorded_at < to_dt,
            )
        )
        return int(result or 0)

    async def daily_counts(
        self,
        user_ids: list[UUID],
        from_day: date,
        days: int,
    ) -> dict[date, int]:
        if not user_ids or days <= 0:
            return {}
        to_day = from_day.toordinal() + days
        to_date = date.fromordinal(to_day)
        day_col = cast(FoodEvent.recorded_at, Date)
        result = await self._session.execute(
            select(day_col, func.count())
            .where(
                FoodEvent.user_id.in_(user_ids),
                day_col >= from_day,
                day_col < to_date,
            )
            .group_by(day_col)
        )
        return {row[0]: int(row[1]) for row in result.all()}

    async def list_for_users(
        self,
        user_ids: list[UUID],
        *,
        limit: int | None = None,
    ) -> list[FoodEvent]:
        if not user_ids:
            return []
        query = (
            select(FoodEvent)
            .where(FoodEvent.user_id.in_(user_ids))
            .order_by(FoodEvent.recorded_at.desc())
        )
        if limit is not None:
            query = query.limit(limit)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def count_for_users(self, user_ids: list[UUID]) -> int:
        if not user_ids:
            return 0
        result = await self._session.scalar(
            select(func.count()).select_from(FoodEvent).where(FoodEvent.user_id.in_(user_ids))
        )
        return int(result or 0)

    async def aggregate_by_user(
        self,
        user_ids: list[UUID],
        from_dt: datetime,
        to_dt: datetime,
    ) -> dict[UUID, dict[str, float]]:
        if not user_ids:
            return {}
        result = await self._session.execute(
            select(
                FoodEvent.user_id,
                func.coalesce(func.sum(FoodEvent.xe), 0),
                func.coalesce(func.sum(FoodEvent.bje), 0),
                func.count(),
            )
            .where(
                FoodEvent.user_id.in_(user_ids),
                FoodEvent.recorded_at >= from_dt,
                FoodEvent.recorded_at < to_dt,
            )
            .group_by(FoodEvent.user_id)
        )
        return {
            row[0]: {"xe": float(row[1]), "bje": float(row[2]), "food_count": float(row[3])}
            for row in result.all()
        }

    async def products_by_user(
        self,
        user_ids: list[UUID],
        from_dt: datetime,
        to_dt: datetime,
        *,
        limit_per_user: int = 20,
    ) -> dict[UUID, list[dict[str, float | str]]]:
        if not user_ids:
            return {}
        name_expr = func.trim(FoodEvent.description)
        result = await self._session.execute(
            select(
                FoodEvent.user_id,
                name_expr,
                func.coalesce(func.sum(FoodEvent.xe), 0),
                func.coalesce(func.sum(FoodEvent.bje), 0),
            )
            .where(
                FoodEvent.user_id.in_(user_ids),
                FoodEvent.recorded_at >= from_dt,
                FoodEvent.recorded_at < to_dt,
            )
            .group_by(FoodEvent.user_id, name_expr)
            .order_by(FoodEvent.user_id, func.sum(FoodEvent.xe).desc())
        )
        by_user: dict[UUID, list[dict[str, float | str]]] = {uid: [] for uid in user_ids}
        for row in result.all():
            user_id = row[0]
            if len(by_user[user_id]) >= limit_per_user:
                continue
            by_user[user_id].append(
                {
                    "name": str(row[1]),
                    "xe": float(row[2]),
                    "bje": float(row[3]),
                }
            )
        return by_user

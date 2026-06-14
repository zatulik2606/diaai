import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.progress_snapshot import ProgressSnapshot


class ProgressSnapshotRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        user_id: uuid.UUID,
        period: str,
        period_start: date,
        period_end: date,
        sum_xe: float,
        sum_bje: float,
        sum_insulin: float,
        trend: str,
        sum_proteins: float | None = None,
        sum_fats: float | None = None,
        sum_carbs: float | None = None,
        comment: str | None = None,
    ) -> ProgressSnapshot:
        snapshot = ProgressSnapshot(
            user_id=user_id,
            period=period,
            period_start=period_start,
            period_end=period_end,
            sum_xe=sum_xe,
            sum_bje=sum_bje,
            sum_insulin=sum_insulin,
            sum_proteins=sum_proteins,
            sum_fats=sum_fats,
            sum_carbs=sum_carbs,
            trend=trend,
            comment=comment,
        )
        self._session.add(snapshot)
        await self._session.flush()
        return snapshot

    async def get_by_user_period(
        self,
        user_id: uuid.UUID,
        period: str,
        period_start: date,
    ) -> ProgressSnapshot | None:
        result = await self._session.execute(
            select(ProgressSnapshot).where(
                ProgressSnapshot.user_id == user_id,
                ProgressSnapshot.period == period,
                ProgressSnapshot.period_start == period_start,
            )
        )
        return result.scalar_one_or_none()

    async def list_by_user(self, user_id: uuid.UUID) -> list[ProgressSnapshot]:
        result = await self._session.execute(
            select(ProgressSnapshot)
            .where(ProgressSnapshot.user_id == user_id)
            .order_by(ProgressSnapshot.period_start.desc())
        )
        return list(result.scalars().all())

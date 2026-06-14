from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.progress_snapshot import ProgressSnapshot
from backend.repositories.progress_snapshot import ProgressSnapshotRepository


class ProgressService:
    def __init__(self, session: AsyncSession) -> None:
        self._snapshots = ProgressSnapshotRepository(session)

    async def create_snapshot(
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
        return await self._snapshots.create(
            user_id=user_id,
            period=period,
            period_start=period_start,
            period_end=period_end,
            sum_xe=sum_xe,
            sum_bje=sum_bje,
            sum_insulin=sum_insulin,
            trend=trend,
            sum_proteins=sum_proteins,
            sum_fats=sum_fats,
            sum_carbs=sum_carbs,
            comment=comment,
        )

    async def list_snapshots(self, user_id: uuid.UUID) -> list[ProgressSnapshot]:
        return await self._snapshots.list_by_user(user_id)

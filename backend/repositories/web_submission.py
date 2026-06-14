from dataclasses import dataclass
from datetime import datetime
from typing import cast
from uuid import UUID

from sqlalchemy import Numeric, func, literal, select, union_all
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.food_event import FoodEvent
from backend.models.photo_analysis import PhotoAnalysis
from backend.models.user import User


from backend.schemas.web import SubmissionType


@dataclass(frozen=True)
class SubmissionRow:
    id: UUID
    submission_type: SubmissionType
    user_id: UUID
    display_name: str | None
    title: str
    xe: float | None
    bje: float | None
    confidence: float | None
    recorded_at: datetime


class WebSubmissionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _combined_query(self, user_ids: list[UUID]):
        food_q = select(
            FoodEvent.id.label("id"),
            literal("food_event").label("submission_type"),
            FoodEvent.user_id.label("user_id"),
            FoodEvent.description.label("title"),
            FoodEvent.xe.label("xe"),
            FoodEvent.bje.label("bje"),
            literal(None).cast(Numeric(10, 2)).label("confidence"),
            FoodEvent.recorded_at.label("recorded_at"),
        ).where(FoodEvent.user_id.in_(user_ids))

        photo_q = select(
            PhotoAnalysis.id.label("id"),
            literal("photo_analysis").label("submission_type"),
            PhotoAnalysis.user_id.label("user_id"),
            literal("Photo analysis").label("title"),
            PhotoAnalysis.xe.label("xe"),
            PhotoAnalysis.bje.label("bje"),
            PhotoAnalysis.confidence.label("confidence"),
            PhotoAnalysis.created_at.label("recorded_at"),
        ).where(PhotoAnalysis.user_id.in_(user_ids))

        return union_all(food_q, photo_q).subquery("submissions")

    async def list_for_users(
        self,
        user_ids: list[UUID],
        *,
        limit: int,
        offset: int,
    ) -> tuple[list[SubmissionRow], int]:
        if not user_ids:
            return [], 0

        combined = self._combined_query(user_ids)
        total = await self._session.scalar(select(func.count()).select_from(combined))

        result = await self._session.execute(
            select(
                combined.c.id,
                combined.c.submission_type,
                combined.c.user_id,
                User.display_name,
                combined.c.title,
                combined.c.xe,
                combined.c.bje,
                combined.c.confidence,
                combined.c.recorded_at,
            )
            .join(User, User.id == combined.c.user_id)
            .order_by(combined.c.recorded_at.desc())
            .limit(limit)
            .offset(offset)
        )

        rows = [
            SubmissionRow(
                id=row.id,
                submission_type=cast(SubmissionType, row.submission_type),
                user_id=row.user_id,
                display_name=row.display_name,
                title=row.title,
                xe=float(row.xe) if row.xe is not None else None,
                bje=float(row.bje) if row.bje is not None else None,
                confidence=float(row.confidence) if row.confidence is not None else None,
                recorded_at=row.recorded_at,
            )
            for row in result.all()
        ]
        return rows, int(total or 0)

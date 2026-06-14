import uuid
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.photo_analysis import PhotoAnalysis
from backend.models.user import User


class PhotoAnalysisRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        user_id: uuid.UUID,
        request_id: uuid.UUID,
        object_type: str,
        comment: str | None = None,
        food_event_id: uuid.UUID | None = None,
        xe: float | None = None,
        bje: float | None = None,
        proteins: float | None = None,
        fats: float | None = None,
        carbs: float | None = None,
        confidence: float | None = None,
    ) -> PhotoAnalysis:
        analysis = PhotoAnalysis(
            user_id=user_id,
            request_id=request_id,
            food_event_id=food_event_id,
            object_type=object_type,
            xe=xe,
            bje=bje,
            proteins=proteins,
            fats=fats,
            carbs=carbs,
            confidence=confidence,
            comment=comment,
        )
        self._session.add(analysis)
        await self._session.flush()
        return analysis

    async def get_by_request_id(self, request_id: uuid.UUID) -> PhotoAnalysis | None:
        result = await self._session.execute(
            select(PhotoAnalysis).where(PhotoAnalysis.request_id == request_id)
        )
        return result.scalar_one_or_none()

    async def list_by_user_id(self, user_id: uuid.UUID) -> list[PhotoAnalysis]:
        result = await self._session.execute(
            select(PhotoAnalysis)
            .where(PhotoAnalysis.user_id == user_id)
            .order_by(PhotoAnalysis.created_at.desc())
        )
        return list(result.scalars().all())

    async def list_for_users_with_patient(
        self,
        user_ids: list[UUID],
    ) -> list[tuple[PhotoAnalysis, User]]:
        if not user_ids:
            return []
        result = await self._session.execute(
            select(PhotoAnalysis, User)
            .join(User, PhotoAnalysis.user_id == User.id)
            .where(PhotoAnalysis.user_id.in_(user_ids))
            .order_by(PhotoAnalysis.created_at.desc())
        )
        return list(result.all())

    async def count_for_users(self, user_ids: list[UUID]) -> int:
        if not user_ids:
            return 0
        result = await self._session.scalar(
            select(func.count())
            .select_from(PhotoAnalysis)
            .where(PhotoAnalysis.user_id.in_(user_ids))
        )
        return int(result or 0)

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.photo_analysis import PhotoAnalysis


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

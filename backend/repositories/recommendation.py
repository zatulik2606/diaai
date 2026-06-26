import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.recommendation import Recommendation


class RecommendationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        user_id: uuid.UUID,
        text: str,
        type: str,
        request_id: uuid.UUID | None = None,
    ) -> Recommendation:
        recommendation = Recommendation(
            user_id=user_id,
            text=text,
            type=type,
            request_id=request_id,
        )
        self._session.add(recommendation)
        await self._session.flush()
        return recommendation

    async def list_by_user(self, user_id: uuid.UUID) -> list[Recommendation]:
        result = await self._session.execute(
            select(Recommendation)
            .where(Recommendation.user_id == user_id)
            .order_by(Recommendation.created_at.desc())
        )
        return list(result.scalars().all())

    async def list_by_user_paged(
        self,
        user_id: uuid.UUID,
        *,
        limit: int,
        offset: int,
    ) -> tuple[list[Recommendation], int]:
        total_result = await self._session.scalar(
            select(func.count())
            .select_from(Recommendation)
            .where(Recommendation.user_id == user_id)
        )
        result = await self._session.execute(
            select(Recommendation)
            .where(Recommendation.user_id == user_id)
            .order_by(Recommendation.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all()), int(total_result or 0)

from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import verify_service_token
from backend.database import get_db
from backend.schemas.analytics import (
    AnalyticsProgressResponse,
    AnalyticsRecommendationsResponse,
    AnalyticsSignalsResponse,
)
from backend.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/progress", response_model=AnalyticsProgressResponse)
async def get_analytics_progress(
    telegram_id: int = Query(...),
    period: Literal["day", "week", "month"] = Query(default="week"),
    _: None = Depends(verify_service_token),
    db: AsyncSession = Depends(get_db),
) -> AnalyticsProgressResponse:
    service = AnalyticsService(db)
    return await service.get_progress(telegram_id, period)


@router.get("/signals", response_model=AnalyticsSignalsResponse)
async def get_analytics_signals(
    telegram_id: int = Query(...),
    period: Literal["week", "month"] = Query(default="week"),
    _: None = Depends(verify_service_token),
    db: AsyncSession = Depends(get_db),
) -> AnalyticsSignalsResponse:
    service = AnalyticsService(db)
    return await service.get_signals(telegram_id, period)


@router.get("/recommendations", response_model=AnalyticsRecommendationsResponse)
async def get_analytics_recommendations(
    telegram_id: int = Query(...),
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    _: None = Depends(verify_service_token),
    db: AsyncSession = Depends(get_db),
) -> AnalyticsRecommendationsResponse:
    service = AnalyticsService(db)
    return await service.get_recommendations(telegram_id, limit=limit, offset=offset)

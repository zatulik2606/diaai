from fastapi import APIRouter, Depends

from backend.api.deps import verify_service_token
from backend.api.v1.web.deps import require_leaderboard_viewer
from backend.models.user import User
from backend.schemas.analytics_query import AnalyticsQueryRequest, AnalyticsQueryResponse
from backend.services.analytics_query_service import (
    AnalyticsQueryService,
    get_analytics_query_service,
)

router = APIRouter(prefix="/analytics", tags=["web"])


@router.post("/query", response_model=AnalyticsQueryResponse)
async def analytics_query(
    body: AnalyticsQueryRequest,
    viewer: User = Depends(require_leaderboard_viewer),
    _: None = Depends(verify_service_token),
    service: AnalyticsQueryService = Depends(get_analytics_query_service),
) -> AnalyticsQueryResponse:
    return await service.query(viewer, body.question)

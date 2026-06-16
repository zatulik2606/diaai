from fastapi import APIRouter, Depends, Query

from backend.api.deps import verify_service_token
from backend.api.v1.web.deps import require_leaderboard_viewer
from backend.api.v1.web.service_deps import get_web_leaderboard_service
from backend.models.user import User
from backend.schemas.web import LeaderboardPeriod, LeaderboardResponse, MetricKey
from backend.services.web_leaderboard_service import WebLeaderboardService

router = APIRouter(prefix="/leaderboard", tags=["web"])


@router.get("", response_model=LeaderboardResponse)
async def get_leaderboard(
    _viewer: User = Depends(require_leaderboard_viewer),
    period: LeaderboardPeriod = Query(default="30d"),
    metric: MetricKey = Query(default="xe"),
    metric_x: MetricKey = Query(default="xe"),
    metric_y: MetricKey = Query(default="insulin_dose"),
    _: None = Depends(verify_service_token),
    service: WebLeaderboardService = Depends(get_web_leaderboard_service),
) -> LeaderboardResponse:
    return await service.get_leaderboard(
        period=period,
        metric=metric,
        metric_x=metric_x,
        metric_y=metric_y,
    )

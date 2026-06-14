from typing import Annotated

from fastapi import APIRouter, Depends, Query

from backend.api.deps import verify_service_token
from backend.api.v1.web.service_deps import get_web_chat_service
from backend.schemas.web import PaginatedHistoryResponse
from backend.services.web_chat_service import WebChatService
from backend.services.web_utils import clamp_limit, clamp_offset

router = APIRouter(prefix="/assistant", tags=["web"])

HistoryLimitParam = Annotated[int, Query(ge=1, le=100, description="Messages per page (max 100)")]
OffsetParam = Annotated[int, Query(ge=0)]


@router.get("/history", response_model=PaginatedHistoryResponse)
async def assistant_history(
    telegram_id: int,
    limit: HistoryLimitParam = 50,
    offset: OffsetParam = 0,
    _: None = Depends(verify_service_token),
    service: WebChatService = Depends(get_web_chat_service),
) -> PaginatedHistoryResponse:
    return await service.get_history(
        telegram_id=telegram_id,
        limit=clamp_limit(limit, default=50),
        offset=clamp_offset(offset),
    )

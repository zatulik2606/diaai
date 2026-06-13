from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import verify_service_token
from backend.config import Settings, get_settings
from backend.database import get_db
from backend.exceptions import AppError
from backend.schemas.assistant import AssistantMessageRequest, AssistantMessageResponse
from backend.services.assistant_service import AssistantService
from backend.services.llm_service import LlmService, get_llm_service

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("/messages", response_model=AssistantMessageResponse)
async def post_assistant_message(
    body: AssistantMessageRequest,
    _: None = Depends(verify_service_token),
    db: AsyncSession = Depends(get_db),
    llm: LlmService = Depends(get_llm_service),
    settings: Settings = Depends(get_settings),
) -> AssistantMessageResponse:
    has_text = body.text is not None and body.text.strip() != ""
    has_image = body.image_base64 is not None and body.image_base64.strip() != ""
    if not has_text and not has_image:
        raise AppError(
            code="BAD_REQUEST",
            message="Either text or image_base64 is required",
            status_code=400,
        )
    service = AssistantService(db, llm, settings)
    return await service.handle_message(body)

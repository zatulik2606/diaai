import logging

from fastapi import APIRouter, Depends, Request

from backend.api.deps import verify_service_token
from backend.schemas.media import TranscribeRequest, TranscribeResponse
from backend.services.transcribe_service import TranscribeService, get_transcribe_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/media", tags=["media"])


@router.post("/transcribe", response_model=TranscribeResponse)
async def post_transcribe(
    request: Request,
    body: TranscribeRequest,
    _: None = Depends(verify_service_token),
    transcribe: TranscribeService = Depends(get_transcribe_service),
) -> TranscribeResponse:
    request_id = getattr(request.state, "request_id", None)
    logger.info(
        "request_id=%s media_type=%s audio_b64_len=%s",
        request_id,
        body.media_type,
        len(body.audio_base64.strip()),
    )
    text = transcribe.transcribe(body.audio_base64.strip(), body.media_type)
    return TranscribeResponse(text=text)

from fastapi import APIRouter, Depends

from backend.api.deps import verify_service_token
from backend.exceptions import AppError
from backend.schemas.assistant import AssistantMessageRequest

router = APIRouter(prefix="/assistant", tags=["assistant"])


def _not_implemented() -> None:
    raise AppError(
        code="NOT_IMPLEMENTED",
        message="Endpoint not implemented yet",
        status_code=501,
    )


@router.post("/messages")
async def post_assistant_message(
    body: AssistantMessageRequest,
    _: None = Depends(verify_service_token),
) -> None:
    has_text = body.text is not None and body.text.strip() != ""
    has_image = body.image_base64 is not None and body.image_base64.strip() != ""
    if not has_text and not has_image:
        raise AppError(
            code="BAD_REQUEST",
            message="Either text or image_base64 is required",
            status_code=400,
        )
    _not_implemented()

from fastapi import APIRouter, Depends

from backend.api.deps import verify_service_token
from backend.api.v1.web.service_deps import get_web_auth_service
from backend.schemas.web import AuthResolveRequest, AuthResolveResponse
from backend.services.web_auth_service import WebAuthService

router = APIRouter(prefix="/auth", tags=["web"])


@router.post("/resolve", response_model=AuthResolveResponse)
async def resolve_auth(
    body: AuthResolveRequest,
    _: None = Depends(verify_service_token),
    service: WebAuthService = Depends(get_web_auth_service),
) -> AuthResolveResponse:
    return await service.resolve_username(body.username)

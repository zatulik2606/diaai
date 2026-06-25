"""Protected GlitchTip smoke route — not part of public API contract."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.config import Settings, get_settings

_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix="/debug", tags=["debug"], include_in_schema=False)


def _verify_debug_token(
    credentials: HTTPAuthorizationCredentials | None,
    settings: Settings,
) -> None:
    if not settings.glitchtip_debug_token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if credentials is None or credentials.credentials != settings.glitchtip_debug_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


@router.get("/glitchtip-test")
async def glitchtip_test(
    settings: Settings = Depends(get_settings),
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> dict[str, bool | str]:
    _verify_debug_token(credentials, settings)
    if not settings.glitchtip_dsn:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="GlitchTip is not configured",
        )

    import sentry_sdk

    sentry_sdk.capture_message("diaai glitchtip test: backend", level="info")
    return {"ok": True, "project": "diaai-backend"}


def include_debug_routes(app, settings: Settings) -> None:
    if settings.glitchtip_debug_token:
        app.include_router(router)

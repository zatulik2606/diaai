"""Shared API dependencies."""

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.config import Settings, get_settings
from backend.exceptions import AppError

_bearer = HTTPBearer(auto_error=False)


def verify_service_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    settings: Settings = Depends(get_settings),
) -> None:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AppError(
            code="UNAUTHORIZED",
            message="Missing or invalid authorization",
            status_code=401,
        )
    if credentials.credentials != settings.backend_service_token:
        raise AppError(
            code="UNAUTHORIZED",
            message="Invalid service token",
            status_code=401,
        )

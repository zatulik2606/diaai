import pytest

from backend.config import Settings, validate_service_token


def test_validate_service_token_rejects_change_me() -> None:
    settings = Settings(backend_service_token="change-me")
    with pytest.raises(RuntimeError, match="BACKEND_SERVICE_TOKEN"):
        validate_service_token(settings)


def test_validate_service_token_accepts_custom() -> None:
    settings = Settings(backend_service_token="secure-random-token")
    validate_service_token(settings)

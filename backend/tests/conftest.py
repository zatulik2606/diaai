import pytest
from httpx import ASGITransport, AsyncClient

from backend.config import get_settings
from backend.main import create_app

# Task-05: override get_db here (sqlite memory or test container)


@pytest.fixture(autouse=True)
def _settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BACKEND_SERVICE_TOKEN", "test-token")
    get_settings.cache_clear()


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def auth_headers() -> dict[str, str]:
    return {"Authorization": "Bearer test-token"}


@pytest.fixture
def invalid_auth_headers() -> dict[str, str]:
    return {"Authorization": "Bearer wrong-token"}


@pytest.fixture
def assistant_text_payload() -> dict:
    return {"telegram_id": 123456789, "text": "Сколько ХЕ?"}


@pytest.fixture
def assistant_photo_payload() -> dict:
    return {
        "telegram_id": 123456789,
        "text": "Оцени фото",
        "image_base64": "abc123",
    }


@pytest.fixture
def food_event_payload() -> dict:
    return {
        "telegram_id": 123456789,
        "description": "борщ",
        "xe": 3.5,
        "bje": 1.0,
        "source": "text",
    }


@pytest.fixture
def insulin_event_payload() -> dict:
    return {"telegram_id": 123456789, "dose": 4.0}

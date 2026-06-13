import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.config import get_settings
from backend.database import Base, get_db
from backend.main import create_app
from backend.services.llm_service import LlmService, get_llm_service

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


class MockLlmService(LlmService):
    def __init__(self) -> None:
        self._model = "mock"
        self._client = None

    def generate_reply(self, system_prompt, history, user_content) -> str:
        return "Тестовый ответ ассистента."


@pytest.fixture(autouse=True)
def _settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BACKEND_SERVICE_TOKEN", "test-token")
    monkeypatch.delenv("DATABASE_URL", raising=False)
    get_settings.cache_clear()


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def client(app):
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_db():
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_llm_service] = MockLlmService

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
    await engine.dispose()


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

import base64

import pytest
from fastapi import Depends
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.config import get_settings
from backend.database import Base, get_db
from backend.main import create_app
from backend.models import (  # noqa: F401
    Consultation,
    Dialog,
    DialogRequest,
    FoodEvent,
    InsulinEvent,
    PhotoAnalysis,
    ProgressSnapshot,
    Recommendation,
    User,
)
from backend.services.analytics_query_service import (
    AnalyticsQueryService,
    get_analytics_query_service,
)
from backend.services.llm_service import LlmService, get_llm_service
from backend.services.sql_guard import SqlGuard
from backend.services.transcribe_service import TranscribeService, get_transcribe_service

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


class MockLlmService(LlmService):
    def __init__(self) -> None:
        self._model = "mock"
        self._client = None

    def generate_reply(self, system_prompt, history, user_content) -> str:
        return "Тестовый ответ ассистента."


class MockTranscribeService(TranscribeService):
    def __init__(self) -> None:
        self._model = "mock"
        self._client = None

    def transcribe(self, audio_base64: str, media_type: str) -> str:
        return "Распознанный текст из голоса"


class MockAnalyticsQueryService(AnalyticsQueryService):
    def __init__(self, db) -> None:
        super().__init__(
            db,
            MockLlmService(),
            sql_guard=SqlGuard(max_row_limit=100),
            query_timeout_seconds=5.0,
            llm_timeout_seconds=30.0,
        )

    async def _generate_sql(self, viewer, question: str) -> str:
        lowered = question.lower()
        if "удали" in lowered or "delete" in lowered:
            return "DELETE FROM food_events"
        if "pg_catalog" in lowered:
            return "SELECT * FROM pg_catalog.pg_tables LIMIT 1"

        if viewer.role == "diabetic":
            tid = viewer.telegram_id
            return (
                "SELECT COALESCE(SUM(xe), 0) AS total_xe FROM food_events "
                f"WHERE user_id = (SELECT id FROM users WHERE telegram_id = {tid})"
            )
        if "топ" in lowered:
            return (
                "SELECT u.display_name, SUM(f.xe) AS total_xe "
                "FROM food_events f "
                "JOIN users u ON u.id = f.user_id "
                "WHERE u.role = 'diabetic' "
                "GROUP BY u.display_name "
                "ORDER BY total_xe DESC LIMIT 3"
            )
        return (
            "SELECT COALESCE(SUM(f.xe), 0) AS total_xe "
            "FROM food_events f "
            "JOIN users u ON u.id = f.user_id "
            "WHERE u.display_name LIKE '%Иван%'"
        )


@pytest.fixture(autouse=True)
def _settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BACKEND_SERVICE_TOKEN", "test-token")
    monkeypatch.delenv("DATABASE_URL", raising=False)
    get_settings.cache_clear()


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def db_engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def client(app, db_engine, db_session_factory):
    import backend.database as db_module

    prev_engine, prev_local = db_module.engine, db_module.AsyncSessionLocal
    db_module.engine = db_engine
    db_module.AsyncSessionLocal = db_session_factory

    async def override_get_db():
        async with db_session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def override_analytics(db=Depends(get_db)):
        return MockAnalyticsQueryService(db)

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_llm_service] = MockLlmService
    app.dependency_overrides[get_transcribe_service] = MockTranscribeService
    app.dependency_overrides[get_analytics_query_service] = override_analytics

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
    db_module.engine = prev_engine
    db_module.AsyncSessionLocal = prev_local


@pytest.fixture
def db_session_factory(db_engine):
    return async_sessionmaker(db_engine, expire_on_commit=False)


@pytest.fixture
async def db_session(db_session_factory):
    async with db_session_factory() as session:
        yield session


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
        "image_base64": base64.b64encode(b"fake-image-bytes").decode(),
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

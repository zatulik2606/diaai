from datetime import UTC, date, datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.database import Base
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
from backend.repositories.photo_analysis import PhotoAnalysisRepository
from backend.repositories.user import UserRepository
from backend.services.consultation_service import ConsultationService
from backend.services.progress_service import ProgressService

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def session() -> AsyncSession:
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as db_session:
        yield db_session

    await engine.dispose()


@pytest.mark.asyncio
async def test_user_create_doctor(session: AsyncSession) -> None:
    repo = UserRepository(session)
    doctor = await repo.create_doctor(display_name="Dr. Test", email="dr@test.example")
    await session.commit()
    assert doctor.role == "doctor"
    assert doctor.display_name == "Dr. Test"
    assert doctor.telegram_id is None


@pytest.mark.asyncio
async def test_photo_analysis_repository(session: AsyncSession) -> None:
    users = UserRepository(session)
    diabetic = await users.get_or_create(111)
    await session.commit()

    repo = PhotoAnalysisRepository(session)

    dialog = Dialog(user_id=diabetic.id)
    session.add(dialog)
    await session.flush()
    req = DialogRequest(
        dialog_id=dialog.id,
        user_id=diabetic.id,
        type="photo",
        reply="reply",
    )
    session.add(req)
    await session.flush()

    analysis = await repo.create(
        user_id=diabetic.id,
        request_id=req.id,
        object_type="dish",
        comment="test",
    )
    await session.commit()

    found = await repo.get_by_request_id(req.id)
    assert found is not None
    assert found.id == analysis.id


@pytest.mark.asyncio
async def test_progress_snapshot_service(session: AsyncSession) -> None:
    users = UserRepository(session)
    user = await users.get_or_create(222)
    await session.commit()

    service = ProgressService(session)
    snapshot = await service.create_snapshot(
        user_id=user.id,
        period="week",
        period_start=date(2026, 5, 1),
        period_end=date(2026, 5, 7),
        sum_xe=10.0,
        sum_bje=5.0,
        sum_insulin=20.0,
        trend="stable",
    )
    await session.commit()

    listed = await service.list_snapshots(user.id)
    assert len(listed) == 1
    assert listed[0].id == snapshot.id


@pytest.mark.asyncio
async def test_consultation_service(session: AsyncSession) -> None:
    users = UserRepository(session)
    diabetic = await users.get_or_create(333)
    doctor = await users.create_doctor(display_name="Doc")
    await session.commit()

    service = ConsultationService(session)
    consultation = await service.create(
        diabetic_id=diabetic.id,
        doctor_id=doctor.id,
        format="online",
        scheduled_at=datetime(2026, 6, 1, 10, 0, tzinfo=UTC),
    )
    await session.commit()

    for_doctor = await service.list_for_doctor(doctor.id)
    assert len(for_doctor) == 1
    assert for_doctor[0].id == consultation.id

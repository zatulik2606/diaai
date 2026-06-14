from datetime import UTC, date, datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.dialog import Dialog
from backend.models.request import DialogRequest
from backend.repositories.photo_analysis import PhotoAnalysisRepository
from backend.repositories.user import UserRepository
from backend.services.consultation_service import ConsultationService
from backend.services.progress_service import ProgressService

pytestmark = pytest.mark.unit


@pytest.mark.asyncio
async def test_user_create_doctor(db_session: AsyncSession) -> None:
    repo = UserRepository(db_session)
    doctor = await repo.create_doctor(display_name="Dr. Test", email="dr@test.example")
    await db_session.commit()
    assert doctor.role == "doctor"
    assert doctor.display_name == "Dr. Test"
    assert doctor.telegram_id is None


@pytest.mark.asyncio
async def test_photo_analysis_repository(db_session: AsyncSession) -> None:
    users = UserRepository(db_session)
    diabetic = await users.get_or_create(111)
    await db_session.commit()

    repo = PhotoAnalysisRepository(db_session)

    dialog = Dialog(user_id=diabetic.id)
    db_session.add(dialog)
    await db_session.flush()
    req = DialogRequest(
        dialog_id=dialog.id,
        user_id=diabetic.id,
        type="photo",
        reply="reply",
    )
    db_session.add(req)
    await db_session.flush()

    analysis = await repo.create(
        user_id=diabetic.id,
        request_id=req.id,
        object_type="dish",
        comment="test",
    )
    await db_session.commit()

    found = await repo.get_by_request_id(req.id)
    assert found is not None
    assert found.id == analysis.id


@pytest.mark.asyncio
async def test_progress_snapshot_service(db_session: AsyncSession) -> None:
    users = UserRepository(db_session)
    user = await users.get_or_create(222)
    await db_session.commit()

    service = ProgressService(db_session)
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
    await db_session.commit()

    listed = await service.list_snapshots(user.id)
    assert len(listed) == 1
    assert listed[0].id == snapshot.id


@pytest.mark.asyncio
async def test_consultation_service(db_session: AsyncSession) -> None:
    users = UserRepository(db_session)
    diabetic = await users.get_or_create(333)
    doctor = await users.create_doctor(display_name="Doc")
    await db_session.commit()

    service = ConsultationService(db_session)
    consultation = await service.create(
        diabetic_id=diabetic.id,
        doctor_id=doctor.id,
        format="online",
        scheduled_at=datetime(2026, 6, 1, 10, 0, tzinfo=UTC),
    )
    await db_session.commit()

    for_doctor = await service.list_for_doctor(doctor.id)
    assert len(for_doctor) == 1
    assert for_doctor[0].id == consultation.id

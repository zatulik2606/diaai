"""Patient dashboard web API contract tests."""

import uuid
from datetime import UTC, datetime, timedelta

import pytest

pytestmark = pytest.mark.integration

PATIENT_TELEGRAM_ID = 900000001
PATIENT_USERNAME = "ivan_p"
DOCTOR_TELEGRAM_ID = 162684825


@pytest.fixture
async def patient_demo_data(db_session):
    from backend.models.dialog import Dialog
    from backend.models.food_event import FoodEvent
    from backend.models.progress_snapshot import ProgressSnapshot
    from backend.models.request import DialogRequest
    from backend.models.user import User

    patient = User(
        id=uuid.UUID("a1000001-0000-4000-8000-000000000001"),
        telegram_id=PATIENT_TELEGRAM_ID,
        telegram_username=PATIENT_USERNAME,
        role="diabetic",
        display_name="Иван П.",
    )
    doctor = User(
        id=uuid.UUID("a1000001-0000-4000-8000-000000000010"),
        telegram_id=DOCTOR_TELEGRAM_ID,
        telegram_username="doctor_ivanov",
        role="doctor",
        display_name="Doctor Ivanov",
    )
    db_session.add_all([patient, doctor])

    now = datetime.now(UTC)
    food = FoodEvent(
        id=uuid.uuid4(),
        user_id=patient.id,
        description="Овсянка",
        xe=2.5,
        bje=1.0,
        source="text",
        recorded_at=now - timedelta(days=1),
    )
    db_session.add(food)

    dialog = Dialog(id=uuid.uuid4(), user_id=patient.id)
    db_session.add(dialog)
    await db_session.flush()

    request = DialogRequest(
        id=uuid.uuid4(),
        dialog_id=dialog.id,
        user_id=patient.id,
        type="text",
        content="Сколько ХЕ в яблоке?",
        reply="Около 1–1.5 ХЕ.",
        created_at=now - timedelta(hours=2),
    )
    db_session.add(request)

    snapshot = ProgressSnapshot(
        id=uuid.uuid4(),
        user_id=patient.id,
        period="week",
        period_start=(now - timedelta(days=7)).date(),
        period_end=now.date(),
        sum_xe=72.0,
        sum_bje=90.0,
        sum_insulin=25.0,
        trend="stable",
    )
    db_session.add(snapshot)
    await db_session.commit()
    return {"patient": patient, "doctor": doctor}


@pytest.mark.asyncio
async def test_patient_summary(client, auth_headers, patient_demo_data) -> None:
    response = await client.get(
        "/api/v1/web/patient/dashboard/summary",
        headers=auth_headers,
        params={"patient_telegram_id": PATIENT_TELEGRAM_ID},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["period_days"] == 7
    kpi_ids = {kpi["id"] for kpi in body["kpis"]}
    assert kpi_ids == {
        "total_xe",
        "questions_count",
        "food_events_count",
        "insulin_total",
    }


@pytest.mark.asyncio
async def test_patient_activity(client, auth_headers, patient_demo_data) -> None:
    response = await client.get(
        "/api/v1/web/patient/dashboard/activity",
        headers=auth_headers,
        params={"patient_telegram_id": PATIENT_TELEGRAM_ID, "days": 14},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["days"] == 14
    assert len(body["series"]) == 14


@pytest.mark.asyncio
async def test_patient_questions(client, auth_headers, patient_demo_data) -> None:
    response = await client.get(
        "/api/v1/web/patient/dashboard/questions",
        headers=auth_headers,
        params={"patient_telegram_id": PATIENT_TELEGRAM_ID},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] >= 1
    assert "patient" not in body["items"][0]
    assert body["items"][0]["content"] == "Сколько ХЕ в яблоке?"


@pytest.mark.asyncio
async def test_patient_submissions(client, auth_headers, patient_demo_data) -> None:
    response = await client.get(
        "/api/v1/web/patient/dashboard/submissions",
        headers=auth_headers,
        params={"patient_telegram_id": PATIENT_TELEGRAM_ID},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] >= 1
    assert "patient" not in body["items"][0]


@pytest.mark.asyncio
async def test_patient_progress_matrix(client, auth_headers, patient_demo_data) -> None:
    response = await client.get(
        "/api/v1/web/patient/dashboard/progress-matrix",
        headers=auth_headers,
        params={"patient_telegram_id": PATIENT_TELEGRAM_ID},
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body["rows"]) == 3
    metric_ids = {row["metric_id"] for row in body["rows"]}
    assert metric_ids == {"xe", "bje", "insulin"}


@pytest.mark.asyncio
async def test_patient_forbidden_for_doctor(client, auth_headers, patient_demo_data) -> None:
    response = await client.get(
        "/api/v1/web/patient/dashboard/summary",
        headers=auth_headers,
        params={"patient_telegram_id": DOCTOR_TELEGRAM_ID},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_patient_not_found(client, auth_headers, patient_demo_data) -> None:
    response = await client.get(
        "/api/v1/web/patient/dashboard/summary",
        headers=auth_headers,
        params={"patient_telegram_id": 999999999},
    )
    assert response.status_code == 404

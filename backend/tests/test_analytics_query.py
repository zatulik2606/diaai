"""Analytics query API and SqlGuard tests."""

import uuid
from datetime import UTC, datetime, timedelta

import pytest

from backend.exceptions import AppError
from backend.services.sql_guard import SqlGuard

pytestmark = pytest.mark.integration

PATIENT_TELEGRAM_ID = 900000001
DOCTOR_TELEGRAM_ID = 162684825


@pytest.fixture
async def analytics_demo_data(db_session):
    from backend.models.food_event import FoodEvent
    from backend.models.user import User

    patient_a = User(
        id=uuid.UUID("a1000001-0000-4000-8000-000000000001"),
        telegram_id=PATIENT_TELEGRAM_ID,
        telegram_username="ivan_p",
        role="diabetic",
        display_name="Иван П.",
    )
    patient_b = User(
        id=uuid.UUID("a1000001-0000-4000-8000-000000000002"),
        telegram_id=900000002,
        telegram_username="maria_p",
        role="diabetic",
        display_name="Мария С.",
    )
    doctor = User(
        id=uuid.UUID("a1000001-0000-4000-8000-000000000010"),
        telegram_id=DOCTOR_TELEGRAM_ID,
        telegram_username="doctor_ivanov",
        role="doctor",
        display_name="Doctor Ivanov",
    )
    db_session.add_all([patient_a, patient_b, doctor])

    now = datetime.now(UTC)
    db_session.add_all(
        [
            FoodEvent(
                id=uuid.uuid4(),
                user_id=patient_a.id,
                description="Овсянка",
                xe=2.5,
                bje=1.0,
                source="text",
                recorded_at=now - timedelta(days=1),
            ),
            FoodEvent(
                id=uuid.uuid4(),
                user_id=patient_a.id,
                description="Яблоко",
                xe=1.0,
                bje=0.5,
                source="text",
                recorded_at=now - timedelta(days=2),
            ),
            FoodEvent(
                id=uuid.uuid4(),
                user_id=patient_b.id,
                description="Суп",
                xe=5.0,
                bje=2.0,
                source="text",
                recorded_at=now - timedelta(days=1),
            ),
        ]
    )
    await db_session.commit()
    return {"patient_a": patient_a, "patient_b": patient_b, "doctor": doctor}


def test_sql_guard_rejects_delete() -> None:
    guard = SqlGuard()
    with pytest.raises(AppError) as exc:
        guard.validate_and_enforce("DELETE FROM food_events")
    assert exc.value.code == "INVALID_SQL"


def test_sql_guard_rejects_system_catalog() -> None:
    guard = SqlGuard()
    with pytest.raises(AppError) as exc:
        guard.validate_and_enforce("SELECT * FROM pg_catalog.pg_tables LIMIT 1")
    assert exc.value.code == "INVALID_SQL"


def test_sql_guard_enforces_limit() -> None:
    guard = SqlGuard(max_row_limit=100)
    sql = guard.validate_and_enforce("SELECT xe FROM food_events")
    assert "LIMIT" in sql.upper()


def test_sql_guard_rejects_unknown_table() -> None:
    guard = SqlGuard()
    with pytest.raises(AppError) as exc:
        guard.validate_and_enforce("SELECT * FROM consultations LIMIT 1")
    assert exc.value.code == "INVALID_SQL"


@pytest.mark.asyncio
async def test_patient_analytics_query_golden(client, auth_headers, analytics_demo_data) -> None:
    response = await client.post(
        "/api/v1/web/analytics/query",
        headers=auth_headers,
        params={"patient_telegram_id": PATIENT_TELEGRAM_ID},
        json={"question": "Сколько ХЕ я съел за последние 7 дней?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["chart_hint"] == "scalar"
    assert float(body["rows"][0][0]) == pytest.approx(3.5)


@pytest.mark.asyncio
async def test_doctor_analytics_query_patient_golden(
    client, auth_headers, analytics_demo_data
) -> None:
    response = await client.post(
        "/api/v1/web/analytics/query",
        headers=auth_headers,
        params={"doctor_telegram_id": DOCTOR_TELEGRAM_ID},
        json={"question": "Сколько ХЕ за неделю у Иван П.?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert float(body["rows"][0][0]) == pytest.approx(3.5)


@pytest.mark.asyncio
async def test_doctor_analytics_query_top_golden(client, auth_headers, analytics_demo_data) -> None:
    response = await client.post(
        "/api/v1/web/analytics/query",
        headers=auth_headers,
        params={"doctor_telegram_id": DOCTOR_TELEGRAM_ID},
        json={"question": "Топ-3 пациента по ХЕ за 30 дней"},
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body["rows"]) >= 2
    assert body["chart_hint"] == "bar"


@pytest.mark.asyncio
async def test_analytics_query_empty_question_422(
    client, auth_headers, analytics_demo_data
) -> None:
    response = await client.post(
        "/api/v1/web/analytics/query",
        headers=auth_headers,
        params={"patient_telegram_id": PATIENT_TELEGRAM_ID},
        json={"question": "   "},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_analytics_query_delete_rejected(client, auth_headers, analytics_demo_data) -> None:
    response = await client.post(
        "/api/v1/web/analytics/query",
        headers=auth_headers,
        params={"patient_telegram_id": PATIENT_TELEGRAM_ID},
        json={"question": "Удали все события"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_analytics_query_unauthorized_401(
    client, invalid_auth_headers, analytics_demo_data
) -> None:
    response = await client.post(
        "/api/v1/web/analytics/query",
        headers=invalid_auth_headers,
        params={"patient_telegram_id": PATIENT_TELEGRAM_ID},
        json={"question": "Сколько ХЕ?"},
    )
    assert response.status_code == 401

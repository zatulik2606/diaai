"""Web API contract tests."""

import uuid
from datetime import UTC, datetime, timedelta

import pytest

pytestmark = pytest.mark.integration

DOCTOR_TELEGRAM_ID = 162684825
DOCTOR_USERNAME = "akozhin"
PATIENT_TELEGRAM_ID = 900000001


@pytest.fixture
async def web_demo_data(db_session):
    from backend.models.dialog import Dialog
    from backend.models.food_event import FoodEvent
    from backend.models.request import DialogRequest
    from backend.models.user import User

    doctor = User(
        id=uuid.UUID("a1000001-0000-4000-8000-000000000010"),
        telegram_id=DOCTOR_TELEGRAM_ID,
        telegram_username=DOCTOR_USERNAME,
        role="doctor",
        display_name="Александр Кожин",
    )
    patient = User(
        id=uuid.UUID("a1000001-0000-4000-8000-000000000001"),
        telegram_id=PATIENT_TELEGRAM_ID,
        telegram_username="ivan_p",
        role="diabetic",
        display_name="Иван П.",
    )
    diabetic_only = User(
        id=uuid.UUID("a1000001-0000-4000-8000-000000000099"),
        telegram_id=999999999,
        role="diabetic",
        display_name="Not Doctor",
    )
    db_session.add_all([doctor, patient, diabetic_only])

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
    await db_session.commit()
    return {"doctor": doctor, "patient": patient}


@pytest.mark.asyncio
async def test_auth_resolve_success(client, auth_headers, web_demo_data) -> None:
    response = await client.post(
        "/api/v1/web/auth/resolve",
        headers=auth_headers,
        json={"username": "akozhin"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["telegram_id"] == DOCTOR_TELEGRAM_ID
    assert body["role"] == "doctor"
    assert body["display_name"] == "Александр Кожин"


@pytest.mark.asyncio
async def test_auth_resolve_not_found(client, auth_headers, web_demo_data) -> None:
    response = await client.post(
        "/api/v1/web/auth/resolve",
        headers=auth_headers,
        json={"username": "unknown_user"},
    )
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_dashboard_summary_schema(client, auth_headers, web_demo_data) -> None:
    response = await client.get(
        "/api/v1/web/doctor/dashboard/summary",
        headers=auth_headers,
        params={"doctor_telegram_id": DOCTOR_TELEGRAM_ID},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["period_days"] == 7
    assert len(body["kpis"]) == 4
    kpi_ids = {kpi["id"] for kpi in body["kpis"]}
    assert kpi_ids == {
        "active_patients",
        "total_xe",
        "questions_count",
        "food_events_count",
    }


@pytest.mark.asyncio
async def test_dashboard_activity_series_length(client, auth_headers, web_demo_data) -> None:
    response = await client.get(
        "/api/v1/web/doctor/dashboard/activity",
        headers=auth_headers,
        params={"doctor_telegram_id": DOCTOR_TELEGRAM_ID, "days": 14},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["days"] == 14
    assert len(body["series"]) == 14


@pytest.mark.asyncio
async def test_dashboard_questions_pagination(client, auth_headers, web_demo_data) -> None:
    response = await client.get(
        "/api/v1/web/doctor/dashboard/questions",
        headers=auth_headers,
        params={"doctor_telegram_id": DOCTOR_TELEGRAM_ID, "limit": 10, "offset": 0},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["limit"] == 10
    assert body["offset"] == 0
    assert body["total"] >= 1
    assert body["items"][0]["patient"]["display_name"] == "Иван П."


@pytest.mark.asyncio
async def test_doctor_forbidden_for_diabetic(client, auth_headers, web_demo_data) -> None:
    response = await client.get(
        "/api/v1/web/doctor/dashboard/summary",
        headers=auth_headers,
        params={"doctor_telegram_id": PATIENT_TELEGRAM_ID},
    )
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"


@pytest.mark.asyncio
async def test_leaderboard_medals(client, auth_headers, web_demo_data) -> None:
    response = await client.get(
        "/api/v1/web/leaderboard",
        headers=auth_headers,
        params={"doctor_telegram_id": DOCTOR_TELEGRAM_ID},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["period"] == "30d"
    assert len(body["table"]) >= 1
    assert body["table"][0]["rank"] == 1
    if len(body["table"]) >= 3:
        medals = [row["medal"] for row in body["table"][:3]]
        assert medals == ["gold", "silver", "bronze"]


@pytest.mark.asyncio
async def test_assistant_history(client, auth_headers, web_demo_data) -> None:
    response = await client.get(
        "/api/v1/web/assistant/history",
        headers=auth_headers,
        params={"telegram_id": PATIENT_TELEGRAM_ID},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] >= 2
    roles = {item["role"] for item in body["items"]}
    assert roles == {"user", "assistant"}

"""Analytics REST API — /api/v1/analytics/* (backend iter 4)."""

import uuid
from datetime import UTC, datetime, timedelta

import pytest

pytestmark = pytest.mark.integration

PATIENT_TELEGRAM_ID = 900000001
DOCTOR_TELEGRAM_ID = 162684825
UNKNOWN_TELEGRAM_ID = 999999999


@pytest.fixture
async def analytics_demo_data(db_session):
    from backend.models.food_event import FoodEvent
    from backend.models.insulin_event import InsulinEvent
    from backend.models.recommendation import Recommendation
    from backend.models.user import User

    patient = User(
        id=uuid.UUID("b1000001-0000-4000-8000-000000000001"),
        telegram_id=PATIENT_TELEGRAM_ID,
        telegram_username="ivan_p",
        role="diabetic",
        display_name="Иван П.",
    )
    doctor = User(
        id=uuid.UUID("b1000002-0000-4000-8000-000000000002"),
        telegram_id=DOCTOR_TELEGRAM_ID,
        role="doctor",
        display_name="Доктор",
    )
    db_session.add_all([patient, doctor])
    await db_session.flush()

    now = datetime.now(UTC)
    db_session.add_all(
        [
            FoodEvent(
                user_id=patient.id,
                description="борщ",
                xe=10.0,
                bje=3.0,
                source="text",
                recorded_at=now - timedelta(days=1),
            ),
            FoodEvent(
                user_id=patient.id,
                description="каша",
                xe=5.0,
                bje=1.5,
                source="text",
                recorded_at=now - timedelta(days=2),
            ),
            FoodEvent(
                user_id=patient.id,
                description="старый завтрак",
                xe=8.0,
                bje=2.0,
                source="text",
                recorded_at=now - timedelta(days=10),
            ),
            InsulinEvent(
                user_id=patient.id,
                dose=12.0,
                injected_at=now - timedelta(days=1),
            ),
            Recommendation(
                user_id=patient.id,
                type="nutrition",
                text="Сверьте перекусы с дневником — без назначения доз.",
            ),
        ]
    )
    await db_session.commit()
    return patient


@pytest.mark.asyncio
async def test_analytics_progress_ok(client, auth_headers, analytics_demo_data) -> None:
    response = await client.get(
        "/api/v1/analytics/progress",
        params={"telegram_id": PATIENT_TELEGRAM_ID, "period": "week"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["telegram_id"] == PATIENT_TELEGRAM_ID
    assert body["period"] == "week"
    assert body["sums"]["xe"] >= 15.0
    assert body["sums"]["insulin"] >= 12.0
    assert body["source"] == "computed"
    assert body["trend"] in {"improving", "stable", "worsening"}
    assert set(body["delta_pct"].keys()) == {"xe", "bje", "insulin"}


@pytest.mark.asyncio
async def test_analytics_progress_forbidden_doctor(
    client, auth_headers, analytics_demo_data
) -> None:
    response = await client.get(
        "/api/v1/analytics/progress",
        params={"telegram_id": DOCTOR_TELEGRAM_ID},
        headers=auth_headers,
    )
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"


@pytest.mark.asyncio
async def test_analytics_progress_not_found(client, auth_headers) -> None:
    response = await client.get(
        "/api/v1/analytics/progress",
        params={"telegram_id": UNKNOWN_TELEGRAM_ID},
        headers=auth_headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_analytics_signals_ok(client, auth_headers, analytics_demo_data) -> None:
    response = await client.get(
        "/api/v1/analytics/signals",
        params={"telegram_id": PATIENT_TELEGRAM_ID, "period": "week"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["telegram_id"] == PATIENT_TELEGRAM_ID
    assert len(body["signals"]) == 3
    codes = {s["code"] for s in body["signals"]}
    assert codes == {"xe_up", "bje_up", "insulin_up"} or "xe_stable" in codes


@pytest.mark.asyncio
async def test_analytics_recommendations_persisted(
    client, auth_headers, analytics_demo_data
) -> None:
    response = await client.get(
        "/api/v1/analytics/recommendations",
        params={"telegram_id": PATIENT_TELEGRAM_ID, "limit": 10},
        headers=auth_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] >= 1
    assert body["items"][0]["type"] == "nutrition"
    assert "доз" not in body["items"][0]["text"].lower() or "назначения" in body["items"][0]["text"]


@pytest.mark.asyncio
async def test_analytics_recommendations_rule_based_when_empty(
    client, auth_headers, analytics_demo_data
) -> None:
    response = await client.get(
        "/api/v1/analytics/recommendations",
        params={"telegram_id": PATIENT_TELEGRAM_ID, "limit": 5, "offset": 100},
        headers=auth_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["items"] == []


@pytest.mark.asyncio
async def test_analytics_unauthorized(client, invalid_auth_headers, analytics_demo_data) -> None:
    response = await client.get(
        "/api/v1/analytics/progress",
        params={"telegram_id": PATIENT_TELEGRAM_ID},
        headers=invalid_auth_headers,
    )
    assert response.status_code == 401

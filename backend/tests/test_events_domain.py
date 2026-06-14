import uuid

import pytest

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_food_foreign_request_id_returns_403(client, auth_headers) -> None:
    other_user = 111111111
    owner = 222222222
    msg = await client.post(
        "/api/v1/assistant/messages",
        headers=auth_headers,
        json={"telegram_id": owner, "text": "Привет"},
    )
    request_id = msg.json()["request_id"]

    response = await client.post(
        "/api/v1/events/food",
        headers=auth_headers,
        json={
            "telegram_id": other_user,
            "description": "борщ",
            "xe": 1.0,
            "bje": 0.5,
            "source": "text",
            "request_id": request_id,
        },
    )
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"


@pytest.mark.asyncio
async def test_food_unknown_request_id_returns_404(
    client, auth_headers, food_event_payload
) -> None:
    payload = {
        **food_event_payload,
        "request_id": str(uuid.uuid4()),
    }
    response = await client.post(
        "/api/v1/events/food",
        headers=auth_headers,
        json=payload,
    )
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_insulin_foreign_food_event_returns_403(client, auth_headers) -> None:
    owner = 333333333
    other_user = 444444444
    food = await client.post(
        "/api/v1/events/food",
        headers=auth_headers,
        json={
            "telegram_id": owner,
            "description": "суп",
            "xe": 2.0,
            "bje": 1.0,
            "source": "text",
        },
    )
    food_id = food.json()["id"]

    response = await client.post(
        "/api/v1/events/insulin",
        headers=auth_headers,
        json={
            "telegram_id": other_user,
            "dose": 3.0,
            "food_event_id": food_id,
        },
    )
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"


@pytest.mark.asyncio
async def test_insulin_unknown_food_event_returns_404(
    client, auth_headers, insulin_event_payload
) -> None:
    payload = {
        **insulin_event_payload,
        "food_event_id": str(uuid.uuid4()),
    }
    response = await client.post(
        "/api/v1/events/insulin",
        headers=auth_headers,
        json=payload,
    )
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"

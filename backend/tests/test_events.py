import pytest

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_create_food_returns_201(client, auth_headers, food_event_payload) -> None:
    response = await client.post(
        "/api/v1/events/food",
        headers=auth_headers,
        json=food_event_payload,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["recorded_at"]


@pytest.mark.asyncio
async def test_create_insulin_returns_201(client, auth_headers, insulin_event_payload) -> None:
    response = await client.post(
        "/api/v1/events/insulin",
        headers=auth_headers,
        json=insulin_event_payload,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["recorded_at"]


@pytest.mark.asyncio
async def test_list_food_returns_200(client, auth_headers, food_event_payload) -> None:
    await client.post(
        "/api/v1/events/food",
        headers=auth_headers,
        json=food_event_payload,
    )
    response = await client.get(
        "/api/v1/events/food",
        headers=auth_headers,
        params={"telegram_id": 123456789},
    )
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["description"] == "борщ"
    assert body[0]["telegram_id"] == 123456789

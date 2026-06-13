import pytest


@pytest.mark.asyncio
async def test_create_food_stub_501(client, auth_headers, food_event_payload) -> None:
    response = await client.post(
        "/api/v1/events/food",
        headers=auth_headers,
        json=food_event_payload,
    )
    assert response.status_code == 501
    assert response.json()["error"]["code"] == "NOT_IMPLEMENTED"


@pytest.mark.asyncio
async def test_create_insulin_stub_501(client, auth_headers, insulin_event_payload) -> None:
    response = await client.post(
        "/api/v1/events/insulin",
        headers=auth_headers,
        json=insulin_event_payload,
    )
    assert response.status_code == 501
    assert response.json()["error"]["code"] == "NOT_IMPLEMENTED"


@pytest.mark.asyncio
async def test_list_food_stub_501(client, auth_headers) -> None:
    response = await client.get(
        "/api/v1/events/food",
        headers=auth_headers,
        params={"telegram_id": 123456789},
    )
    assert response.status_code == 501
    assert response.json()["error"]["code"] == "NOT_IMPLEMENTED"

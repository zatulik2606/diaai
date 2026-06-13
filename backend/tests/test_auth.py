import pytest


@pytest.mark.asyncio
async def test_assistant_without_token_returns_401(client) -> None:
    response = await client.post(
        "/api/v1/assistant/messages",
        json={"telegram_id": 1, "text": "hello"},
    )
    assert response.status_code == 401
    body = response.json()
    assert body["error"]["code"] == "UNAUTHORIZED"


@pytest.mark.asyncio
async def test_invalid_bearer_on_assistant_returns_401(
    client, invalid_auth_headers, assistant_text_payload
) -> None:
    response = await client.post(
        "/api/v1/assistant/messages",
        headers=invalid_auth_headers,
        json=assistant_text_payload,
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


@pytest.mark.asyncio
async def test_invalid_bearer_on_food_returns_401(
    client, invalid_auth_headers, food_event_payload
) -> None:
    response = await client.post(
        "/api/v1/events/food",
        headers=invalid_auth_headers,
        json=food_event_payload,
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


@pytest.mark.asyncio
async def test_health_no_auth_required(client) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "1.0.0"}

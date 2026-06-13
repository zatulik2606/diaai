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

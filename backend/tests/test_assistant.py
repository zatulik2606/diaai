import pytest


@pytest.mark.asyncio
async def test_assistant_text_stub_501(client, auth_headers, assistant_text_payload) -> None:
    response = await client.post(
        "/api/v1/assistant/messages",
        headers=auth_headers,
        json=assistant_text_payload,
    )
    assert response.status_code == 501
    assert response.json()["error"]["code"] == "NOT_IMPLEMENTED"


@pytest.mark.asyncio
async def test_assistant_photo_stub_501(client, auth_headers, assistant_photo_payload) -> None:
    response = await client.post(
        "/api/v1/assistant/messages",
        headers=auth_headers,
        json=assistant_photo_payload,
    )
    assert response.status_code == 501
    assert response.json()["error"]["code"] == "NOT_IMPLEMENTED"


@pytest.mark.asyncio
async def test_assistant_empty_content_400(client, auth_headers) -> None:
    response = await client.post(
        "/api/v1/assistant/messages",
        headers=auth_headers,
        json={"telegram_id": 123456789},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "BAD_REQUEST"


@pytest.mark.asyncio
async def test_assistant_response_has_request_id_header(
    client, auth_headers, assistant_text_payload
) -> None:
    response = await client.post(
        "/api/v1/assistant/messages",
        headers={**auth_headers, "X-Request-Id": "test-req-id"},
        json=assistant_text_payload,
    )
    assert response.headers.get("x-request-id") == "test-req-id"

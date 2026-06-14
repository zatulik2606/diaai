import uuid

import pytest
from sqlalchemy import func, select

from backend.models.photo_analysis import PhotoAnalysis

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_assistant_text_returns_200(client, auth_headers, assistant_text_payload) -> None:
    response = await client.post(
        "/api/v1/assistant/messages",
        headers=auth_headers,
        json=assistant_text_payload,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["dialog_id"]
    assert body["request_id"]
    assert body["reply"] == "Тестовый ответ ассистента."


@pytest.mark.asyncio
async def test_assistant_photo_returns_200(client, auth_headers, assistant_photo_payload) -> None:
    response = await client.post(
        "/api/v1/assistant/messages",
        headers=auth_headers,
        json=assistant_photo_payload,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["dialog_id"]
    assert body["request_id"]
    assert body["reply"]


@pytest.mark.asyncio
async def test_assistant_photo_creates_photo_analysis(
    client, auth_headers, assistant_photo_payload, db_session_factory
) -> None:
    response = await client.post(
        "/api/v1/assistant/messages",
        headers=auth_headers,
        json=assistant_photo_payload,
    )
    assert response.status_code == 200
    request_id = uuid.UUID(response.json()["request_id"])

    async with db_session_factory() as session:
        result = await session.execute(
            select(PhotoAnalysis).where(PhotoAnalysis.request_id == request_id)
        )
        analysis = result.scalar_one_or_none()

    assert analysis is not None
    assert analysis.object_type == "dish"


@pytest.mark.asyncio
async def test_assistant_text_does_not_create_photo_analysis(
    client, auth_headers, assistant_text_payload, db_session_factory
) -> None:
    response = await client.post(
        "/api/v1/assistant/messages",
        headers=auth_headers,
        json=assistant_text_payload,
    )
    assert response.status_code == 200
    request_id = uuid.UUID(response.json()["request_id"])

    async with db_session_factory() as session:
        count = await session.scalar(
            select(func.count())
            .select_from(PhotoAnalysis)
            .where(PhotoAnalysis.request_id == request_id)
        )

    assert count == 0


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

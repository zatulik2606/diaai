import base64

import pytest


@pytest.mark.asyncio
async def test_assistant_missing_telegram_id_422(client, auth_headers) -> None:
    response = await client.post(
        "/api/v1/assistant/messages",
        headers=auth_headers,
        json={},
    )
    assert response.status_code == 422
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_food_missing_required_fields_422(client, auth_headers) -> None:
    response = await client.post(
        "/api/v1/events/food",
        headers=auth_headers,
        json={"telegram_id": 1},
    )
    assert response.status_code == 422
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_food_negative_xe_422(client, auth_headers, food_event_payload) -> None:
    payload = {**food_event_payload, "xe": -1}
    response = await client.post(
        "/api/v1/events/food",
        headers=auth_headers,
        json=payload,
    )
    assert response.status_code == 422
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_insulin_dose_zero_422(client, auth_headers, insulin_event_payload) -> None:
    payload = {**insulin_event_payload, "dose": 0}
    response = await client.post(
        "/api/v1/events/insulin",
        headers=auth_headers,
        json=payload,
    )
    assert response.status_code == 422
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_list_food_missing_telegram_id_422(client, auth_headers) -> None:
    response = await client.get("/api/v1/events/food", headers=auth_headers)
    assert response.status_code == 422
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_assistant_image_exceeds_5mb_422(client, auth_headers) -> None:
    oversized = base64.b64encode(b"x" * (5 * 1024 * 1024 + 1)).decode()
    response = await client.post(
        "/api/v1/assistant/messages",
        headers=auth_headers,
        json={"telegram_id": 123456789, "image_base64": oversized},
    )
    assert response.status_code == 422
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_assistant_invalid_base64_422(client, auth_headers) -> None:
    response = await client.post(
        "/api/v1/assistant/messages",
        headers=auth_headers,
        json={"telegram_id": 123456789, "image_base64": "not-valid-base64!!!"},
    )
    assert response.status_code == 422
    assert "detail" in response.json()

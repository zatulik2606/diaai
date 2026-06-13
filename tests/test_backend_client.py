from __future__ import annotations

from collections.abc import Callable

import httpx
import pytest

from diaai.backend_client import BackendClient, BackendClientError

Handler = Callable[[httpx.Request], httpx.Response]


async def _make_client(handler: Handler) -> BackendClient:
    transport = httpx.MockTransport(handler)
    client = BackendClient(base_url="http://test", service_token="test-token")
    await client._client.aclose()
    client._client = httpx.AsyncClient(transport=transport, base_url="http://test")
    return client


@pytest.mark.asyncio
async def test_send_assistant_message_returns_reply_on_200() -> None:
    client = await _make_client(
        lambda _request: httpx.Response(
            200,
            json={
                "dialog_id": "550e8400-e29b-41d4-a716-446655440000",
                "request_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                "reply": "  Ориентировочно 3 ХЕ  ",
            },
        )
    )
    try:
        reply = await client.send_assistant_message(123456789, text="Сколько ХЕ?")
        assert reply == "Ориентировочно 3 ХЕ"
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_send_assistant_message_sends_bearer_and_json_body() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["auth"] = request.headers.get("Authorization")
        captured["request_id"] = request.headers.get("X-Request-Id")
        captured["json"] = __import__("json").loads(request.content)
        return httpx.Response(
            200,
            json={"dialog_id": "d", "request_id": "r", "reply": "ok"},
        )

    client = await _make_client(handler)
    try:
        await client.send_assistant_message(42, text="hello")
        assert captured["auth"] == "Bearer test-token"
        assert captured["request_id"]
        assert captured["json"] == {"telegram_id": 42, "text": "hello"}
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_send_assistant_message_includes_photo_fields() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["json"] = __import__("json").loads(request.content)
        return httpx.Response(
            200,
            json={"dialog_id": "d", "request_id": "r", "reply": "photo ok"},
        )

    client = await _make_client(handler)
    try:
        await client.send_assistant_message(
            1,
            text="Оцени фото",
            image_base64="abc123",
            image_media_type="image/png",
        )
        assert captured["json"] == {
            "telegram_id": 1,
            "text": "Оцени фото",
            "image_base64": "abc123",
            "image_media_type": "image/png",
        }
    finally:
        await client.aclose()


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code", [502, 503])
async def test_send_assistant_message_raises_unavailable_on_server_errors(
    status_code: int,
) -> None:
    client = await _make_client(lambda _request: httpx.Response(status_code))
    try:
        with pytest.raises(BackendClientError) as exc_info:
            await client.send_assistant_message(1, text="hi")
        assert "временно недоступен" in exc_info.value.user_message
    finally:
        await client.aclose()


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code", [401, 403])
async def test_send_assistant_message_raises_config_on_auth_errors(status_code: int) -> None:
    client = await _make_client(lambda _request: httpx.Response(status_code))
    try:
        with pytest.raises(BackendClientError) as exc_info:
            await client.send_assistant_message(1, text="hi")
        assert exc_info.value.user_message == "Ошибка конфигурации сервиса."
    finally:
        await client.aclose()


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code", [400, 422])
async def test_send_assistant_message_raises_invalid_on_client_errors(status_code: int) -> None:
    client = await _make_client(lambda _request: httpx.Response(status_code))
    try:
        with pytest.raises(BackendClientError) as exc_info:
            await client.send_assistant_message(1, text="hi")
        assert exc_info.value.user_message == "Не удалось обработать сообщение."
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_send_assistant_message_raises_unavailable_on_connect_error() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused")

    client = await _make_client(handler)
    try:
        with pytest.raises(BackendClientError) as exc_info:
            await client.send_assistant_message(1, text="hi")
        assert "временно недоступен" in exc_info.value.user_message
    finally:
        await client.aclose()


@pytest.mark.asyncio
async def test_send_assistant_message_returns_fallback_on_empty_reply() -> None:
    client = await _make_client(
        lambda _request: httpx.Response(
            200,
            json={"dialog_id": "d", "request_id": "r", "reply": "   "},
        )
    )
    try:
        reply = await client.send_assistant_message(1, text="hi")
        assert "Не удалось получить ответ" in reply
    finally:
        await client.aclose()

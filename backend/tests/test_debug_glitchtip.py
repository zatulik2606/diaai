from unittest.mock import patch

import pytest

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_sentry_test_not_found_without_debug_token(monkeypatch) -> None:
    monkeypatch.setenv("GLITCHTIP_DEBUG_TOKEN", "")
    get_settings = __import__("backend.config", fromlist=["get_settings"]).get_settings
    get_settings.cache_clear()
    app = __import__("backend.main", fromlist=["create_app"]).create_app()

    from httpx import ASGITransport, AsyncClient

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/debug/glitchtip-test",
            headers={"Authorization": "Bearer any"},
        )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_sentry_test_unauthorized(client, monkeypatch) -> None:
    monkeypatch.setenv("GLITCHTIP_DEBUG_TOKEN", "expected-token")
    monkeypatch.setenv("GLITCHTIP_DSN", "https://example@glitchtip.com/1")
    get_settings = __import__("backend.config", fromlist=["get_settings"]).get_settings
    get_settings.cache_clear()
    app = __import__("backend.main", fromlist=["create_app"]).create_app()

    from httpx import ASGITransport, AsyncClient

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/debug/glitchtip-test",
            headers={"Authorization": "Bearer wrong"},
        )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_sentry_test_ok(monkeypatch) -> None:
    monkeypatch.setenv("GLITCHTIP_DEBUG_TOKEN", "expected-token")
    monkeypatch.setenv("GLITCHTIP_DSN", "https://example@glitchtip.com/1")
    get_settings = __import__("backend.config", fromlist=["get_settings"]).get_settings
    get_settings.cache_clear()
    app = __import__("backend.main", fromlist=["create_app"]).create_app()

    from httpx import ASGITransport, AsyncClient

    transport = ASGITransport(app=app)
    with patch("sentry_sdk.capture_message") as capture:
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get(
                "/debug/glitchtip-test",
                headers={"Authorization": "Bearer expected-token"},
            )
    assert response.status_code == 200
    assert response.json() == {"ok": True, "project": "diaai-backend"}
    capture.assert_called_once()


@pytest.mark.asyncio
async def test_error_test_returns_500(monkeypatch) -> None:
    monkeypatch.setenv("GLITCHTIP_DEBUG_TOKEN", "expected-token")
    get_settings = __import__("backend.config", fromlist=["get_settings"]).get_settings
    get_settings.cache_clear()
    app = __import__("backend.main", fromlist=["create_app"]).create_app()

    from httpx import ASGITransport, AsyncClient

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/debug/error-test",
            headers={"Authorization": "Bearer expected-token"},
        )
    assert response.status_code == 500
    assert response.json()["error"]["code"] == "INTERNAL_ERROR"

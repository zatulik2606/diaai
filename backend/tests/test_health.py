import pytest

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_health(client) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "version": "1.0.0",
        "database": "ok",
    }


@pytest.mark.asyncio
async def test_health_without_database(app) -> None:
    from httpx import ASGITransport, AsyncClient

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 503
    assert response.json() == {"status": "unavailable", "database": "down"}

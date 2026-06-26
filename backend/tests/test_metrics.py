import pytest

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_metrics(client) -> None:
    response = await client.get("/metrics")
    assert response.status_code == 200
    assert "http" in response.text

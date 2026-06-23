import base64

import pytest

pytestmark = pytest.mark.integration


@pytest.fixture
def transcribe_payload() -> dict:
    return {
        "audio_base64": base64.b64encode(b"fake-audio-bytes").decode(),
        "media_type": "audio/ogg",
    }


@pytest.mark.asyncio
async def test_transcribe_returns_200(client, auth_headers, transcribe_payload) -> None:
    response = await client.post(
        "/api/v1/media/transcribe",
        headers=auth_headers,
        json=transcribe_payload,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["text"] == "Распознанный текст из голоса"


@pytest.mark.asyncio
async def test_transcribe_empty_audio_422(client, auth_headers) -> None:
    response = await client.post(
        "/api/v1/media/transcribe",
        headers=auth_headers,
        json={"audio_base64": base64.b64encode(b"").decode(), "media_type": "audio/ogg"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_transcribe_invalid_base64_422(client, auth_headers) -> None:
    response = await client.post(
        "/api/v1/media/transcribe",
        headers=auth_headers,
        json={"audio_base64": "not!!!base64", "media_type": "audio/ogg"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_transcribe_unauthorized_401(
    client, invalid_auth_headers, transcribe_payload
) -> None:
    response = await client.post(
        "/api/v1/media/transcribe",
        headers=invalid_auth_headers,
        json=transcribe_payload,
    )
    assert response.status_code == 401

import pytest

from backend.config import Settings
from backend.glitchtip_poller import GlitchTipPoller


def test_format_issue_message():
    message = GlitchTipPoller.format_issue_message(
        {
            "metadata": {
                "type": "ValueError",
                "value": "invalid glucose reading format [backend 20260625T161242]",
            },
            "permalink": "https://eu.glitchtip.com/diaai-backend/issues/73774",
        }
    )
    assert "GlitchTip: ValueError: invalid glucose reading format" in message
    assert "73774" in message


@pytest.mark.asyncio
async def test_poll_once_primes_without_sending(monkeypatch):
    settings = Settings(
        glitchtip_api_token="token",
        glitchtip_url="https://eu.glitchtip.com",
        glitchtip_org="diaai",
        telegram_alarm_bot_token="bot",
        telegram_alarm_chat_id="123",
    )
    poller = GlitchTipPoller(settings)
    poller.fetch_issues = lambda: _async_issues(  # type: ignore[method-assign]
        [{"id": "1", "metadata": {"type": "Exception", "value": "first"}, "permalink": "https://x/1"}]
    )
    calls: list[str] = []
    monkeypatch.setattr(
        "backend.glitchtip_poller.send_telegram",
        lambda _token, _chat_id, text: calls.append(text),
    )

    sent = await poller.poll_once()
    assert sent == 0
    assert calls == []


@pytest.mark.asyncio
async def test_poll_once_sends_new_issue(monkeypatch):
    settings = Settings(
        glitchtip_api_token="token",
        glitchtip_url="https://eu.glitchtip.com",
        glitchtip_org="diaai",
        telegram_alarm_bot_token="bot",
        telegram_alarm_chat_id="123",
    )
    poller = GlitchTipPoller(settings)
    poller._primed = True
    poller._seen.add("1")
    poller.fetch_issues = lambda: _async_issues(  # type: ignore[method-assign]
        [
            {"id": "1", "metadata": {"type": "Exception", "value": "old"}, "permalink": "https://x/1"},
            {"id": "2", "metadata": {"type": "Exception", "value": "new issue"}, "permalink": "https://x/2"},
        ]
    )
    calls: list[str] = []
    monkeypatch.setattr(
        "backend.glitchtip_poller.send_telegram",
        lambda _token, _chat_id, text: calls.append(text),
    )

    sent = await poller.poll_once()
    assert sent == 1
    assert len(calls) == 1
    assert "new issue" in calls[0]


async def _async_issues(issues):
    return issues

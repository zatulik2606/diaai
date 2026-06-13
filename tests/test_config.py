from __future__ import annotations

import pytest

from diaai.config import Config


@pytest.fixture(autouse=True)
def _no_dotenv_file(monkeypatch: pytest.MonkeyPatch) -> None:
    """Isolate env tests from local .env (AAA: controlled Arrange)."""
    monkeypatch.setattr("diaai.config.load_dotenv", lambda *args, **kwargs: None)


def test_config_from_env_loads_backend_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "bot-token")
    monkeypatch.setenv("BACKEND_URL", "http://127.0.0.1:9000")
    monkeypatch.setenv("BACKEND_SERVICE_TOKEN", "service-token")
    monkeypatch.setenv("LOG_LEVEL", "debug")

    config = Config.from_env()

    assert config.telegram_bot_token == "bot-token"
    assert config.backend_url == "http://127.0.0.1:9000"
    assert config.backend_service_token == "service-token"
    assert config.log_level == "DEBUG"


def test_config_from_env_requires_telegram_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.setenv("BACKEND_SERVICE_TOKEN", "service-token")

    with pytest.raises(ValueError, match="TELEGRAM_BOT_TOKEN"):
        Config.from_env()


def test_config_from_env_requires_backend_service_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "bot-token")
    monkeypatch.delenv("BACKEND_SERVICE_TOKEN", raising=False)

    with pytest.raises(ValueError, match="BACKEND_SERVICE_TOKEN"):
        Config.from_env()


def test_config_from_env_default_backend_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "bot-token")
    monkeypatch.setenv("BACKEND_SERVICE_TOKEN", "service-token")
    monkeypatch.delenv("BACKEND_URL", raising=False)

    config = Config.from_env()

    assert config.backend_url == "http://127.0.0.1:8000"

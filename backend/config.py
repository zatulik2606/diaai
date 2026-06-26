from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

_INSECURE_SERVICE_TOKENS = frozenset({"", "change-me"})


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    backend_service_token: str = "change-me"
    backend_host: str = "127.0.0.1"
    backend_port: int = 8000
    log_level: str = "INFO"
    database_url: str = "postgresql+asyncpg://diaai:diaai@localhost:5433/diaai"
    openrouter_api_key: str = ""
    llm_model: str = "openrouter/auto"
    llm_max_history: int = 10
    llm_timeout_seconds: float = 30.0
    stt_model: str = "openai/whisper-large-v3"
    stt_timeout_seconds: float = 60.0
    analytics_query_model: str = "openrouter/auto"
    analytics_query_timeout_seconds: float = 5.0
    analytics_query_row_limit: int = 100
    analytics_query_llm_timeout_seconds: float = 30.0
    glitchtip_dsn: str = ""
    glitchtip_environment: str = "development"
    glitchtip_traces_sample_rate: float = 0.01
    glitchtip_release: str = ""
    glitchtip_debug_token: str = ""
    glitchtip_url: str = "https://eu.glitchtip.com"
    glitchtip_org: str = "diaai"
    glitchtip_api_token: str = ""
    glitchtip_poll_interval_seconds: int = 60
    telegram_alarm_bot_token: str = ""
    telegram_alarm_chat_id: str = ""
    glitchtip_webhook_secret: str = ""
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_use_tls: bool = True
    glitchtip_alert_email_to: str = ""
    glitchtip_alert_email_from: str = ""
    glitchtip_smtp_relay_url: str = ""
    smtp_relay_token: str = ""


def validate_service_token(settings: Settings) -> None:
    if settings.backend_service_token in _INSECURE_SERVICE_TOKENS:
        msg = "Set BACKEND_SERVICE_TOKEN to a secure value in .env (not 'change-me')"
        raise RuntimeError(msg)


@lru_cache
def get_settings() -> Settings:
    return Settings()

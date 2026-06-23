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


def validate_service_token(settings: Settings) -> None:
    if settings.backend_service_token in _INSECURE_SERVICE_TOKENS:
        msg = "Set BACKEND_SERVICE_TOKEN to a secure value in .env (not 'change-me')"
        raise RuntimeError(msg)


@lru_cache
def get_settings() -> Settings:
    return Settings()

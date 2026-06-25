import logging

from backend.config import Settings

logger = logging.getLogger(__name__)


def init_sentry(settings: Settings) -> None:
    if not settings.glitchtip_dsn:
        return

    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    from sentry_sdk.integrations.starlette import StarletteIntegration

    kwargs: dict = {
        "dsn": settings.glitchtip_dsn,
        "environment": settings.glitchtip_environment,
        "traces_sample_rate": settings.glitchtip_traces_sample_rate,
        "auto_session_tracking": False,  # GlitchTip does not support sessions
        "send_default_pii": False,
        "integrations": [
            StarletteIntegration(transaction_style="endpoint"),
            FastApiIntegration(transaction_style="endpoint"),
            LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
        ],
    }
    if settings.glitchtip_release:
        kwargs["release"] = settings.glitchtip_release

    sentry_sdk.init(**kwargs)
    logger.info(
        "GlitchTip enabled (environment=%s, traces=%s)",
        settings.glitchtip_environment,
        settings.glitchtip_traces_sample_rate,
    )

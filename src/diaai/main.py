from __future__ import annotations

import asyncio
import logging

from diaai.backend_client import BackendClient
from diaai.bot import TelegramBot
from diaai.config import Config


def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


async def run() -> None:
    config = Config.from_env()
    setup_logging(config.log_level)
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")

    backend_client = BackendClient(
        base_url=config.backend_url,
        service_token=config.backend_service_token,
    )
    try:
        bot = TelegramBot(
            bot_token=config.telegram_bot_token,
            backend_client=backend_client,
        )
        await bot.run_polling()
    finally:
        await backend_client.aclose()


def main() -> None:
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Bot stopped")


if __name__ == "__main__":
    main()

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from diaai.bot import TelegramBot
from diaai.config import Config
from diaai.llm_client import LlmClient
from diaai.prompt import Prompt
from diaai.session_store import SessionStore


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

    system_prompt = Prompt(Path("prompts/system.txt")).load_system_prompt()
    session_store = SessionStore(max_history_pairs=config.llm_max_history)
    llm_client = LlmClient(api_key=config.openrouter_api_key, model=config.llm_model)

    bot = TelegramBot(
        bot_token=config.telegram_bot_token,
        llm_client=llm_client,
        session_store=session_store,
        system_prompt=system_prompt,
    )
    await bot.run_polling()


def main() -> None:
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Bot stopped")


if __name__ == "__main__":
    main()

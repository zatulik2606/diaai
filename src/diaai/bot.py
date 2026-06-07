from __future__ import annotations

from aiogram import Bot, Dispatcher

from diaai.handlers import build_handlers
from diaai.llm_client import LlmClient
from diaai.session_store import SessionStore


class TelegramBot:
    def __init__(
        self,
        bot_token: str,
        llm_client: LlmClient,
        session_store: SessionStore,
        system_prompt: str,
    ) -> None:
        self._bot = Bot(token=bot_token)
        self._dispatcher = Dispatcher()
        self._dispatcher.include_router(
            build_handlers(
                llm_client=llm_client,
                session_store=session_store,
                system_prompt=system_prompt,
            )
        )

    async def run_polling(self) -> None:
        await self._dispatcher.start_polling(self._bot)

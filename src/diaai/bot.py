from __future__ import annotations

from aiogram import Bot, Dispatcher

from diaai.backend_client import BackendClient
from diaai.handlers import build_handlers


class TelegramBot:
    def __init__(self, bot_token: str, backend_client: BackendClient) -> None:
        self._bot = Bot(token=bot_token)
        self._dispatcher = Dispatcher()
        self._dispatcher.include_router(build_handlers(backend_client))

    async def run_polling(self) -> None:
        await self._dispatcher.start_polling(self._bot)

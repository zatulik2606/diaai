from __future__ import annotations

import base64
import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from diaai.backend_client import BackendClient, BackendClientError

logger = logging.getLogger(__name__)


def build_handlers(backend_client: BackendClient) -> Router:
    router = Router()

    @router.message(CommandStart())
    async def start_handler(message: Message) -> None:
        await message.answer(
            "Привет! Я помогу обсудить питание, ХЕ и контекст инсулина.\n"
            "Отправьте вопрос текстом. Это справочная информация, не замена врачу."
        )

    @router.message(F.text)
    async def text_handler(message: Message) -> None:
        user_text = (message.text or "").strip()
        if not user_text:
            return

        chat_id = message.chat.id
        logger.info("Incoming message chat_id=%s", chat_id)

        try:
            reply = await backend_client.send_assistant_message(chat_id, text=user_text)
        except BackendClientError as exc:
            await message.answer(exc.user_message)
            return

        await message.answer(reply)

    @router.message(F.photo)
    async def photo_handler(message: Message) -> None:
        chat_id = message.chat.id
        logger.info("Incoming photo chat_id=%s", chat_id)

        if not message.photo:
            await message.answer("Не удалось прочитать фото. Попробуйте отправить снова.")
            return

        photo = message.photo[-1]
        file_info = await message.bot.get_file(photo.file_id)
        file_bytes = await message.bot.download_file(file_info.file_path)
        image_base64 = base64.b64encode(file_bytes.read()).decode("utf-8")

        caption = (message.caption or "").strip()
        text_part = caption or "Оцени состав и ориентировочные ХЕ по фото."

        try:
            reply = await backend_client.send_assistant_message(
                chat_id,
                text=text_part,
                image_base64=image_base64,
            )
        except BackendClientError as exc:
            await message.answer(exc.user_message)
            return

        await message.answer(reply)

    return router

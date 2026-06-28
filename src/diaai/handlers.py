from __future__ import annotations

import base64
import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from diaai.backend_client import BackendClient, BackendClientError
from diaai.commands import EXAMPLE_TEXT, HELP_TEXT

logger = logging.getLogger(__name__)


def build_handlers(backend_client: BackendClient) -> Router:
    router = Router()

    @router.message(CommandStart())
    async def start_handler(message: Message) -> None:
        await message.answer(
            "Привет! Я Ника — помогу обсудить питание, ХЕ и контекст инсулина.\n"
            "Отправь вопрос текстом или фото. Это справочная информация, не замена врачу."
        )

    @router.message(Command("help"))
    async def help_handler(message: Message) -> None:
        await message.answer(HELP_TEXT)

    @router.message(Command("example"))
    async def example_handler(message: Message) -> None:
        await message.answer(EXAMPLE_TEXT)

    @router.message(F.text & ~F.text.startswith("/"))
    async def text_handler(message: Message) -> None:
        user_text = (message.text or "").strip()
        if not user_text:
            return

        chat_id = message.chat.id
        logger.info("Incoming message chat_id=%s text_len=%s", chat_id, len(user_text))

        try:
            reply = await backend_client.send_assistant_message(chat_id, text=user_text)
        except BackendClientError as exc:
            await message.answer(exc.user_message)
            return

        await message.answer(reply)

    @router.message(F.photo)
    async def photo_handler(message: Message) -> None:
        chat_id = message.chat.id

        if not message.photo:
            await message.answer("Не удалось прочитать фото. Попробуйте отправить снова.")
            return

        photo = message.photo[-1]
        file_info = await message.bot.get_file(photo.file_id)
        file_bytes = await message.bot.download_file(file_info.file_path)
        raw = file_bytes.read()
        image_base64 = base64.b64encode(raw).decode("utf-8")
        logger.info("Incoming photo chat_id=%s image_bytes=%s", chat_id, len(raw))

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

    @router.message(F.voice)
    async def voice_handler(message: Message) -> None:
        chat_id = message.chat.id

        if not message.voice:
            await message.answer("Не удалось прочитать голосовое. Попробуйте снова.")
            return

        file_info = await message.bot.get_file(message.voice.file_id)
        file_bytes = await message.bot.download_file(file_info.file_path)
        raw = file_bytes.read()
        audio_base64 = base64.b64encode(raw).decode("utf-8")
        logger.info("Incoming voice chat_id=%s audio_bytes=%s", chat_id, len(raw))

        try:
            text = await backend_client.transcribe_audio(
                audio_base64,
                media_type="audio/ogg",
            )
        except BackendClientError as exc:
            await message.answer(exc.user_message)
            return

        try:
            reply = await backend_client.send_assistant_message(chat_id, text=text)
        except BackendClientError as exc:
            await message.answer(exc.user_message)
            return

        await message.answer(reply)

    return router

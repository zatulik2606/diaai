from __future__ import annotations

import base64
import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from diaai.llm_client import LlmClient
from diaai.session_store import SessionStore

logger = logging.getLogger(__name__)


def build_handlers(
    llm_client: LlmClient, session_store: SessionStore, system_prompt: str
) -> Router:
    router = Router()

    @router.message(CommandStart())
    async def start_handler(message: Message) -> None:
        session_store.clear(message.chat.id)
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
        history = session_store.get_history(chat_id)

        try:
            reply = llm_client.generate_reply(
                system_prompt=system_prompt,
                history=history,
                user_content=user_text,
            )
        except RuntimeError:
            await message.answer("Сервис временно недоступен. Попробуйте ещё раз через минуту.")
            return

        session_store.add_message(chat_id, "user", user_text)
        session_store.add_message(chat_id, "assistant", reply)
        await message.answer(reply)

    @router.message(F.photo)
    async def photo_handler(message: Message) -> None:
        chat_id = message.chat.id
        logger.info("Incoming photo chat_id=%s", chat_id)
        history = session_store.get_history(chat_id)

        if not message.photo:
            await message.answer("Не удалось прочитать фото. Попробуйте отправить снова.")
            return

        photo = message.photo[-1]
        file_info = await message.bot.get_file(photo.file_id)
        file_bytes = await message.bot.download_file(file_info.file_path)
        image_base64 = base64.b64encode(file_bytes.read()).decode("utf-8")

        caption = (message.caption or "").strip()
        text_part = caption or "Оцени состав и ориентировочные ХЕ по фото."
        user_content = [
            {"type": "text", "text": text_part},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
            },
        ]

        try:
            reply = llm_client.generate_reply(
                system_prompt=system_prompt,
                history=history,
                user_content=user_content,
            )
        except RuntimeError:
            await message.answer("Сервис временно недоступен. Попробуйте ещё раз через минуту.")
            return

        session_store.add_message(chat_id, "user", user_content)
        session_store.add_message(chat_id, "assistant", reply)
        await message.answer(reply)

    return router

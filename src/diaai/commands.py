from __future__ import annotations

from aiogram import Bot
from aiogram.types import BotCommand

BOT_COMMANDS: tuple[BotCommand, ...] = (
    BotCommand(command="start", description="Начать диалог с Никой"),
    BotCommand(command="help", description="Как пользоваться ботом"),
    BotCommand(command="example", description="Примеры вопросов"),
)

HELP_TEXT = (
    "Я — Ника, справочный ассистент по питанию и диабету.\n\n"
    "• Текст — вопрос о еде, ХЕ или контексте инсулина\n"
    "• Фото — оценю блюдо (можно добавить подпись)\n"
    "• Голос — распознаю и отвечу\n\n"
    "⚠️ Не назначаю дозы инсулина. Это не замена врачу."
)

EXAMPLE_TEXT = (
    "Примеры вопросов:\n\n"
    "• Сколько примерно ХЕ в тарелке борща?\n"
    "• Что учесть, если съела яблоко перед сном?\n"
    "• Как посчитать ХЕ по этикетке?\n\n"
    "Напиши текстом или отправь фото блюда."
)


async def setup_bot_commands(bot: Bot) -> None:
    await bot.set_my_commands(list(BOT_COMMANDS))

from asyncio import sleep
from random import choice

from aiogram.types import Message

from python_usrus_bot.bot.bot_context import BotContext


async def handle_who_is_right(message: Message, context: BotContext) -> None:
    message_text = message.text
    if message_text is None:
        return

    words = message_text.split()
    if len(words) < 2:
        return

    names = words[1::]

    answer_message = await message.reply("Детально изучаю всю переписку...")

    await sleep(2)
    await answer_message.edit_text("Знакомлюсь с позициями собеседников...")

    await sleep(2)
    await answer_message.edit_text("Изучаю все аргументы...")

    await sleep(2)
    await answer_message.edit_text("Изучаю источники...")

    await sleep(2)
    await answer_message.edit_text("Проверяю публичные базы данных...")

    await sleep(2)
    await answer_message.edit_text(f"Я считаю, что {choice(names)} абсолютно прав!")

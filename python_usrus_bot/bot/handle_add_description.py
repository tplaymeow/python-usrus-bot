import re

from aiogram.types import Message

from python_usrus_bot.bot.bot_context import BotContext
from python_usrus_bot.bot.helpers import is_user_admin
from python_usrus_bot.models.description import Description


async def handle_add_description(message: Message, context: BotContext) -> None:
    if not await is_user_admin(message, context):
        await message.answer("Действие доступно только админам")
        return

    message_text = message.text
    if message_text is None:
        return

    pattern = re.compile(r"/add_description (?P<user_id>\d+) (?P<text>.+)")
    match = pattern.match(message_text)
    if match is None:
        await message.answer("Неверный формат")
        return

    user_id_string = match.group("user_id")
    description_text = match.group("text")
    if user_id_string is None or description_text is None:
        await message.answer("Неверный формат")
        return

    await context.description_repository.add(int(user_id_string), Description(0, description_text))

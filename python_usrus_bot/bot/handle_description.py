import re

from aiogram.types import Message

from python_usrus_bot.bot.bot_context import BotContext
from python_usrus_bot.bot.helpers import is_user_admin
from python_usrus_bot.models.description import Description


async def handle_description(message: Message, context: BotContext) -> None:
    if not await is_user_admin(message, context):
        await message.answer("Действие доступно только админам")
        return

    message_text = message.text
    if message_text is None:
        return

    pattern = re.compile(r"/description (?P<user_id>\d+)")
    match = pattern.match(message_text)
    if match is None:
        await message.answer("Неверный формат")
        return

    user_id_string = match.group("user_id")
    if user_id_string is None:
        await message.answer("Неверный формат")
        return

    descriptions = await context.description_repository.get(int(user_id_string))
    descriptions_strings = [descr.text for descr in descriptions]
    descriptions_string = "\n".join(descriptions_strings)

    await message.reply(descriptions_string)

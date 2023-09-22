import datetime

from aiogram.types import Message

from python_usrus_bot.bot.bot_context import BotContext
from python_usrus_bot.bot.helpers import get_user_info
from python_usrus_bot.models.obscene_expressions_stat import ObsceneExpressionsStat
from python_usrus_bot.text_utills.obscene_words import obscene_words_count
from python_usrus_bot.text_utills.text_processing import text_preprocessing


async def handle_obscene_stat(message: Message, context: BotContext, text: str = None) -> None:
    message_text = text or message.text
    if message_text is None:
        return

    user_info = await get_user_info(message, context)

    count = obscene_words_count(text_preprocessing(message_text))
    stat = await context.obscene_expressions_stat_repository.get(user_info.id)
    if stat is None or stat.is_outdated:
        stat = ObsceneExpressionsStat(datetime.date.today(), count)
    else:
        stat.count += count

    await context.obscene_expressions_stat_repository.add_or_update(user_info.id, stat)

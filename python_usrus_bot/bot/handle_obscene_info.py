from aiogram.types import Message

from python_usrus_bot.bot.bot_context import BotContext


async def handle_obscene_info(message: Message, context: BotContext) -> None:

    info = await context.obscene_expressions_stat_repository.get(message.from_user.id)
    descriptions_string = (
        f"User - @{message.from_user.username}\n"
        f"Матов - {info.count}"
    )

    await message.answer(descriptions_string)
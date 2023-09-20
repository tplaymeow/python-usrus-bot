from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from motor.motor_asyncio import AsyncIOMotorClient

from python_usrus_bot.bot.bot_context import BotContext
from python_usrus_bot.bot.handle_add_answer_style import handle_add_answer_style
from python_usrus_bot.bot.handle_add_description import handle_add_description
from python_usrus_bot.bot.handle_description import handle_description
from python_usrus_bot.bot.handle_info import handle_info
from python_usrus_bot.bot.handle_obscene_info import handle_obscene_info
from python_usrus_bot.bot.handle_obscene_stat import handle_obscene_stat
from python_usrus_bot.bot.handle_voice_reply import handle_voice_reply
from python_usrus_bot.database.answer_style_repository import AnswerStyleRepository
from python_usrus_bot.database.description_repository import DescriptionRepository
from python_usrus_bot.database.obscene_expressions_stat_repository import ObsceneExpressionsStatRepository
from python_usrus_bot.database.user_info_repository import UserInfoRepository

dp = Dispatcher()

db_client = AsyncIOMotorClient("mongodb://mongodb:27017")
context = BotContext(
    user_info_repository=UserInfoRepository(db_client),
    description_repository=DescriptionRepository(db_client),
    answer_style_repository=AnswerStyleRepository(db_client),
    obscene_expressions_stat_repository=ObsceneExpressionsStatRepository(db_client))


@dp.message(Command("info"))
async def command_info(message: Message) -> None:
    await handle_info(message)


@dp.message(Command("obscene_info"))
async def command_obscene_info(message: Message) -> None:
    await handle_obscene_info(message, context)


@dp.message(Command("add_description"))
async def command_add_description(message: Message) -> None:
    await handle_add_description(message, context)


@dp.message(Command("description"))
async def command_add_description(message: Message) -> None:
    await handle_description(message, context)


@dp.message(Command("add_answer_style"))
async def command_add_answer_style(message: Message) -> None:
    await handle_add_answer_style(message, context)


@dp.message()
async def other_message(message: Message) -> None:
    await handle_obscene_stat(message, context)
    await handle_voice_reply(message, context)


async def start_bot() -> None:
    bot = Bot(getenv("TG_BOT_TOKEN"))
    await dp.start_polling(bot)

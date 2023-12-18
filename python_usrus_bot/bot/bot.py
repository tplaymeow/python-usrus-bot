from os import getenv, remove

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from motor.motor_asyncio import AsyncIOMotorClient

from python_usrus_bot.bot.bot_context import BotContext
from python_usrus_bot.bot.handle_mem import handle_mem
from python_usrus_bot.bot.handle_add_answer_style import handle_add_answer_style
from python_usrus_bot.bot.handle_add_description import handle_add_description
from python_usrus_bot.bot.handle_description import handle_description
from python_usrus_bot.bot.handle_info import handle_info
from python_usrus_bot.bot.handle_obscene_info import handle_obscene_info
from python_usrus_bot.bot.handle_obscene_stat import handle_obscene_stat
from python_usrus_bot.bot.handle_voice_reply import handle_voice_reply
from python_usrus_bot.bot.handle_who_is_right import handle_who_is_right
from python_usrus_bot.bot.handler_answer_voice import handler_answer_voice
from python_usrus_bot.bot.helpers import is_user_admin
from python_usrus_bot.database.answer_style_repository import AnswerStyleRepository
from python_usrus_bot.database.description_repository import DescriptionRepository
from python_usrus_bot.database.obscene_expressions_stat_repository import ObsceneExpressionsStatRepository
from python_usrus_bot.database.user_info_repository import UserInfoRepository

bot = Bot(getenv("TG_BOT_TOKEN"))
dp = Dispatcher()
scheduler = AsyncIOScheduler()

db_client = AsyncIOMotorClient("mongodb://mongodb:27017")
context = BotContext(
    user_info_repository=UserInfoRepository(db_client),
    description_repository=DescriptionRepository(db_client),
    answer_style_repository=AnswerStyleRepository(db_client),
    obscene_expressions_stat_repository=ObsceneExpressionsStatRepository(db_client))


@dp.message(F.content_type.in_({'video_note', 'voice'}))
async def answer_voice_handler(message: Message):
    await handler_answer_voice(message, context, bot)


@dp.message(Command("subscribe"))
async def command_subscribe(message: Message) -> None:
    if not await is_user_admin(message, context):
        await message.answer("Действие доступно только админам")
        return

    scheduler.add_job(
        send_chat_info,
        trigger="cron", id=str(message.chat.id),
        hour=0, minute=0, args=[message.chat.id])


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


@dp.message(Command("mem"))
async def command_mem(message: Message) -> None:
    await handle_mem(message, bot)


@dp.message(Command("who_is_right"))
async def command_who_is_right(message: Message) -> None:
    await handle_who_is_right(message, context)


@dp.message()
async def other_message(message: Message) -> None:
    await handle_obscene_stat(message, context)
    await handle_voice_reply(message, context)


async def start_bot() -> None:
    scheduler.start()
    await dp.start_polling(bot)


async def send_chat_info(chat_id: int) -> None:
    users = await context.user_info_repository.get_all()
    message = "Сапожники:"

    for user in users:
        obscene_info = await context.obscene_expressions_stat_repository.get(user.id)
        message += f"\n@{user.username} {user.name or ''} плохо выразился {obscene_info.count} раз"
        stat = ObsceneExpressionsStat(datetime.date.today(), 0)
        await context.obscene_expressions_stat_repository.add_or_update(user.id, stat)

    await bot.send_message(chat_id, message)

from aiogram.enums import ContentType
from aiogram.types import Message

from python_usrus_bot.bot.bot_context import BotContext
from python_usrus_bot.models.user_info import UserInfo


async def get_user_info(message: Message, context: BotContext) -> UserInfo:
    info = await context.user_info_repository.get(message.from_user.id)
    if info is None:
        info = UserInfo(message.from_user.id, message.from_user.username)
        await context.user_info_repository.add(info)
    return info


async def is_user_admin(message: Message, context: BotContext) -> bool:
    user_info = await get_user_info(message, context)
    return user_info.is_admin

def convert_content_type(message: Message) -> str:
    match message.content_type:
        case ContentType.VOICE:
            return "голосовухи"
        case ContentType.VIDEO_NOTE:
            return "кружочка"
        case _:
            return ""
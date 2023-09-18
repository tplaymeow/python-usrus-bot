from aiogram.types import Message


async def handle_info(message: Message) -> None:
    await message.reply((
        f"Chat ID: {message.chat.id}\n"
        f"User ID: {message.from_user.id}\n"
        f"Username: {message.from_user.username}"))

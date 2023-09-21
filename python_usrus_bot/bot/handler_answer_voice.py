from os import remove
from pathlib import Path

from aiogram import Bot, types
from aiogram.types import Message

from python_usrus_bot.bot.bot_context import BotContext
from python_usrus_bot.bot.handle_voice_reply import handle_voice_reply
from python_usrus_bot.stt.stt import STT

stt = STT()

async def handler_answer_voice(message: Message, context: BotContext, bot: Bot) -> None:
    if message.content_type == types.ContentType.VOICE:
        file_id = message.voice.file_id
    elif message.content_type == types.ContentType.VIDEO_NOTE:
        file_id = message.video_note.file_id
    else:
        return

    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_on_disk = Path("", f"{file_id}.tmp")
    await bot.download_file(file_path, destination=file_on_disk)
    text = stt.audio_to_text(file_on_disk)
    print(text)
    await handle_voice_reply(message, context, text or "")

    remove(file_on_disk)
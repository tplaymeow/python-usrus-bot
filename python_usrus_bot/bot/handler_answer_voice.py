from os import remove

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.types import Message

from python_usrus_bot.bot.bot_context import BotContext
from python_usrus_bot.bot.handle_obscene_stat import handle_obscene_stat
from python_usrus_bot.bot.handle_voice_reply import handle_voice_reply
from python_usrus_bot.stt.stt import STT


stt = STT()


async def handler_answer_voice(message: Message, context: BotContext, bot: Bot) -> None:
    match message.content_type:
        case ContentType.VOICE:
            file_id = message.voice.file_id
            file_unique_id = message.voice.file_unique_id
            file_extension = "ogg"
            content_type = "голосовухи"
        case ContentType.VIDEO_NOTE:
            file_id = message.video_note.file_id
            file_unique_id = message.video_note.file_unique_id
            file_extension = "mp4"
            content_type = "кружка"
        case _:
            return

    file_info = await bot.get_file(file_id)

    output_path = f"{file_unique_id}.{file_extension}"
    await bot.download_file(file_info.file_path, output_path)
    recognized_text = stt.run(output_path)
    remove(output_path)
    await message.reply((
        f"<b>Расшифровка {content_type}:</b>\n"
        f"<span class=tg-spoiler>'{recognized_text}'</span>"
    ), parse_mode="html")
    await handle_obscene_stat(message, context, recognized_text)
    await handle_voice_reply(message, context, recognized_text)

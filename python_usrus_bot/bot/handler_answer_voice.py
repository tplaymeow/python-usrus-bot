from io import BytesIO
from os import remove
from pathlib import Path

from aiogram import Bot, types
from aiogram.enums import ContentType
from aiogram.types import Message, Voice, VideoNote
from pydub import AudioSegment

from python_usrus_bot.bot.bot_context import BotContext
from python_usrus_bot.bot.handle_voice_reply import handle_voice_reply
from python_usrus_bot.bot.helpers import convert_content_type
from python_usrus_bot.stt.stt import STT


# stt = STT()

def files_output_path(name: str, format: str) -> str:
    return f"{name}.{format}"


async def save_voice_as_wav(bot: Bot, voice: Voice) -> str:
    file_info = await bot.get_file(voice.file_id)
    data = BytesIO()
    await bot.download_file(file_info.file_path, data)

    output_format = "wav"
    output_path = files_output_path(voice.file_unique_id, output_format)
    AudioSegment.from_ogg(data).export(output_path, format=output_format)

    return output_path


async def save_video_note_as_wav(bot: Bot, video: VideoNote) -> str:
    file_info = await bot.get_file(video.file_id)
    data = BytesIO()
    await bot.download_file(file_info.file_path, data)

    output_format = "wav"
    output_path = files_output_path(video.file_unique_id, output_format)
    AudioSegment.from_file(data, format="mp4").export(output_path, format=output_format)

    return output_path


async def handler_answer_voice(message: Message, context: BotContext, bot: Bot) -> None:
    match message.content_type:
        case ContentType.VOICE:
            await save_voice_as_wav(bot, message.voice)
        case ContentType.VIDEO_NOTE:
            await save_video_note_as_wav(bot, message.video_note)
        case _:
            return

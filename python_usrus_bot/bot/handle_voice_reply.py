from os import remove
from random import random

from aiogram.types import Message, FSInputFile

from python_usrus_bot.bot.bot_context import BotContext
from python_usrus_bot.bot.helpers import get_user_info
from python_usrus_bot.chat_gpt.chat_gpt import chat_gpt_request

from python_usrus_bot.models.answer_style import pick_random_styles
from python_usrus_bot.models.description import pick_random_descriptions
from python_usrus_bot.tts.tts import text_to_speech


def should_process(message_text: str) -> bool:
    return len(message_text) > 30 and random() < 0.3


async def handle_voice_reply(message: Message, context: BotContext) -> None:
    message_text = message.text
    if message_text is None:
        return

    if not should_process(message_text):
        return

    user_info = await get_user_info(message, context)

    descriptions = await context.description_repository.get(user_info.id) or []
    descriptions_texts = pick_random_descriptions(descriptions, 2)
    descriptions_text = "\n".join(descriptions_texts)

    styles = await context.answer_style_repository.get(user_info.id) or []
    styles_texts = pick_random_styles(styles, 2)
    styles_text = "\n".join(styles_texts)

    request_text = ("Составь короткий ответ на сообщение от женского лица в чате человеку в указанном стиле, используя "
                    "описание человека.\n")
    request_text += f"Имя человека: {user_info.name}.\n\n" if user_info.name is not None else ""
    request_text += f"Сообщение:\n{message_text}\n\n"
    request_text += f"Описание человека:\n{descriptions_text}\n\n"
    request_text += f"Стиль ответа:\n{styles_text}\n\n"

    reply_text = await chat_gpt_request(request_text)

    filename = f"{message.message_id}.mp3"

    text_to_speech(reply_text, filename)

    await message.reply_voice(FSInputFile(filename))

    remove(filename)

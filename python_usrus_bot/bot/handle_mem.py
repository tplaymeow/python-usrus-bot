import random
from aiogram import Bot
from aiogram.types import Message

from python_usrus_bot.yandex_pictures.find_pictures import find_pictures


async def handle_mem(message: Message, bot: Bot) -> None:
    message_text = 'мем ' + ' '.join(message.text.split()[1::])
    answer_message = await message.reply("Погрузился в поиски...")

    try:
        images = await find_pictures(message_text)
        image = random.choice(images)
        await bot.send_photo(chat_id=message.chat.id, photo=image)
        await answer_message.delete()
    except:
        await answer_message.edit_text("Приносим извинения, что-то пошло не так")

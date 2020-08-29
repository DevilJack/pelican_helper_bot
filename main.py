import os
import re
import io
import logging
import asyncio
from time import gmtime, strftime, localtime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN, BOSS_ID, LOZHKIN_ID, PELICAN_TEAM_ID
from load import load_xl_data
from do import do_find_top_answers, do_remember_user_start
from df_config import detect_intent_texts


logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()

bot = Bot(token=TOKEN)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage, loop=loop)

xl_data = load_xl_data("qa.xlsx")


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение"""
    await do_remember_user_start(message)
    hello_message = "привет, я пеликан"
    await message.answer(hello_message)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    """Отправляет вспомогательное сообщение"""
    help_message = "спроси меня что-нибудь про политех"
    await message.answer(help_message)


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def text_question_handler(message: types.Message):
    """Обрабатывает прочие сообщения"""
    global xl_data
    answers = await do_find_top_answers(message, xl_data)

    if answers == False:
        df_result = detect_intent_texts("pelican-vbox", "123456789", message.text, "ru")
        if df_result:
            await message.answer(df_result)
        else:
            await message.answer("Я ещё учусь понимать все твои фразы, я ведь всё-таки пеликан :)")

        q_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        question = message.text
        username = message.from_user.username
        first_last = message.from_user.first_name + " " + message.from_user.last_name

        no_answer_message = f"""
====================
Неотвеченный вопрос:

Имя: {first_last}
Никнейм: {username}
Время: {q_time}
Ответ dialogflow:
{df_result}
Текст сообщения:
{question}
====================
    """

        await bot.send_message(PELICAN_TEAM_ID, no_answer_message)

        
    elif answers == -1:
        await message.answer("Произошла ошибка :(")
        await bot.send_message(PELICAN_TEAM_ID, "Произошла ошибка :(")
    
    else:
        await message.answer(answers)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
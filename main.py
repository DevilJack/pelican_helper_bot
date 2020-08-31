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


root_logger= logging.getLogger()
root_logger.setLevel(logging.INFO) # or whatever
handler = logging.FileHandler('app.log', 'w', 'utf-8') # or whatever
formatter = logging.Formatter('%(levelname)s - %(message)s') # or whatever
handler.setFormatter(formatter) # Pass handler as a parameter, not assign
root_logger.addHandler(handler)

loop = asyncio.get_event_loop()

bot = Bot(token=TOKEN)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage, loop=loop)

xl_data = load_xl_data("qa.xlsx")


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение"""
    await do_remember_user_start(message)
    hello_message = """
Привет, политехник!

Я - Цифровой пеликан, твой помощник и проводник в жизнь Политехнического университета. Я буду сопровождать тебя на протяжении твоего обучения. 

Не стесняйся и спрашивай обо всем, что тебя интересует. Я могу рассказать тебе о Политехе, студенческой жизни здесь и не только. Пиши мне в любое время и я с радостью тебе отвечу!

Но помни, что я только учусь и могу не сразу верно понять твой вопрос. Старайся сформулировать его как можно точнее."""

    await message.answer(hello_message)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    """Отправляет вспомогательное сообщение"""
    help_message = """
Не стесняйся и спрашивай обо всем, что тебя интересует. Я могу рассказать тебе о Политехе, студенческой жизни здесь и не только. Пиши мне в любое время и я с радостью тебе отвечу!

Но помни, что я только учусь и могу не сразу верно понять твой вопрос. Старайся сформулировать его как можно точнее."""

    await message.answer(help_message)


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def text_question_handler(message: types.Message):
    """Обрабатывает прочие сообщения"""
    global xl_data
    answers = await do_find_top_answers(message, xl_data)

    q_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    question = message.text
    username = message.from_user.username if message.from_user.username else "Nousername"
    first_last = message.from_user.first_name if message.from_user.first_name else "Noname" + " " + message.from_user.last_name if  message.from_user.last_name else "Noname" 

    if answers == False:
        df_result = detect_intent_texts("pelican-vbox", "123456789", message.text, "ru")
        if df_result:
            await message.answer(df_result)
        else:
            await message.answer("Я ещё учусь понимать все твои фразы, я ведь всё-таки пеликан :)")

        df_result = "Нет ответа" if not df_result else df_result

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
        logging.info(f"{q_time}--{username}--{df_result}--Answered DF")

        await bot.send_message(PELICAN_TEAM_ID, no_answer_message)

        
    elif answers == -1:
        logging.error(f"{q_time}--{username}--{question}--Error")

        await message.answer("Произошла ошибка :(")
        await bot.send_message(PELICAN_TEAM_ID, "Произошла ошибка :(")
    
    else:
        logging.info(f"{q_time}--{username}--{question}--Answered from XL")
        await message.answer(answers)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
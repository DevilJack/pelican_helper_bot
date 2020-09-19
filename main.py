import os
import re
import io
import logging
import asyncio
from time import gmtime, strftime, localtime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN, BOSS_ID, LOZHKIN_ID, PELICAN_TEAM_ID, \
    MAIN_KEYBOARD, BIG_ROOM_DOMUCH_KEYBOARD, DEAL_CONFIRM_KEYBOARD, CANCEL_KEYBOARD, BUILDING_KEYBOARD, DOCUMENTS_KEYBOARD, BIG_ROOM_STUD_CLUB_KEYBOARD
from load import load_xl_data
from do import do_find_top_answers, do_remember_user_start
from df_config import detect_intent_texts
from states import ServiceForm
from word_model import render_new_doc_sluzhebka
#from mail_model import send_email


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

    await message.answer(hello_message, reply_markup=MAIN_KEYBOARD)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    """Отправляет вспомогательное сообщение"""
    help_message = """
Не стесняйся и спрашивай обо всем, что тебя интересует. Я могу рассказать тебе о Политехе, студенческой жизни здесь и не только. Пиши мне в любое время и я с радостью тебе отвечу!

Но помни, что я только учусь и могу не сразу верно понять твой вопрос. Старайся сформулировать его как можно точнее."""

    await message.answer(help_message, reply_markup=MAIN_KEYBOARD)


@dp.message_handler(lambda message: message.text == '💼 Подать документ 💼')
async def documents_main_handler(message: types.Message):
    text = "Это новая функция, с помощью которой Вы можете заполнить документ и отправить его \
в чат Профсоюзной организации для утверждения.\n\n\
Для успешного оформления документа, пожалуйста, ВНИМАТЕЛЬНО читайте то, что Вам\n\
пишет бот, ВНИМАТЕЛЬНО отвечайте на его вопросы, представьте себе, что \n\
Вы заполняете настоящий бумажный документ - цените время людей, которые будут проверять Ваш документ.\n\n\
После выбора документа, бот задаст несколько последовательных вопросов, необходимых для создания документа.\n\n\
(Для ответа предлагается использовать кнопки (там, где они есть))\n\n\
На каждом вопросе, Вы увидите кнопку ОТМЕНИТЬ ДЕЙСТВИЕ - эта кнопка ПОЛНОСТЬЮ отменяет создание документа, придется начать заново. \
Данные, предоставленные Вами при заполении документа не будут переданы третьим лицам, сразу после отправки документа на почту профсоюза, \n\
все данные будут стерты из памяти бота.\n\n\
НИЖЕ ПРЕДСТАВЛЕН ПРИМЕР ГОТОВОГО ДОКУМЕНТА, ПОЖАЛУЙСТА, ОЗНАКОМЬТЕСЬ С ФОРМАТОМ"
    await message.answer(text)

    with open("word_templates/sluzhebka/example_service.docx", 'rb') as file:
        await bot.send_document(message.chat.id, file, disable_notification=True)

    await message.answer("Пожалуйста, выберите ДОКУМЕНТ для оформления из списка ниже:", reply_markup=DOCUMENTS_KEYBOARD)



# ================================================================================================== СЛУЖЕБКА

@dp.callback_query_handler(lambda callback_query: True, state=ServiceForm.building)
async def service_building_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    #print("in building")
    if callback_query.data == "cancel_building":
        await state.reset_state()
        await callback_query.message.answer("Вы отменили текущее действие", reply_markup=MAIN_KEYBOARD)

    elif callback_query.data in ('gz', 'nik', '3k'):
        await state.update_data(building=callback_query.data)
        await ServiceForm.audience.set()
        await callback_query.message.answer("Вы выбрали здание, в котором множество аудиторий/помещений\n\
Пожалуйста, введите (с помощью клавиатуры) НОМЕР нужной аудитории/помещения: ( НАПРИМЕР, 255 )", reply_markup=CANCEL_KEYBOARD)

    elif callback_query.data == 'du':
        await state.update_data(building=callback_query.data)
        await ServiceForm.room.set()
        await callback_query.message.answer("Вы выбрали Дом учёных, в котором два доступных помещения\n\
Пожалуйста, выберите нужное ПОМЕЩЕНИЕ (для ответа используйте кнопки):", reply_markup=BIG_ROOM_DOMUCH_KEYBOARD)

    elif callback_query.data == 'sc':
        await state.update_data(building=callback_query.data)
        await ServiceForm.room.set()
        await callback_query.message.answer("Вы выбрали Студенческий клуб, в котором два доступных помещения\n\
Пожалуйста, выберите нужное ПОМЕЩЕНИЕ (для ответа используйте кнопки):", reply_markup=BIG_ROOM_STUD_CLUB_KEYBOARD)


@dp.callback_query_handler(lambda callback_query: True, state=ServiceForm.room)
async def service_room_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    #print("in room")
    if callback_query.data == "cancel_big_room":
        await state.reset_state()
        await callback_query.message.answer("Вы отменили текущее действие", reply_markup=MAIN_KEYBOARD)

    elif callback_query.data in ('actzal', 'holl', 'actzal_holl', 'prime_time', 'actzal_prime_time'):
        await state.update_data(room=callback_query.data)
        await ServiceForm.date_interval.set()
        await callback_query.message.answer("Пожалуйста, введите ПРОМЕЖУТОК ДАТ, необходимый для Вашего мероприятия:\n\
( НАПРИМЕР, 'с 18 сентября по 14 ноября 2020 года' или 'c 20 марта по 25 мая 2020 года (по четвергам)' ):", reply_markup=CANCEL_KEYBOARD)


@dp.message_handler(state=ServiceForm.audience)
async def service_audience_message_handler(message: types.Message, state: FSMContext):
    #print("in audience")
    await state.update_data(audience=message.text)
    await ServiceForm.date_interval.set()
    await message.answer("Пожалуйста, введите ПРОМЕЖУТОК ДАТ, необходимый для Вашего мероприятия:\n\
( НАПРИМЕР, 'с 18 сентября по 14 ноября 2020 года' или 'c 20 марта по 25 мая 2020 года (по четвергам)' ):", reply_markup=CANCEL_KEYBOARD)


@dp.message_handler(state=ServiceForm.date_interval)
async def service_date_interval_message_handler(message: types.Message, state: FSMContext):
    #print("in date_interval")
    await state.update_data(date_interval=message.text)
    await ServiceForm.time_interval.set()
    await message.answer("Пожалуйста, введите ВРЕМЕННОЙ ИНТЕРВАЛ, необходимый для Вашего мероприятия:\n\
( НАПРИМЕР, 'с 18:00 до 21:30' или 'c 10:00 до 14:00' )", reply_markup=CANCEL_KEYBOARD)


@dp.message_handler(state=ServiceForm.time_interval)
async def service_time_interval_message_handler(message: types.Message, state: FSMContext):
    #print("in time_interval")
    await state.update_data(time_interval=message.text)
    await ServiceForm.goal.set()
    await message.answer("Пожалуйста, введите ЦЕЛЬ Вашего мероприятия (пожалуйста, обратите внимание на слово ДЛЯ в каждом примере):\n\
( НАПРИМЕР, 'для проведения собраний профоргов ИКНТ' или 'для проведения конкурса Профорг года' )", reply_markup=CANCEL_KEYBOARD)


@dp.message_handler(state=ServiceForm.goal)
async def service_goal_message_handler(message: types.Message, state: FSMContext):
    #print("in goal")
    await state.update_data(goal=message.text)
    await ServiceForm.responsible.set()
    await message.answer("Пожалуйста, введите ФАМИЛИЮ, ИМЯ и ТЕЛЕФОН ответственного за Ваше мероприятие:\n\
( НАПРИМЕР, 'Липянина Анна, тел.: 89217871320' )", reply_markup=CANCEL_KEYBOARD)


@dp.message_handler(state=ServiceForm.responsible)
async def service_responsible_message_handler(message: types.Message, state: FSMContext):
    #print("in responsible")
    await state.update_data(responsible=message.text)
    state_data = await state.get_data()
    new_file = await render_new_doc_sluzhebka(state_data)
    if new_file != None:
        with open(new_file, 'rb') as file:
            await bot.send_document(message.chat.id, file, disable_notification=True)
    else:
        await message.answer("При формировании документа произошла ошибка, пожалуйста, попробуйте позднее")
    await state.update_data(filename=new_file)
    await ServiceForm.confirm.set()
    await message.answer("Пожалуйста, ТЩАТЕЛЬНО ПРОВЕРЬТЕ сформированный документ и подтвердите (или отмените) отправку служебной записки:", reply_markup=DEAL_CONFIRM_KEYBOARD)


@dp.callback_query_handler(lambda callback_query: True, state=ServiceForm.confirm)
async def service_confirm_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    #print("in confirm")
    state_data = await state.get_data()
    filename = state_data.get('filename')

    if callback_query.data == "cancel_deal_send":
        await callback_query.message.answer("Вы отменили отправку служебной записки, ВСЕ введенные Вами данные были стерты", reply_markup=MAIN_KEYBOARD)

    elif callback_query.data == "confirm_deal_send":
        await callback_query.message.answer("Вы подтвердили отправку служебной записки в чат Профсоюзной организации", disable_notification=True)
        await callback_query.message.answer("Отправка Вашего обращения...", disable_notification=True)
        
        goal = state_data.get('goal')
        responsible = state_data.get('responsible')
        
        mail_message = f"====================\nНовый документ:\n\nЦель: {goal}\nОтветственный: {responsible}\nНазвание документа: {filename}\nДокумент был сформирован через бота (Цифровой Пеликан)\n===================="
        
        await bot.send_message(PELICAN_TEAM_ID, mail_message)

        with open(filename, 'rb') as file:
            await bot.send_document(PELICAN_TEAM_ID, file, disable_notification=True)

        #is_sent = send_email("zhozhpost@gmail.com", "НОВАЯ СЛУЖЕБНАЯ ЗАПИСКА ИЗ БОТА", mail_message, filename)
        #if is_sent:
        await callback_query.message.answer("Ваше обращение было успешно отправлено в чат Профсоюзной организации,\n\
спасибо что воспользовались нашим ботом :)")
        
        q_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        logging.info(f"{q_time}--New document send to pelican chat | {responsible} | {goal}")
        # else:
        #     await callback_query.message.answer("При отправке письма на почту Профсоюзной организации произошла ошибка, пожалуйста, попробуйте позднее")
        #     q_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        #     logging.error(f"{q_time}--Error while sending a document | {responsible} | {goal}")
        
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
    os.remove(path)
    await state.reset_state()


# ================================================================================================== MAIN CALLBACK
@dp.callback_query_handler(lambda callback_query: callback_query.data in ("main_cancel", "service_document"), state="*")
async def all_cancels_handler(callback_query: types.CallbackQuery, state: FSMContext):
    #print("in all_cancels")
    if callback_query.data == "main_cancel":
        if await state.get_state() != None:
            await state.reset_state()
            await callback_query.message.answer("Вы отменили текущее действие", reply_markup=MAIN_KEYBOARD)

    elif callback_query.data == "service_document":
        await ServiceForm.building.set()
        await callback_query.message.answer("Вы выбрали СЛУЖЕБНУЮ ЗАПИСКУ для оформления, пожалуйста, ответьте на несколько вопросов:")
        await callback_query.message.answer("Какое здание необходимо для Вашей цели? (для ответа используйте кнопки)", reply_markup=BUILDING_KEYBOARD)


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
            await message.answer(df_result, reply_markup=MAIN_KEYBOARD)
        else:
            await message.answer("Я ещё учусь понимать все твои фразы, я ведь всё-таки пеликан :)", reply_markup=MAIN_KEYBOARD)

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

        await message.answer("Произошла ошибка :(", reply_markup=MAIN_KEYBOARD)
        await bot.send_message(PELICAN_TEAM_ID, "Произошла ошибка :(")
    
    else:
        logging.info(f"{q_time}--{username}--{question}--Answered from XL")
        await message.answer(answers, reply_markup=MAIN_KEYBOARD)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
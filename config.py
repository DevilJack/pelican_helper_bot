from configparser import ConfigParser
from keyboards import ListOfButtons


config = ConfigParser()
config.read("config.ini", encoding='utf-8-sig')

TOKEN = config['token']['TOKEN']

BOSS_ID = config['chat_ids']['BOSS_ID']
LOZHKIN_ID = config['chat_ids']['LOZHKIN_ID']
PELICAN_TEAM_ID = config['chat_ids']['PELICAN_TEAM_ID']

BOT_URL = config['bot_url']['BOT_URL']

WORK_MAIL_LOGIN = config['mail']['WORK_MAIL_LOGIN']
WORK_MAIL_PASSWORD = config['mail']['WORK_MAIL_PASSWORD']
PROF_MAIL = config['mail']['PROF_MAIL']
ZHOZH_MAIL = config['mail']['ZHOZH_MAIL']

MAIN_KEYBOARD = ListOfButtons(
    text = [
        '💼 Подать документ 💼'
    ],
    align = [1]
).reply_keyboard

DEAL_CONFIRM_KEYBOARD = ListOfButtons(
    text = [
        'Подтвердить отправку',
        'Отменить отправку'
    ],
    callback = ['confirm_deal_send', 'cancel_deal_send'],
    align = [1, 1]
).inline_keyboard

CANCEL_KEYBOARD = ListOfButtons(
    text = [
        'Отменить действие'
    ],
    callback = ['main_cancel'],
    align = [1]
).inline_keyboard

BUILDING_KEYBOARD = ListOfButtons(
    text = [
        'Главный учебный корпус', 
        'Научно-исследовательский корпус',
        '3-й учебный корпус',
        'Дом учёных',
        'Студенческий клуб ДКПиМТ СПбПУ',
        'Отменить действие'
    ],
    callback=['gz', 'nik', '3k', 'du', 'sc', 'cancel_building'],
    align=[1, 1, 1, 1, 1, 1]
).inline_keyboard

BIG_ROOM_DOMUCH_KEYBOARD = ListOfButtons(
    text = [
        'Актовый зал', 
        'Холл',
        'Актовый зал и холл',
        'Отменить действие'
    ],
    callback=['actzal', 'holl', 'actzal_holl', 'cancel_big_room'],
    align=[1, 1, 1, 1]
).inline_keyboard

BIG_ROOM_STUD_CLUB_KEYBOARD = ListOfButtons(
    text = [
        'Актовый зал', 
        'Зона Prime Time',
        'Актовый зал и зона Prime Time',
        'Отменить действие'
    ],
    callback=['actzal', 'prime_time', 'actzal_prime_time', 'cancel_big_room'],
    align=[1, 1, 1, 1]
).inline_keyboard

DOCUMENTS_KEYBOARD = ListOfButtons(
    text = [
        'Служебная записка'
    ],
    callback = ['service_document'],
    align = [1]
).inline_keyboard
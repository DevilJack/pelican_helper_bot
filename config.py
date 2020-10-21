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

SERVICE_DOC_PASSWORD = config['passwords']['SERVICE_DOC_PASSWORD']

MAIN_KEYBOARD = ListOfButtons(
    text = [
        'Заполнить документ ✏️'
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

MAT_HELP_BUDGET_KEYBOARD = ListOfButtons(
    text = [
        'Из средств бюджета Просоюза СПбПУ',
        'Из Фонда соц. защиты обуч-ся',
        'Отменить действие'
    ],
    callback = ['mat_help_prof', 'mat_help_fond', 'cancel_mat_help_budget'],
    align = [1, 1, 1]
).inline_keyboard

MAT_HELP_FOND_KEYBOARD = ListOfButtons(
    text = [
        'Из Фонда соц. защиты обуч-ся'
    ],
    callback = ['mat_help_fond'],
    align = [1]
).inline_keyboard

MAT_HELP_PROF_KEYBOARD = ListOfButtons(
    text = [
        'Из средств бюджета Просоюза СПбПУ'
    ],
    callback = ['mat_help_prof'],
    align = [1]
).inline_keyboard

INSTITUTE_KEYBOARD = ListOfButtons(
    text = [
        'Инженерно-строительный (ИСИ)', 
        'Энергетики (ИЭ)',
        'Физики, нанотехнологий и телекоммуникаций (ИФНиТ)',
        'Машиностроения, материалов и транспорта (ИММиТ)',
        'Компьютерных наук и технологий (ИКНТ)',
        'Прикладной математики и механики (ИПММ)',
        'Промышленного менеджмента, экономики и торговли (ИПМЭиТ)',
        'Гуманитарный институт (ГИ)',
        'Передовых производственных технологий (ИППТ)',
        'Биомедицинских систем и биотехнологий (ИБСиБ)',
        'Средне-профессионального образования (ИСПО)',
        'Аспирантура',
        'Институт кибербезопасности и защиты информации (ИКиЗИ)',
        'Отменить действие'
    ],
    callback=['isi', 'ia', 'ifnit', 'immit', 'iknt', 'ipmm', 'ipmait', 'gi', 'ippt', 'ibsib', 'ispo', 'aspirantura', 'ikizi', 'cancel_institute'],
    align=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
).inline_keyboard

MAT_HELP_CATEGORY_PROF_LIST = """
1. Категория проф
"""

MAT_HELP_CATEGORY_FOND_LIST = """
1. Категория фонд
"""


MAT_HELP_CATEGORY_PROF_DICT = {
    1: "категория проф"
}

MAT_HELP_CATEGORY_FOND_DICT = {
    1: "категория фонд"
}

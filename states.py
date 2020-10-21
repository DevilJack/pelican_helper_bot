from aiogram.dispatcher.filters.state import StatesGroup, State


class ServiceForm(StatesGroup):
    password_for_service = State()
    building = State()
    room = State()
    audience = State()
    date_interval = State()
    time_interval = State()
    goal = State()
    responsible = State()
    confirm = State()
    filename = State()

class MatHelpForm(StatesGroup):
    prof_or_fond = State()
    name = State()
    category = State()
    institute = State()
    passport = State()
    registration = State()
    inn = State()
    birth_date = State()
    phone_number = State()
    card_info = State()
    now_date = State()
    name_inic = State()
    confirm = State()
    filename = State()
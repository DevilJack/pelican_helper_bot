from aiogram.dispatcher.filters.state import StatesGroup, State


class ServiceForm(StatesGroup):
    building = State()
    room = State()
    audience = State()
    date_interval = State()
    time_interval = State()
    goal = State()
    responsible = State()
    confirm = State()
    filename = State()
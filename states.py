from aiogram.dispatcher.filters.state import StatesGroup, State

class DataState(StatesGroup): 
    status = State()
    ism_familiya = State()
    yosh = State()
    texnologiya = State()
    telefon = State()
    hudud = State()
    narx = State()
    kasb = State()
    murojat_vaqti = State()
    ish_vaqti = State()
    maqsad = State()
    ha_yoq = State()
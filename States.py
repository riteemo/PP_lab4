from aiogram.filters.state import StatesGroup, State


class Form(StatesGroup):
    artist_name = State()
    favorite_artist = State()

from aiogram.filters.state import StatesGroup, State


# Класс для ведения диалога с ботом
class Form(StatesGroup):
    artist_name = State() # установка имени артиста (для чарта)
    favorite_artist = State() # установка имени артиста (для бд и рандомных песен)

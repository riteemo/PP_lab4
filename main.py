import asyncio
import logging
import sys
import os
import aiogram.filters
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from YandexMusicAPI import YandexMusicAPI
from States import Form
from Postgres import Postgres

load_dotenv()
my_token = os.getenv("TOKEN")
ym_client = YandexMusicAPI(os.getenv("YM_TOKEN"))
dp = Dispatcher()
db = Postgres()


# Обработка команды получение рейтинга треков артиста
@dp.message(aiogram.filters.Command("get_chart_by_artist"))
async def get_chart_by_artist(message: types.Message, state: FSMContext):
    await message.answer("Отправьте мне имя исполнителя или название группы.")
    await state.set_state(Form.artist_name)


@dp.message(Form.artist_name)
async def process_artist_name(message: types.Message, state: FSMContext):
    await state.update_data(artist_name=message.text)
    res = await ym_client.get_chart_by_artist(message.text)
    if res:
        await message.answer(res)
    else:
        await message.answer("Что-то пошло не так...")
    await state.clear()


# Обработка команды установки любимого артиста
@dp.message(aiogram.filters.Command("set_favorite_artist"))
async def set_favorite_artist(message: types.Message, state: FSMContext):
    await message.answer("Отправьте мне имя любимого исполнителя.")
    await state.set_state(Form.favorite_artist)


@dp.message(Form.favorite_artist)
async def process_favorite_artist(message: types.Message, state: FSMContext):
    await state.update_data(favorite_artist=message.text)
    print(await db.insert(message.from_user.username, message.text))
    await message.answer("Успешно! Любимый артист выбран.")
    await state.clear()


# Обработка команды получения рандомной песни любимого артиста
@dp.message(aiogram.filters.Command("get_random_song"))
async def get_random_song(message: types.Message):
    val = await db.get_favorite_artist_by_user(message.from_user.username)
    if val:
        res = await ym_client.get_random_song(val)
        if res:
            await message.answer(res)
        else:
            await message.answer(f'''Что-то пошло не так...Попробуйте изменить имя артиста.
Ваш любимый артист сейчас: {val}''')
    else:
        await message.answer('''Вы не выбрали любимого исполнителя.
Чтобы сделать это, воспользуйтесь командой /set_favorite_artist''')


# Обработка команды начала работы с ботом
@dp.message(aiogram.filters.Command("start"))
async def start_func(message: types.Message):
    await message.answer(f'''Привет, {message.from_user.username}!
     
Я Snoopy - твой личный помощник в мире музыки! 🐶 Помогу тебе следить за трендами и подбирать песни на твой вкус.
     
Используйте следующие команды чтобы начать работу:
/get_chart  - получить чарт на текущий момент
/get_chart_by_artist - получить топ 10 песен исполнителя
/set_favorite_artist - назначить любимого исполнителя
/get_random_song - получить случайную песню по любимому исполнителю''')


# Обработка команды получения рейтинга песен
@dp.message(aiogram.filters.Command("get_chart"))
async def get_chart(message: types.Message):
    await message.answer(await ym_client.get_chart())


# Обработка получения неизвестной команды
@dp.message()
async def unknown_command(message: types.Message):
    await message.answer("Гав-гав...")


async def main():
    await db.connect()
    bot = Bot(my_token) # создание бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

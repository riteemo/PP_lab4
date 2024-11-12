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

load_dotenv()
my_token = os.getenv("TOKEN")
ym_client = YandexMusicAPI(os.getenv("YM_TOKEN"))
dp = Dispatcher()


@dp.message(aiogram.filters.Command("start"))
async def start_func(message: types.Message):
    await message.answer(f"Hello, {message.from_user.username}")


@dp.message(aiogram.filters.Command("get_chart"))
async def get_chart(message: types.Message):
    await message.answer(await ym_client.get_chart())


@dp.message(aiogram.filters.Command("get_chart_by_artist"))
async def get_chart_by_artist(message: types.Message, state: FSMContext):
    await message.answer("Enter the artist's name")
    await state.set_state(Form.artist_name)


@dp.message(aiogram.filters.Command("set_favorite_artist"))
async def set_favorite_artist(message: types.Message, state: FSMContext):
    await message.answer("Enter the favorite artist's name")
    await state.set_state(Form.favorite_artist)


@dp.message(aiogram.filters.Command("get_random_song"))
async def get_random_song(message: types.Message, state: FSMContext):
    val = await state.get_value("favorite_artist")
    if val:
        await message.answer(await ym_client.get_random_song_by_artist(val))
    else:
        await message.answer("No artist selected")


@dp.message(Form.artist_name)
async def process_artist_name(message: types.Message, state: FSMContext):
    await state.update_data(artist_name=message.text)
    await message.answer(await ym_client.get_chart_by_artist(message.text))


@dp.message(Form.favorite_artist)
async def process_favorite_artist(message: types.Message, state: FSMContext):
    print(await state.get_value("favorite_artist"))
    await state.update_data(favorite_artist=message.text)
    await message.answer("Artist selected")


async def main():
    bot = Bot(my_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

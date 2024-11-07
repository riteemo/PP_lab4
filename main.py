import asyncio
import logging
import sys
import aiogram.filters
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
import os

load_dotenv()
my_token = os.getenv("TOKEN")

dp = Dispatcher()


@dp.message(aiogram.filters.Command("start"))
async def start_func(message: types.Message):
    await message.answer(f"Hello, {message.from_user.username}\nI'm bot ")


async def main():
    bot = Bot(my_token)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

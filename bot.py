import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()
bot = Bot(os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Это мой первый Telegram бот 🤖")

@dp.message()
async def echo(message: Message):
    await message.answer(f"Ты написал: {message.text}")

if __name__ == "__main__":
    dp.run_polling(bot)
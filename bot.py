import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
client = OpenAI(api_key=OPENAI_API_KEY)

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Напиши описание изображения, и я сгенерирую картинку 🎨🤖")

@dp.message()
async def generate_image(message: Message):
    prompt = message.text
    await message.answer(f"Генерирую изображение, подожди 5-10 секунд... 🔄🤗")

    img = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    await message.answer_photo(img.data[0].url, caption="Изображение готово!😊")

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
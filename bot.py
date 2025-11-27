import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

MODEL = "stabilityai/stable-diffusion-2" # бесплатная текст→картинка модель
HF_API_URL = f"https://router.huggingface.co/route/text-to-image/{MODEL}"


def generate_image(prompt: str) -> bytes:
    payload = {
        "inputs": prompt,
    }

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Accept": "image/png"
    }

    response = requests.post(HF_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise ValueError(f"HuggingFace API error {response.status_code}: {response.text}")

    return response.content

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Напиши описание изображения, и я сгенерирую картинку 🎨🤖")

@dp.message()
async def on_message(message: Message):
    prompt = message.text

    await message.answer(f"Генерирую изображение, подожди 5-10 секунд... 🔄🤗")

    try:
        img = generate_image(prompt)
        await message.answer_photo(photo=img, caption="Изображение готово!😊")
    except Exception as e:
        await message.answer(f"Ошибка генерации: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
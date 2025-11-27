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

HF_MODEL = "stabilityai/stable-diffusion-2"


def generate_image(prompt: str) -> bytes:
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt}

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise ValueError(f"HuggingFace API error {response.status_code}: {response.text}")

    return response.content

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Напиши описание изображения, и я сгенерирую картинку 🎨🤖")

@dp.message()
async def generate_msg(message: Message):
    prompt = message.text
    await message.answer(f"Генерирую изображение, подожди 5-10 секунд... 🔄🤗")

    try:
        img_bytes = generate_image(prompt)
        await message.answer_photo(photo=img_bytes, caption="Изображение готово!😊")
    except Exception as e:
        await message.answer(f"Ошибка генерации: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from dotenv import load_dotenv
from io import BytesIO
from huggingface_hub import InferenceClient

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

hf_client = InferenceClient(
    provider="fal-ai",
    api_key=HF_TOKEN,
)


def generate_image(prompt: str):
    try:
        # Генерация изображения через SD3-medium
        img = hf_client.text_to_image(
            prompt,
            model="stabilityai/stable-diffusion-3-medium",
        )

        # Конвертируем PIL.Image → bytes
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    except Exception as e:
        raise ValueError(f"Ошибка генерации: {e}")

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Просто напиши описание изображения, и я сгенерирую картинку 🎨🤖")

@dp.message()
async def on_message(message: Message):
    prompt = message.text

    await message.answer(f"Генерирую изображение, подожди 5-10 секунд... 🔄🤗")

    result = generate_image(prompt)

    if isinstance(result, str):
        await message.reply(result)  # Ошибка
        return

    await message.reply_photo(result, caption=f"Готово!\n\nПромпт: {prompt}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
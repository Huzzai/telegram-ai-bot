import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from groq import AsyncGroq, RateLimitError, APIStatusError
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not TELEGRAM_TOKEN or not GROQ_API_KEY:
    raise ValueError("❌ Missing TELEGRAM_BOT_TOKEN or GROQ_API_KEY in .env")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()  # ✅ CORRECT: no arguments
groq_client = AsyncGroq(api_key=GROQ_API_KEY)

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("🚀 Hi! I'm Llama 3 on Groq — ask me anything!")

@dp.message(F.text)
async def chat(message: Message):
    try:
        completion = await groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": message.text}],
            max_tokens=512
        )
        reply = (
            completion.choices[0].message.content.strip()
            if completion.choices and completion.choices[0].message and completion.choices[0].message.content
            else "❌ No response from model"
        )
        await message.answer(reply[:4000])
        
    except RateLimitError:
        await message.answer("⏳ Too many requests. Try again in 10 seconds.")
    except APIStatusError as e:
        if e.status_code == 400 and "token" in str(e).lower():
            await message.answer("⚠️ Your message is too long. Please shorten it.")
        else:
            await message.answer(f"⚠️ API error ({e.status_code}): {str(e)[:150]}")
    except Exception as e:
        await message.answer(f"❌ Unexpected error: {str(e)[:200]}")

async def main():
    await dp.start_polling(bot)  # ✅ bot passed here

if __name__ == "__main__":
    asyncio.run(main())
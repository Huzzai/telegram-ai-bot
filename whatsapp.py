import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from groq import AsyncGroq

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
WEBHOOK_PATH = "/webhook"   # <-- FIXED

if not TELEGRAM_BOT_TOKEN or not GROQ_KEY:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN or GROQ_API_KEY")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
groq = AsyncGroq(api_key=GROQ_KEY)

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Bot online — Groq + Aiogram v3 running.")

@dp.message()
async def reply(message: Message):
    try:
        resp = await groq.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": message.text}],
            max_tokens=300
        )
        await message.answer(resp.choices[0].message.content[:4000])
    except Exception as e:
        await message.answer(f"Error: {str(e)[:200]}")

async def main():
   async def main():
    app = web.Application()

    webhook_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    return app



if __name__ == "__main__":
    web.run_app(main(), host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

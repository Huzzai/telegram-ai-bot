import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from groq import AsyncGroq

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
WEBHOOK_PATH = "https://telegram-ai-bot-fyak.onrender.com/webhook"

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
    app = web.Application()


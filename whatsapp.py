import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from groq import AsyncGroq

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
WEBHOOK_URL = os.getenv("https://telegram-ai-bot-fyak.onrender.com")  # Full URL: https://your-bot.onrender.com/webhook

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
groq = AsyncGroq(api_key=GROQ_KEY)
chat_histories = {}

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Hi! I'm your AI assistant. Send me a message!")

@dp.message()
async def echo(message: Message):
    chat_id = message.chat.id
    if chat_id not in chat_histories:
        chat_histories[chat_id] = []
    chat_histories[chat_id].append({"role": "user", "content": message.text})
    
    try:
        completion = await groq.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=chat_histories[chat_id][-6:],
            max_tokens=300
        )
        reply = completion.choices[0].message.content
        chat_histories[chat_id].append({"role": "assistant", "content": reply})
        await message.answer(reply[:4000])
    except Exception as e:
        await message.answer(f"❌ Error: {str(e)[:200]}")

async def main():
    # Set webhook
    await bot.set_webhook(url=WEBHOOK_URL)
    logging.info(f"Webhook set to {WEBHOOK_URL}")
    
    # Start webhook listener (aiogram handles server internally)
    await dp.start_polling(bot)  # ❌ NO! For webhooks, use:
    # Actually — for webhooks, you must use a web framework. But aiogram v3.23+ has a built-in way:

# ✅ CORRECT: Use aiogram's built-in webhook runner
if __name__ == "__main__":
    import asyncio
    from aiogram.webhook.aiohttp_server import setup_server
    from aiohttp import web

    async def on_startup(app):
        await bot.set_webhook(WEBHOOK_URL)

    app = web.Application()
    setup_server(app, dp, bot, "/webhook")
    app.on_startup.append(on_startup)
    
    PORT = int(os.getenv("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=PORT)

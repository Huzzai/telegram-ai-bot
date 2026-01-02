# bot.py
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleAIOHTTPWebhookServer
from groq import AsyncGroq

# Configure logging
logging.basicConfig(level=logging.INFO)

# Environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WEBHOOK_HOST = os.getenv("https://telegram-ai-bot-fyak.onrender.com")  # e.g., https://your-bot.onrender.com
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
PORT = int(os.getenv("PORT", 10000))

# Initialize
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
groq = AsyncGroq(api_key=GROQ_API_KEY)
chat_histories = {}

@dp.message(Command("start", "clear"))
async def start(message: Message):
    chat_histories[message.chat.id] = []
    await message.answer("Hi! I'm powered by Llama 3.1 via Groq — ask me anything!")

@dp.message(F.text)
async def handle_text(message: Message):
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
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook set to {WEBHOOK_URL}")

    # Start aiohttp server
    server = SimpleAIOHTTPWebhookServer(
        dispatcher=dp,
        bot=bot,
        handle_path=WEBHOOK_PATH
    )
    await server.start(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    asyncio.run(main())

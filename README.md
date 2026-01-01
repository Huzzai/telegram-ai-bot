# Telegram AI Bot

A fast, free, and open-source Telegram chatbot powered by:
- **Groq** (free Llama 3.1 inference)
- **aiogram** (Python Telegram framework)

💬 Users can send text, and the bot replies using **Llama 3.1 8B**, hosted on Groq’s ultra-fast inference API.

## Features
- Real-time AI responses via Telegram
- Multi-turn conversation memory (remembers last 3 exchanges)
- `/clear` command to reset chat history
- Deployable to **Render** (free cloud hosting)
- No payment required (uses Groq’s free tier)

## Setup

### 1. Create a Telegram Bot
- Message **[@BotFather](https://t.me/BotFather)** on Telegram
- Use `/newbot` to create a bot
- Copy the **API token** (e.g., `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### 2. Get a Groq API Key
- Go to [https://console.groq.com](https://console.groq.com)
- Sign up → **no payment needed**
- Create an API key → copy it (`gsk_...`)

### 3. Clone & Configure
```bash
git clone https://github.com/Huzzai/telegram-ai-bot.git
cd telegram-ai-bot

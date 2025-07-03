import os
from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI, Request
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

app = FastAPI()


@dp.message()
async def handle_message(message: types.Message):
    await message.reply("Привет! Бот работает через webhook.")


@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)


@app.post("/webhook")
async def telegram_webhook(req: Request):
    update = types.Update(**await req.json())
    await dp.feed_update(bot, update)
    return {"status": "ok"}

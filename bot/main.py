import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from fastapi import FastAPI, Request

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "")
WEBHOOK_URL = RENDER_EXTERNAL_URL + WEBHOOK_PATH

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_message(message: Message):
    await message.answer("Привет! Бот работает на webhook (FastAPI).")

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)

@app.post(WEBHOOK_PATH)
async def process_webhook(request: Request):
    body = await request.body()
    update = types.Update.parse_raw(body)
    await dp.feed_update(bot, update)
    return {"ok": True}

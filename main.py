import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set")

WEBHOOK_HOST = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 5000))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("Привет! 👋 Я бот, который крутится на Render 🚀")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    print("Webhook установлен!")

async def on_shutdown(dp):
    await bot.delete_webhook()
    print("Webhook удалён!")

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )

from aiogram import Bot, Dispatcher
from handlers.commands import router as commands_router
import os

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
dp.include_router(commands_router)
from aiogram import Bot, Dispatcher
from handlers.commands import router as commands_router
import os

API_TOKEN = '8305223003:AAGGk5NoBE2l01OdjA6pFFXUEXleqZLviFU'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
dp.include_router(commands_router)
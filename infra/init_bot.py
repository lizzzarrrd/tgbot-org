from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from adapters.handlers.start import StartHandler
from adapters.handlers.send_message import MessageSender
#импротируем нужные библиотеки потом из инита лучше
import asyncio
import os

API_TOKEN = '8305223003:AAGGk5NoBE2l01OdjA6pFFXUEXleqZLviFU'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
# Ручка для команды /start


@dp.message(CommandStart())
async def start_handler(message: Message):
    sender = MessageSender(bot)
    await StartHandler(sender=sender).handle(message)


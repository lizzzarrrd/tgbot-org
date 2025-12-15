from aiogram import Router, Bot, Dispatcher
from aiogram import types
from aiogram.filters import CommandStart

from adapters.handlers.start import StartHandler
from adapters.handlers.get_message import MessageHandler
from adapters.send_message import MessageSender

#импротируем нужные библиотеки потом из инита лучше

API_TOKEN = '8305223003:AAGGk5NoBE2l01OdjA6pFFXUEXleqZLviFU'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

router = Router()
dp.include_router(router)

sender = MessageSender(bot)
start_handler = StartHandler(sender)
message_handler = MessageHandler(sender)
    
@router.message(CommandStart())
async def start_command(message: types.Message):
    await StartHandler(sender=sender).handle(message)


@router.message()
async def all_messages(message: types.Message):
    await MessageHandler(sender=sender).handle(message)
from aiogram import Router, Bot, Dispatcher
from aiogram import F, types
from aiogram.filters import CommandStart

from adapters import MessageHandler, MessageSender, StartHandler, ConfirmHandler
from domain.all_buttons_types import ConfirmButton

API_TOKEN = '8305223003:AAGGk5NoBE2l01OdjA6pFFXUEXleqZLviFU'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

router = Router()
dp.include_router(router)

sender = MessageSender(bot)
start_handler = StartHandler(sender)
message_handler = MessageHandler(sender)
confirm_handler = ConfirmHandler(sender)
    
@router.message(CommandStart())
async def start_command(message: types.Message):
    await start_handler.handle(message)

@router.message()
async def all_messages(message: types.Message):
    await message_handler.handle(message)

@router.callback_query(F.data.in_({ConfirmButton.YES, ConfirmButton.NO}))
async def confirm_callbacks(callback: types.CallbackQuery):
    await confirm_handler.handle(callback)
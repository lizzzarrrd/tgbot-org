from aiogram import Router, Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from core.config import settings

storage = MemoryStorage()

API_TOKEN_BOT = settings.api_token_bot

bot: Bot = Bot(token=API_TOKEN_BOT)
dp: Dispatcher = Dispatcher()

router: Router = Router()
dp.include_router(router)


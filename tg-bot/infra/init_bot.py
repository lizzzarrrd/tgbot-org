from aiogram import Router, Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

load_dotenv()
storage = MemoryStorage()


API_TOKEN: str = os.getenv("API_TOKEN_BOT")
if not API_TOKEN:
    raise RuntimeError("API_TOKEN_BOT not found in environment variables")

bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

router: Router = Router()
dp.include_router(router)


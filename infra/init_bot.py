from aiogram import Router, Bot, Dispatcher

API_TOKEN = '8305223003:AAGGk5NoBE2l01OdjA6pFFXUEXleqZLviFU'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

router = Router()
dp.include_router(router)

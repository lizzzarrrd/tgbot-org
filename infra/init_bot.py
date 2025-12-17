from aiogram import Router, Bot, Dispatcher

API_TOKEN = '8305223003:AAGGk5NoBE2l01OdjA6pFFXUEXleqZLviFU'

bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

router: Router = Router()
dp.include_router(router)
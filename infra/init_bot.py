from __future__ import annotations

import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

API_TOKEN = '8305223003:AAGGk5NoBE2l01OdjA6pFFXUEXleqZLviFU'
#плохо, потом уберем в окружение, чтобы скрыть
async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    token = API_TOKEN
    if not token:
        raise RuntimeError("BOT_TOKEN is not set")

    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start_handler(message: Message) -> None:
        await message.answer("Егор чемпион (и Паша тоже ) 👋")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
import asyncio
from infra.init_bot import bot, dp
import logging
import adapters.routes # импорт не удалять, он на самом деле используется 

logging.basicConfig(level=logging.INFO)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
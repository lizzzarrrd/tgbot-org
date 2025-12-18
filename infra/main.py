import asyncio
from infra.init_bot import bot, dp
import logging
import adapters.routes # импорт не удалять, он на самом деле используется 

from .init_db import engine
from domain.database.base import Base

logging.basicConfig(level=logging.INFO)

async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(main())
    

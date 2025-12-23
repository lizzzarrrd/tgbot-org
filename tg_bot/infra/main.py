import asyncio
import logging

from .init_bot import bot, dp, router
from .init_db import engine
from tg_bot.domain.database.base import Base
from tg_bot.adapters import InitRoute

routes = InitRoute
routes.setup_routes(router)

logging.basicConfig(level=logging.INFO)

async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    

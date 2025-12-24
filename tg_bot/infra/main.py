import asyncio
import logging

from tg_bot import bot, dp, router
from tg_bot import engine
from tg_bot import Base
from tg_bot import InitRoute

from tg_bot.infra.google_oauth_server import start_google_oauth_server, cleanup_oauth_states_task

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    InitRoute.setup_routes(router)

    await start_google_oauth_server()
    asyncio.create_task(cleanup_oauth_states_task())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

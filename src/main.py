import asyncio

from aiogram import Bot, Dispatcher

from core.config import settings
from handlers import start, ping, help, stats


async def main():

    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(ping.router)
    dp.include_router(help.router)
    dp.include_router(stats.router)

    # Запускаем бота
    await dp.start_polling(settings.telegram_bot)

if __name__ == "__main__":
    asyncio.run(main())
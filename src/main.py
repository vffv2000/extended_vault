import asyncio

from aiogram import Bot, Dispatcher

from core.config import settings
from handlers import start, ping


async def main():
    bot = Bot(token=settings.telegram_bot_api_key)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(ping.router)

    # Запускаем бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
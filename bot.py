import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config_reader import config
from data.requests import get_new_deposit_monero

from handlers import user_commands
from callbacks import navigation, withdraw
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls

    bot = Bot(config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode="HTML"))
    # All handlers should be attached to the Router (or Dispatcher)
    dp = Dispatcher()
    scheduler = AsyncIOScheduler()

    scheduler.add_job(get_new_deposit_monero, trigger="interval", seconds=15)
    scheduler.start()
    dp.include_routers(user_commands.router,
                       navigation.router,
                       withdraw.router,
                       )
    await bot.delete_webhook(drop_pending_updates=True)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # Получаем event loop
    loop = asyncio.get_event_loop()
    # Устанавливаем asyncio event loop для apscheduler
    scheduler = AsyncIOScheduler()
    scheduler.configure(loop=loop)
    # Запускаем main()
    loop.run_until_complete(main())

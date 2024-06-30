import asyncio
import sys
import logging

from config import *
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers.commands import router as commands_router
from base.queries.user import nickname as get_user_by_nickname
from base.commands.user import add as add_user
from tasks.dummy import DummyTask
from tasks.tasker import Tasker

configuration = Config()
dp = Dispatcher()
bot = Bot(token=configuration.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def on_startup():
    tasker = Tasker()

    # Add tasks here
    tasker.add_task(DummyTask(5))

    # Run the tasks
    _ = asyncio.create_task(tasker.run())


async def main():
    # Add the bootstrap user to the database
    user = get_user_by_nickname(configuration.BOOTSTRAP_USER)

    if not user:
        user = add_user(0, 'Bootstrap User', 'Bootstrap User', configuration.BOOTSTRAP_USER)
        if user:
            logging.info(f"Bootstrap user added to the database: {user.nickname}")
        else:
            logging.error(f"Failed to add bootstrap user to the database: {configuration.BOOTSTRAP_USER}")
            return

    # Start the bot
    dp.include_router(commands_router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # Set up logging
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # Turn off the logging
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    asyncio.run(main())

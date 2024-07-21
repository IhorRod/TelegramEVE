import asyncio
import logging
import sys
from typing import List

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from base.commands.user import add as add_user
from base.queries.user import nickname as get_user_by_nickname
from config import *
from handlers.commands import router as commands_router
from handlers.menu import router as menu_router
from tasks.dummy import DummyTask
from tasks.task import Task

"""
This module contains the main entry point of the bot.
"""

configuration = Config()
dp = Dispatcher()
bot = Bot(token=configuration.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
scheduler = AsyncIOScheduler()


async def on_startup():
    # Collection of tasks to be run on startup
    tasks_to_start: List[Task] = [
        DummyTask()
    ]

    # Add the bot to the database
    for task in tasks_to_start:
        scheduler.add_job(task.func, task.trigger, **task.timer, id=task.id, name=task.name)

    # Start the scheduler
    scheduler.start()
    logging.info("Started background scheduler")


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
    dp.include_routers(commands_router, menu_router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # Set up logging
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # Turn off the logging
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    asyncio.run(main())

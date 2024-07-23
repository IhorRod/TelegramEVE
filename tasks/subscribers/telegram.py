from .subscriber import Subscriber
from aiogram import Bot


class Telegram(Subscriber):
    _bot: Bot

    def __init__(self, bot: Bot):
        self._bot = bot

    async def info(self, message: str):
        await self._bot.send_message(chat_id=0, text=message)

    async def error(self, message: str):
        await self._bot.send_message(chat_id=0, text=message)

from base.db import SubscriptionDelivers
from base.model import Subscription
from .subscriber import Subscriber
from aiogram import Bot
from base.queries.user import get_id as get_user_id


class Telegram(Subscriber):
    _bot: Bot

    def __init__(self, bot: Bot):
        self._bot = bot

    @property
    def sub_type(self):
        return SubscriptionDelivers.TG

    async def info(self, subscription: Subscription, message: str):
        user = get_user_id(subscription.sub_id)
        if user:
            await self._bot.send_message(chat_id=user.tgid, text=message)

    async def error(self, subscription: Subscription, message: str):
        user = get_user_id(subscription.sub_id)
        if user:
            await self._bot.send_message(chat_id=user.tgid, text=message)

from base.db import SubscriptionDelivers
from base.model import Subscription
from .subscriber import Subscriber
import logging


class DummySubscriber(Subscriber):

    @property
    def sub_type(self):
        return SubscriptionDelivers.LOG

    async def info(self, subscription: Subscription, message: str):
        logging.info(message)

    async def error(self, subscription: Subscription, message: str):
        logging.error(message)

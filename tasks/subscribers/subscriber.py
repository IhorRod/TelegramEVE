from abc import ABC, abstractmethod

from base.db import SubscriptionDelivers
from base.model import Subscription


class Subscriber(ABC):
    @property
    @abstractmethod
    def sub_type(self) -> SubscriptionDelivers:
        """
        Returns the type of the subscriber
        """
        ...

    @abstractmethod
    async def info(self, subscription: Subscription, message: str):
        """
        Log an informational message

        :param subscription: The subscription that the message is related to
        :param message: The message to log
        """
        ...

    @abstractmethod
    async def error(self, subscription: Subscription, message: str):
        """
        Log an error message

        :param subscription: The subscription that the message is related to
        :param message: The message to log
        """
        ...

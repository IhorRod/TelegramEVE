from typing import Dict, Any, Optional, List

from aiogram import Bot

from base.db import SubscriptionDelivers
from .factory import AbstractFactory
from tasks.subscribers.subscriber import Subscriber
from strenum import StrEnum


class SubscriberType(StrEnum):
    DUMMY = 'dummy'
    TG = 'tg'


class SubscriberFactory(AbstractFactory):
    _configuration: List[str]
    _arguments: Dict[str, Any]
    _subscribers: Dict[SubscriptionDelivers, Subscriber]

    def __init__(self, configuration: List[str], **kwargs):
        self._configuration = configuration
        self._arguments = kwargs
        self._subscribers = {}

    def create(self, specification: SubscriberType, **kwargs) -> Subscriber:
        """
        Create a subscriber.

        :param specification: The type of the subscriber to create.
        :param kwargs: Keyword arguments to pass to the subscriber constructor.
        :return: The created subscriber.
        """
        match specification:
            case SubscriberType.DUMMY:
                from tasks.subscribers.dummy import DummySubscriber
                return DummySubscriber()
            case SubscriberType.TG:
                from tasks.subscribers.telegram import TelegramSubscriber
                tgbot: Optional[Bot] = self._arguments.get('tgbot', None)
                if tgbot is None:
                    raise ValueError("Telegram bot is required for Telegram subscriber.")
                return TelegramSubscriber(tgbot)
            case _:
                raise ValueError(f"Unknown subscriber type: {specification}")

    def __collect(self):
        """
        Collect all subscribers.
        """
        for subtype in self._configuration:
            sbtype = SubscriberType(subtype)
            subscriber = self.create(sbtype)
            self._subscribers[subscriber.sub_type] = subscriber

    def get(self, sub_type: SubscriptionDelivers) -> Optional[Subscriber]:
        """
        Get a subscriber by name.

        :param sub_type: The type of the subscriber.
        :return: The subscriber.
        """
        try:
            return self._subscribers[sub_type]
        except KeyError:
            return None

    def subscribers(self) -> Dict[SubscriptionDelivers, Subscriber]:
        """
        Get all subscribers.

        :return: The subscribers.
        """
        self.__collect()
        return self._subscribers

from typing import Dict, Any, Optional

from persistence.factory import AbstractFactory
from tasks.subscribers.subscriber import Subscriber
from strenum import StrEnum


class SubscriberType(StrEnum):
    DUMMY = 'dummy'


class SubscriberFactory(AbstractFactory):
    _configuration: dict
    _arguments: Dict[str, Any]
    _subscribers: Dict[str, Subscriber]

    def __init__(self, configuration: dict, **kwargs):
        self._configuration = configuration
        self._arguments = kwargs
        self._subscribers = {}
        self.__collect()

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
            case _:
                raise ValueError(f"Unknown subscriber type: {specification}")

    def __collect(self):
        """
        Collect all subscribers.
        """
        for name in self._configuration:
            subconfig: dict = self._configuration[name]

            try:
                subtype = subconfig['specification']
            except KeyError:
                raise ValueError(f"Missing specification for subscriber: {name}")

            subconfig.pop('specification')

            subscriber = self.create(subtype, **subconfig)
            self._subscribers[name] = subscriber

    def get(self, name: str) -> Optional[Subscriber]:
        """
        Get a subscriber by name.

        :param name: The name of the subscriber.
        :return: The subscriber.
        """
        try:
            return self._subscribers[name]
        except KeyError:
            return None

    def has(self, name: str) -> bool:
        """
        Check if a subscriber exists.

        :param name: The name of the subscriber.
        :return: True if the subscriber exists, False otherwise.
        """
        return name in self._subscribers

from abc import ABC, abstractmethod
from typing import Dict, List
from strenum import StrEnum

from tasks.subscribers.subscriber import Subscriber


class Trigger(StrEnum):
    INTERVAL = 'interval'
    CRON = 'cron'
    DATE = 'date'


class Task(ABC):
    __subscribers: List[Subscriber]

    def __init__(self, subscribers: List[Subscriber]):
        self.__subscribers = subscribers

    @property
    @abstractmethod
    def trigger(self) -> Trigger:
        """
        Returns the trigger that will be used to schedule the task execution. ('interval', 'cron', 'date')
        """
        ...

    @property
    @abstractmethod
    def timer(self) -> Dict[str, int]:
        """
        Returns the time dict that will be used to schedule the task execution.

        For 'interval' triggers:
        {'weeks': 0, 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'start_date': None, 'end_date': None,
        'timezone': None, timezone: None, jitter: None}

        For 'cron' triggers:
        {'year': None, 'month': None, 'day': None, 'week': None, 'day_of_week': None, 'hour': None, 'minute': None,
        'second': None, 'start_date': None, 'end_date': None, 'timezone': None, jitter: None}
        """
        ...

    @property
    def id(self):
        return self.name.lower().replace(' ', '_')

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def func(self):
        """
        Returns the function that will be executed by the task.
        """
        return self._func

    @abstractmethod
    async def _func(self):
        """
        The function that will be executed by the task.
        """
        ...

    async def _info(self, message: str):
        for subscriber in self.__subscribers:
            await subscriber.info(message)

    async def _error(self, message: str):
        for subscriber in self.__subscribers:
            await subscriber.error(message)

from typing import Dict, List

from base.db import SubscriptionTypes, SubscriptionDelivers
from .subscribers.subscriber import Subscriber
from .task import Task, Trigger


class DummyTask(Task):

    def __init__(self, subscribers: Dict[SubscriptionDelivers, Subscriber]):
        super().__init__(subscribers)
        self.counter = 0

    @property
    def task_type(self):
        return SubscriptionTypes.DUMMY

    @property
    def trigger(self) -> Trigger:
        return Trigger.INTERVAL

    @property
    def timer(self) -> Dict[str, int]:
        return {'seconds': 5}

    async def _func(self):
        await self._info(f"Counter: {self.counter}")
        self.counter += 1

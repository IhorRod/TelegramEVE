import logging
from typing import Dict, List

from tasks.subscribers.subscriber import Subscriber
from tasks.task import Task, Trigger


class DummyTask(Task):

    def __init__(self, subscribers: List[Subscriber]):
        super().__init__(subscribers)
        self.counter = 0

    @property
    def trigger(self) -> Trigger:
        return Trigger.INTERVAL

    @property
    def timer(self) -> Dict[str, int]:
        return {'seconds': 5}

    def _func(self):
        self._info(f"Counter: {self.counter}")
        self.counter += 1

import logging
from typing import Dict

from tasks.task import Task, Trigger


class DummyTask(Task):

    def __init__(self):
        self.counter = 0

    @property
    def trigger(self) -> Trigger:
        return Trigger.INTERVAL

    @property
    def timer(self) -> Dict[str, int]:
        return {'seconds': 5}

    def _func(self):
        logging.info(f"DummyTask :: Counter: {self.counter}")
        self.counter += 1

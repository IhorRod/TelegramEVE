from typing import List, Dict
from strenum import StrEnum

from base.db import SubscriptionDelivers
from .factory import AbstractFactory
from .subscribers import SubscriberFactory

from tasks.subscribers.subscriber import Subscriber
from tasks.task import Task


class TaskType(StrEnum):
    DUMMY = 'dummy'


class TaskFactory(AbstractFactory):
    _configuration: dict
    _arguments: dict
    _subfactory: SubscriberFactory
    _subscribers: Dict[SubscriptionDelivers, Subscriber]

    def __init__(self, configuration: dict, subfactory: SubscriberFactory, **kwargs):
        self._configuration = configuration
        self._subfactory = subfactory
        self._arguments = kwargs
        self._subscribers = subfactory.subscribers()

    def create(self, specification: TaskType, **kwargs) -> Task:
        """
        Create a task.

        :param specification: The type of the task to create.
        :param kwargs: Keyword arguments to pass to the task constructor.
        :return: The created task.
        """
        match specification:
            case TaskType.DUMMY:
                from tasks.dummy import DummyTask
                return DummyTask(self._subscribers)
            case _:
                raise ValueError(f"Unknown task type: {specification}")

    def collect(self) -> List[Task]:
        """
        Collect all tasks.

        :return: The list of tasks.
        """
        tasks: List[Task] = []
        for taskconfig in self._configuration:
            try:
                specification = taskconfig['specification']
            except KeyError:
                raise ValueError(f"Task configuration missing specification: {taskconfig}")

            taskconfig.pop("specification")
            task = self.create(specification, **taskconfig)
            tasks.append(task)

        return tasks

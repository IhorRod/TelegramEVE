from typing import List
from strenum import StrEnum


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

    def __init__(self, configuration: dict, subfactory: SubscriberFactory, **kwargs):
        self._configuration = configuration
        self._subfactory = subfactory
        self._arguments = kwargs

    def create(self, specification: TaskType, **kwargs) -> Task:
        """
        Create a task.

        :param specification: The type of the task to create.
        :param kwargs: Keyword arguments to pass to the task constructor.
        :return: The created task.
        """
        subscribers: List[Subscriber] = kwargs.get('subscribers', [])
        match specification:
            case TaskType.DUMMY:
                from tasks.dummy import DummyTask
                return DummyTask(subscribers)
            case _:
                raise ValueError(f"Unknown task type: {specification}")

    def collect(self) -> List[Task]:
        """
        Collect all tasks.

        :return: The list of tasks.
        """
        tasks: List[Task] = []
        for name in self._configuration:
            taskconfig: dict = self._configuration[name]
            try:
                specification = taskconfig['specification']
            except KeyError:
                raise ValueError(f"Task configuration missing specification: {name}")

            subscribers = [
                self._subfactory.get(subscriber) for subscriber in taskconfig.get('subscribers', [])
                if self._subfactory.has(subscriber)
            ]

            taskconfig.pop("specification")
            taskconfig.pop("subscribers")
            task = self.create(specification, **taskconfig, subscribers=subscribers)
            tasks.append(task)

        return tasks

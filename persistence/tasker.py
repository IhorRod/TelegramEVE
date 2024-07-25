from typing import List, Dict, Optional
from strenum import StrEnum

from base.db import SubscriptionDelivers, SubscriptionTypes
from config import Config
from .asker import AskerPaginationFactory
from .factory import AbstractFactory
from .subscribers import SubscriberFactory

from tasks.subscribers.subscriber import Subscriber
from tasks.task import Task


class TaskType(StrEnum):
    DUMMY = 'dummy'
    MAILS = 'mails'
    NOTIFICATIONS = 'notifications'


class TaskFactory(AbstractFactory):
    _configuration: Config
    _arguments: dict
    _subfactory: SubscriberFactory
    _subscribers: Dict[SubscriptionDelivers, Subscriber]
    _pafactory: Optional[AskerPaginationFactory]

    _tasks = Dict[SubscriptionTypes, Task]

    def __init__(self, configuration: Config, subfactory: SubscriberFactory, **kwargs):
        self._configuration = configuration
        self._subfactory = subfactory
        self._arguments = kwargs
        self._subscribers = subfactory.subscribers()
        self._pafactory = None
        self._tasks = {}

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
            case TaskType.MAILS:
                from tasks.character import MailTask
                return MailTask(self._subscribers, self.__pagination_factory)
            case TaskType.NOTIFICATIONS:
                from tasks.character import NotificationTask
                return NotificationTask(self._subscribers, self.__pagination_factory)
            case _:
                raise ValueError(f"Unknown task type: {specification}")

    def collect(self) -> List[Task]:
        """
        Collect all tasks.

        :return: The list of tasks.
        """
        tasks: List[Task] = []
        for taskconfig in self._configuration.TASKS:
            try:
                specification = taskconfig['specification']
            except KeyError:
                raise ValueError(f"Task configuration missing specification: {taskconfig}")

            taskconfig.pop("specification")
            task = self.create(specification, **taskconfig)
            tasks.append(task)

            self._tasks[task.task_type] = task

        return tasks

    @property
    def __pagination_factory(self) -> AskerPaginationFactory:
        if not self._pafactory:
            self._pafactory = AskerPaginationFactory(self._configuration.SEAT_URL, self._configuration.SEAT_TOKEN)

        return self._pafactory

    def get(self, task_type: SubscriptionTypes) -> Optional[Task]:
        """
        Get a task by its type.

        :param task_type: The type of the task to get.
        :return: The task or None if not found.
        """
        return self._tasks.get(task_type, None)

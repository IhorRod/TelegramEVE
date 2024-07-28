import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from asker.model.base import BaseObject
from asker.model.character import Mail, Notification
from base.db import SubscriptionTypes, SubscriptionDelivers
from base.model import Subscription
from base.queries.history import exist_ids
from base.commands.history import add_ids
from base.commands.subscription import start_history
from persistence.asker import AskerPaginationFactory
from .subscribers.subscriber import Subscriber
from .task import Task, Trigger


class PaginationTask(Task, ABC):
    _collector: AskerPaginationFactory

    def __init__(self, subscribers: Dict[SubscriptionDelivers, Subscriber], collector: AskerPaginationFactory):
        super().__init__(subscribers)
        self._collector = collector

    def collect(self, target_id: int) -> List[BaseObject]:
        objects: List[BaseObject] = (self._collector
                                     .create(self.task_type, character_id=target_id)
                                     .collect())

        ids = [obj.obj_id for obj in objects]
        checks = exist_ids(ids, target_id, self.task_type)
        filtered = [obj for obj, check in zip(objects, checks) if not check]

        add_ids([obj.obj_id for obj in filtered], target_id, self.task_type)

        return filtered

    @property
    def trigger(self) -> Trigger:
        return Trigger.INTERVAL

    async def _func(self):
        # Group subscriptions by target_id to avoid multiple queries
        grouped = {}
        for subscription in self._subscriptions:
            if subscription.target_id not in grouped:
                grouped[subscription.target_id] = []
            grouped[subscription.target_id].append(subscription)

        for target_id, subscriptions in grouped.items():
            objects = self.collect(target_id)
            for subscription in subscriptions:
                if subscription.history_started:
                    for obj in objects:
                        message = self._process(obj, subscription)
                        if message:
                            await self._info(subscription, message)

                else:
                    logging.info(f"Starting history for subscription {subscription.id} - found {len(objects)} objects")
                    start_history(subscription.id)

    @abstractmethod
    def _process(self, obj: BaseObject, subscription: Subscription) -> Optional[str]:
        """
        Processes the object and returns a message to be sent to the subscriber.

        :param obj: The object to be processed.
        :param subscription: The subscription that triggered the task.

        :return: A message to be sent to the subscriber.
        """
        ...


class MailTask(PaginationTask):
    def _process(self, obj: Mail, subscription: Subscription) -> Optional[str]:
        return f"""
        New mail received:
        From: {obj.sender_name}
        Subject: {obj.subject}
        Date: {obj.timestamp}
        {obj.body}  
        """

    @property
    def timer(self) -> Dict[str, int]:
        return {'seconds': 20}

    @property
    def task_type(self) -> SubscriptionTypes:
        return SubscriptionTypes.MAIL


class NotificationTask(PaginationTask):
    def _process(self, obj: Notification, subscription: Subscription) -> Optional[str]:
        return f"""
        New notification received:
        From: {obj.sender_id}
        Date: {obj.timestamp}
        Type: {obj.type}
        {obj.text}  
        """

    @property
    def timer(self) -> Dict[str, int]:
        return {'minutes': 1}

    @property
    def task_type(self) -> SubscriptionTypes:
        return SubscriptionTypes.NOTIFICATIONS

import json

from .db import TgUser as DBTGUSer, Subscribes as DBSubscribers, SubscriptionHistory as DBTypeHistory, \
    SubscriptionDelivers, SubscriptionTypes


class User:
    """
    TgUser model
    """

    def __init__(self, user: DBTGUSer):
        self.id = user.id
        self.tgid = user.tgid
        self.name = user.name
        self.fullname = user.fullname
        self.nickname = user.nickname


class Subscription:
    """
    Character subscribers model
    """

    def __init__(self, subscriber: DBSubscribers):
        self.id = subscriber.id
        self.sub_deliver: SubscriptionDelivers = subscriber.sub_deliver
        self.sub_id = subscriber.sub_id
        self.sub_type: SubscriptionTypes = subscriber.sub_type
        self.target_id = subscriber.target_id
        self.filter: dict = json.loads(subscriber.filter)
        self.history_started = subscriber.history_started


class TypeHistory:
    def __init__(self, history: DBTypeHistory):
        self.id = history.id
        self.item_id = history.item_id
        self.target_id = history.target_id
        self.item_type: SubscriptionTypes = history.item_type

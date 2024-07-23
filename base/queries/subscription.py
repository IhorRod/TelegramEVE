from typing import Optional, List

from ..db import Session, Subscribes, SubscriptionTypes, SubscriptionDelivers
from ..model import Subscription as SubscriptionModel


def get_id(subscription_id: int) -> Optional[SubscriptionModel]:
    session = Session()
    subscriptionm = None
    try:
        subscription = session.query(Subscribes).filter(Subscribes.id == subscription_id).first()
        if subscription:
            subscriptionm = SubscriptionModel(subscription)
    except Exception as e:
        print(e)
    finally:
        session.close()
    return subscriptionm


def get_type(subscription_type: SubscriptionTypes) -> List[SubscriptionModel]:
    session = Session()
    subscriptionsm = []
    try:
        subscriptions = session.query(Subscribes).filter(Subscribes.sub_type == subscription_type).all()
        for subscription in subscriptions:
            subscriptionsm.append(SubscriptionModel(subscription))
    except Exception as e:
        print(e)
    finally:
        session.close()
    return subscriptionsm

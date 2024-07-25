from typing import List, Optional

from ..db import Session, SubscriptionHistory, SubscriptionTypes


def exist_id(item_id: int, target_id: Optional[int], item_type: SubscriptionTypes) -> bool:
    """
    Check if history item with given ID exists

    :param item_id: ID of the item
    :param target_id: ID of the target
    :param item_type: Type of the item

    :return: True if exists
    """
    session = Session()
    history = (session.query(SubscriptionHistory)
               .filter(SubscriptionHistory.item_id == item_id,
                       SubscriptionHistory.target_id == target_id,
                       SubscriptionHistory.item_type == item_type)
               .first())
    session.close()
    return history is not None


def exist_ids(item_ids: List[int], target_id: Optional[int], item_type: SubscriptionTypes) -> List[bool]:
    """
    Check if history item with given IDs exists

    :param item_ids: IDs of the items
    :param target_id: ID of the target
    :param item_type: Type of the item

    :return: List of booleans
    """
    session = Session()
    history = [h.item_id in item_ids
               for h
               in session.query(SubscriptionHistory)
               .filter(SubscriptionHistory.item_id.in_(item_ids),
                       SubscriptionHistory.target_id == target_id,
                       SubscriptionHistory.item_type == item_type)
               .all()]
    session.close()
    return history

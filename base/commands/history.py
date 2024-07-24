import logging

from ..db import Session, SubscriptionHistory, SubscriptionTypes
from ..queries.history import exist_ids


def add(item_id: int, item_type: SubscriptionTypes) -> bool:
    """
    Add history item to database

    :param item_id: ID of the item
    :param item_type: Type of the item

    :return: True if success
    """
    session = Session()
    try:
        history = SubscriptionHistory(item_id=item_id, item_type=item_type)
        session.add(history)
        session.commit()
        session.close()
        return True
    except Exception as e:
        logging.error(f"Error while adding history item: {e}")
        session.rollback()
        return False
    finally:
        session.close()


def add_ids(ids: list[int], item_type: SubscriptionTypes) -> bool:
    """
    Add history items to database. This is used when multiple items are added at once.
    Should add only ids that are not already in the history.

    :param ids: List of IDs of the items
    :param item_type: Type of the item

    :return: True if success
    """
    ids_check = exist_ids(ids, item_type)
    ids = [item_id for item_id, check in zip(ids, ids_check) if not check]
    if len(ids) == 0:
        return True

    session = Session()
    try:
        history = [SubscriptionHistory(item_id=item_id, item_type=item_type) for item_id in ids]
        session.add_all(history)
        session.commit()
        session.close()
        return True
    except Exception as e:
        logging.error(f"Error while adding history items: {e}")
        session.rollback()
        return False
    finally:
        session.close()

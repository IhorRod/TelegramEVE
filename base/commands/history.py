import logging

from ..db import Session, SubscriptionHistory, SubscriptionTypes


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


import logging
import json

from ..db import Session, Subscribes, SubscriptionTypes, SubscriptionDelivers


def add(sub_deliver: SubscriptionDelivers, sub_id: int, sub_type: SubscriptionTypes, filterer: dict) -> bool:
    session = Session()
    try:
        session.add(Subscribes(sub_deliver=sub_deliver, sub_id=sub_id, sub_type=sub_type, filter=json.dumps(filterer)))
        session.commit()
        return True
    except Exception as e:
        logging.error(f"Error while adding subscription: {e}")
        session.rollback()
        return False
    finally:
        session.close()

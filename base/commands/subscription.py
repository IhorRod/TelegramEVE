import logging
import json
from typing import Optional

from ..db import Session, Subscribes, SubscriptionTypes, SubscriptionDelivers


def add(sub_deliver: SubscriptionDelivers, sub_id: Optional[int], sub_type: SubscriptionTypes, filterer: dict) -> bool:
    session = Session()
    try:
        # Check if the subscription already exists
        if (session.query(Subscribes)
                .filter(Subscribes.sub_deliver == sub_deliver,
                        Subscribes.sub_id == sub_id,
                        Subscribes.sub_type == sub_type)
                .first()):

            raise ValueError(f"Subscription already exists: {sub_deliver} {sub_id} {sub_type}")
        session.add(Subscribes(sub_deliver=sub_deliver, sub_id=sub_id, sub_type=sub_type, filter=json.dumps(filterer)))
        session.commit()
        return True
    except Exception as e:
        logging.error(f"Error while adding subscription: {e}")
        session.rollback()
        return False
    finally:
        session.close()

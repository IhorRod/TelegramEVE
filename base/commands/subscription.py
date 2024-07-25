import logging
import json
from typing import Optional

from ..db import Session, Subscribes, SubscriptionTypes, SubscriptionDelivers


def add(sub_deliver: SubscriptionDelivers,
        sub_id: Optional[int],
        target_id: Optional[int],
        sub_type: SubscriptionTypes,
        filterer: dict) -> bool:
    session = Session()
    try:
        # Check if the subscription already exists
        if (session.query(Subscribes)
                .filter(Subscribes.sub_deliver == sub_deliver,
                        Subscribes.sub_id == sub_id,
                        Subscribes.sub_type == sub_type,
                        Subscribes.target_id == target_id,
                        Subscribes.filter == json.dumps(filterer))
                .first()):
            raise ValueError(f"Subscription already exists: {sub_deliver} {sub_id} {sub_type}")

        session.add(Subscribes(sub_deliver=sub_deliver,
                               sub_id=sub_id,
                               sub_type=sub_type,
                               filter=json.dumps(filterer),
                               target_id=target_id
                               ))
        session.commit()
        return True
    except Exception as e:
        logging.error(f"Error while adding subscription: {e}")
        session.rollback()
        return False
    finally:
        session.close()


def start_history(sub_id: int) -> bool:
    session = Session()
    try:
        session.query(Subscribes).filter(Subscribes.id == sub_id).update({Subscribes.history_started: True})
        session.commit()
        return True
    except Exception as e:
        logging.error(f"Error while starting history: {e}")
        session.rollback()
        return False
    finally:
        session.close()

from typing import Optional

from asker.requester.character import Mails, Notifications
from asker.requester.requester import Pagination
from base.db import SubscriptionTypes
from .factory import AbstractFactory


class AskerPaginationFactory(AbstractFactory):
    _base_url: str
    _token: str

    def __init__(self, base_url: str, token: str):
        self._base_url = base_url
        self._token = token

    def create(self, specification: SubscriptionTypes, **kwargs) -> Pagination:
        match specification:
            case SubscriptionTypes.MAIL:
                character_id: Optional[int] = kwargs.get("character_id", None)
                if character_id is None:
                    raise ValueError("Character ID is required for mail subscription.")
                return Mails(self._base_url, self._token, character_id)
            case SubscriptionTypes.NOTIFICATIONS:
                character_id: Optional[int] = kwargs.get("character_id", None)
                if character_id is None:
                    raise ValueError("Character ID is required for notifications subscription.")
                return Notifications(self._base_url, self._token, character_id)
            case _:
                raise ValueError(f"Unknown subscription type: {specification}")

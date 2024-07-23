from abc import ABC
from typing import Optional, List

from ..model.character import Notification, Mail
from .requester import Pagination


class Character(Pagination, ABC):
    _character_id: int
    _filterer: Optional[str]

    def __init__(self, base_url: str, token: str, character_id: int, filterer: Optional[str] = None):
        super().__init__(base_url, token, character_id, filter=filterer)
        self._character_id = character_id
        self._filterer = filterer

    @property
    def _warn_if_not_total(self) -> str:
        return (f"Total items ({self._total}) does not match the number of items "
                f"({len(self._items)}) for character {self._character_id}")


class Notifications(Character):

    def _equal(self, one: Notification, other: Notification) -> bool:
        return one.notification_id == other.notification_id

    def _transform(self, item: dict) -> Notification:
        return Notification(item)

    def collect(self) -> List[Notification]:
        return super().collect()

    @property
    def _endpoint(self) -> str:
        return "api/v2/character/notifications"


class Mails(Character):

    def _equal(self, one: Mail, other: Mail) -> bool:
        return one.mail_id == other.mail_id

    def _transform(self, item: dict) -> Mail:
        return Mail(item)

    def collect(self) -> List[Mail]:
        return super().collect()

    @property
    def _endpoint(self) -> str:
        return "api/v2/character/mail"


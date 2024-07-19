from typing import Optional, List

from asker.model.character import Notification
from asker.requester.requester import Requester, Pagination


class Notifications(Pagination):
    _notifications: List[Notification]
    _filterer: Optional[str]
    _character_id: int

    def __init__(self, base_url: str, token: str, character_id: int, filterer: Optional[str] = None):
        super().__init__(base_url,
                         "api/v2/character/notifications",
                         token,
                         character_id,
                         filter=filterer)
        self._character_id = character_id
        self._filterer = filterer
        self._notifications = []

    def _equal(self, one: Notification, other: Notification) -> bool:
        """
        Compare two items to see if they are equal
        """
        return one.notification_id == other.notification_id

    def _transform(self, item: dict) -> Notification:
        """
        Transform a dictionary into a Notification object
        """
        return Notification(item)

    def _warn_if_not_total(self) -> str:
        return (f"Total notifications ({self._total}) does not match the number of notifications "
                f"({len(self._notifications)}) for character {self._character_id}")

    def collect(self) -> List[Notification]:
        return super().collect()

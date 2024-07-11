from typing import Optional, List, Tuple

from asker.model.character import Notification
from asker.requester.requester import Requester


class Notifications:
    _next: Optional[str]
    _previous: Optional[str]
    _notifications: List[Notification]
    _base_url: str
    _endpoint: str
    _token: str
    _filterer: Optional[str]
    _character_id: int

    def __init__(self, base_url: str, character_id: int, token: str, filterer: Optional[str] = None):
        self._endpoint = "api/v2/character/notifications"
        self._base_url = base_url
        self._character_id = character_id
        self._token = token
        self._filterer = filterer
        self._next = None
        self._previous = None
        self._notifications = []

    def get(self, page: int = 1) -> Tuple[bool, List[Notification], Optional[str]]:
        """
        Get the notifications from the API

        :return: Success, list of notifications
        """
        url = f"{self._base_url}/{self._endpoint}/{self._character_id}?page={page}&filter={self._filterer}" \
            if self._filterer \
            else f"{self._base_url}/{self._endpoint}/{self._character_id}?page={page}"

        try:
            response = Requester.ask_seat(url, self._token)
            self._next = response.get("links", {}).get("next", None)
            self._previous = response.get("links", {}).get("prev", None)
            notifications = [Notification(notification) for notification in response.get("data", [])]

            for notification in notifications:
                if not any(notification.notification_id == n.notification_id for n in self._notifications):
                    self._notifications.append(notification)

            return True, notifications, None
        except Exception as e:
            return False, [], str(e)

    def next(self) -> Tuple[bool, List[Notification], Optional[str]]:
        """
        Get the next page of notifications

        :return: Success, list of notifications
        """
        if not self._next:
            return False, [], "No next page"

        try:
            response = Requester.ask_seat(self._next, self._token)
            self._next = response.get("links", {}).get("next", None)
            self._previous = response.get("links", {}).get("prev", None)
            notifications = [Notification(notification) for notification in response.get("data", [])]

            for notification in notifications:
                if not any(notification.notification_id == n.notification_id for n in self._notifications):
                    self._notifications.append(notification)

            return True, notifications, None
        except Exception as e:
            return False, [], str(e)

    def previous(self) -> Tuple[bool, List[Notification], Optional[str]]:
        """
        Get the previous page of notifications

        :return: Success, list of notifications
        """
        if not self._previous:
            return False, [], "No previous page"

        try:
            response = Requester.ask_seat(self._previous, self._token)
            self._next = response.get("links", {}).get("next", None)
            self._previous = response.get("links", {}).get("prev", None)
            notifications = [Notification(notification) for notification in response.get("data", [])]

            for notification in notifications:
                if not any(notification.notification_id == n.notification_id for n in self._notifications):
                    self._notifications.append(notification)

            return True, notifications, None
        except Exception as e:
            return False, [], str(e)
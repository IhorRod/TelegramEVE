from typing import Dict, Any

from asker.model.base import BaseObject


class Notification(BaseObject):
    notification_id: int
    type: str
    sender_id: int
    sender_type: str
    timestamp: str
    is_read: bool
    text: Dict[str, Any]

    def _process(self):
        self.notification_id = int(self._raw["notification_id"])
        self.type = self._raw["type"]
        self.sender_id = int(self._raw["sender_id"])
        self.sender_type = self._raw["sender_type"]
        self.timestamp = self._raw["timestamp"]
        self.is_read = self._raw["is_read"]
        self.text = self._raw["text"]

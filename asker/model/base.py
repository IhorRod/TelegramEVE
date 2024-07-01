from typing import Dict, Any


class BaseObject:
    _raw: Dict[str, Any]

    def __init__(self, json: dict):
        self._raw = json
        self._process()

    def _process(self):
        """
        Process the raw data into a more usable format for the object in variables

        :return: None
        """
        pass

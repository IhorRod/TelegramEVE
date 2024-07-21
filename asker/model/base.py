from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseObject(ABC):
    _raw: Dict[str, Any]

    def __init__(self, json: dict):
        self._raw = json
        self.__process_wrapper()

    def __process_wrapper(self):
        try:
            self._process()
        except Exception as e:
            print(f"Error processing {self.__class__.__name__} with {self._raw}")
            raise e

    @abstractmethod
    def _process(self):
        """
        Process the raw data into a more usable format for the object in variables

        :return: None
        """
        raise NotImplementedError

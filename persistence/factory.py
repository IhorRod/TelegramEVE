from abc import ABC, abstractmethod
from typing import Any


class AbstractFactory(ABC):
    @abstractmethod
    def create(self, specification: Any, **kwargs) -> Any:
        """
        Create an object. This method should be implemented by the subclass.

        :param specification: The specification of the object to create.
        :param kwargs: Keyword arguments to pass to the object constructor.
        :return: The created object.
        """
        ...

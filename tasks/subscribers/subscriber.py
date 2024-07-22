from abc import ABC, abstractmethod


class Subscriber(ABC):
    @abstractmethod
    async def info(self, message: str):
        """
        Log an informational message
        :param message: The message to log
        """
        ...

    @abstractmethod
    async def error(self, message: str):
        """
        Log an error message
        :param message: The message to log
        """
        ...

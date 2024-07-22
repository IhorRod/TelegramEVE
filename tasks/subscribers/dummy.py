from .subscriber import Subscriber
import logging


class DummySubscriber(Subscriber):
    async def info(self, message: str):
        logging.info(message)

    async def error(self, message: str):
        logging.error(message)

from tasks.subscribers.subscriber import Subscriber
import logging


class DummySubscriber(Subscriber):
    def info(self, message: str):
        logging.info(message)

    def error(self, message: str):
        logging.error(message)

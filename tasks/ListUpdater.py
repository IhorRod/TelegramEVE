import logging

from config import Config
from tasks.task import Task


class ListUpdater(Task):
    def __init__(self, delay: int, config: Config):
        super().__init__(delay)
        self.base_url = config.SEAT_URL
        self.token = config.SEAT_TOKEN

    def task_body(self):
        logging.info('ListUpdater::List updater is running')
        pass

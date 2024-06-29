import logging

from tasks.task import Task


class DummyTask(Task):
    async def task_body(self):
        logging.info('Dummy task is running')

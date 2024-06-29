import asyncio


class Task:
    """
    Base class for tasks that are run periodically.
    """
    def __init__(self, delay):
        self.delay = delay

    async def task_body(self):
        """
        This method should be overridden by subclasses to provide the actual task functionality.
        """
        pass

    async def run(self):
        """
        Run the task indefinitely.
        :return:
        """
        while True:
            await self.task_body()
            await asyncio.sleep(self.delay)

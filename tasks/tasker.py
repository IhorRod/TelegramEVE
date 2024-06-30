import asyncio

from tasks.task import Task


class Tasker:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    async def run(self):
        await asyncio.gather(*(task.run() for task in self.tasks))

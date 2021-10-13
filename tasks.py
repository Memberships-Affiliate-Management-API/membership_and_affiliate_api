"""
    will start task scheduler as a service
"""
from threading import Thread
from typing import Optional, List

from config.use_context import get_client
from schedulers.scheduler import task_scheduler


def start_task() -> None:

    task_scheduler.run_all(delay_seconds=5)
    task_scheduler.clear()

    return None


class TasksRunManager:
    def __init__(self):
        self.tasks_list: List[Optional[Thread]] = []

    def add_tasks(self, task: Thread):
        if not len(self.tasks_list):
            self.tasks_list.append(task.start())

        for idx, tasks in enumerate(self.tasks_list):
            if tasks is None:
                self.tasks_list[idx] = task.start()

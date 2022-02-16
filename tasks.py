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
    """
        Manager to run api tasks
    """
    def __init__(self):
        self.tasks_list: List[Optional[Thread]] = []

    def add_tasks(self, task: Thread):
        """Given a task as a thread add the task to the list and start it"""
        if not self.tasks_list:
            # if tasks list is empty add task and start it
            self.tasks_list.append(task.start())

        for idx, tasks in enumerate(self.tasks_list):
            # insert task in the first spot that contains a finished task and start it
            if tasks is None:
                self.tasks_list[idx] = task.start()

"""
    will start task scheduler as a service
"""
from config.use_context import get_client
from schedulers.scheduler import task_scheduler


def run_tasks():
    print(f'running tasks...')
    task_scheduler.run_all(delay_seconds=5)
    task_scheduler.clear()
    print('done running tasks')

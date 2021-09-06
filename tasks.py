"""
    will start task scheduler as a service
"""

from schedulers.scheduler import task_scheduler


if __name__ == '__main__':
    task_scheduler.start()

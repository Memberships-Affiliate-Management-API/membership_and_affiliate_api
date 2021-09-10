"""
    will start task scheduler as a service
"""
import time
from time import sleep
from schedulers.scheduler import task_scheduler


def main():
    while True:
        print(f'running tasks...')
        task_scheduler.run_all(delay_seconds=5)
        task_scheduler.clear()
        print(f'tasks fully cleared done running')
        time.sleep(60)
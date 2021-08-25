***REMOVED***
    **scheduler**
        used to dynamically add jobs on a separate thread to complete tasks that should not interfere
        with requests, or requests that takes a long time to complete
***REMOVED***
from typing import Callable
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from utils import create_id as create_unique_id

task_scheduler = BackgroundScheduler()
cron_scheduler = BackgroundScheduler()


def schedule_func(func: Callable, kwargs: dict) -> None:
    ***REMOVED***
    **schedule_cache_deletion**
        schedule cache deletion such that it occurs sometime time in the future
    :param func:
    :param kwargs:
    :return:
    ***REMOVED***
    twenty_seconds_after = datetime.now() + timedelta(seconds=20)
    task_scheduler.add_job(func=func, trigger='date', run_date=twenty_seconds_after, kwargs=kwargs, id=create_unique_id(),
                           name="schedule_func", misfire_grace_time=360)

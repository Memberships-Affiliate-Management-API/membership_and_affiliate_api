"""
    **scheduler**
        used to dynamically add jobs on a separate thread to complete tasks that should not interfere
        with requests, or requests that takes a long time to complete
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from typing import Callable, Hashable, Optional
# noinspection PyUnresolvedReferences
from schedule import Scheduler, Job, repeat, every, run_pending

task_scheduler = Scheduler()
cron_scheduler = Scheduler()


def schedule_func(func: Callable, job_name: str, kwargs: Optional[dict] = None) -> Job:
    """
    **schedule_cache_deletion**
        schedule cache deletion such that it occurs sometime time in the future
    :param func:
    :param kwargs:
    :param job_name
    :return: None
    # schedule
    # twenty_seconds_after = datetime.now() + timedelta(seconds=30)
    # task_scheduler.add_job(func=func, trigger='date', run_date=twenty_seconds_after, kwargs=kwargs, id=create_unique_id(),
    #                        name="schedule_func", misfire_grace_time=360)
    """
    _args: dict = dict()
    _job_names: Hashable = hash(job_name)
    if kwargs:
        return task_scheduler.every(interval=30).seconds.do(func, *_args, **kwargs).tag(_job_names)
    return task_scheduler.every(interval=30).seconds.do(job_func=func).tag(_job_names)

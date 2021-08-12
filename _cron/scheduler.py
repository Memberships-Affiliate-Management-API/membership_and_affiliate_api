from apscheduler.schedulers.background import BackgroundScheduler
from config import config_instance
import asyncio

schedule = BackgroundScheduler()


@schedule.scheduled_job('interval', minutes=5)
def task_run():
    ***REMOVED***
        **task_run**
            launch tasks/processes that must run in a short interval  here

    :return:
    ***REMOVED***
    print("this job run every 5 minutes")


@schedule.scheduled_job('cron', day_of_week='mon-sun', hour=17)
def daily_task_run():
    ***REMOVED***
        **daily_task_run**
            launch daily processes here asynchronously

    :return:
    ***REMOVED***
    print('This job is run every weekday at 5pm.')

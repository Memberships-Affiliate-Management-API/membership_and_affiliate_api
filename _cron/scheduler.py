from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

schedule = BackgroundScheduler()


@schedule.scheduled_job('interval', minutes=5)
def task_run():
    ***REMOVED***
        launch processes here
    :return:
    ***REMOVED***
    print("this job run every 5 minutes")


@schedule.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    ***REMOVED***

    :return:
    ***REMOVED***
    print('This job is run every weekday at 5pm.')

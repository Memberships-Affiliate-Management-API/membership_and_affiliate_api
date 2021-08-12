from apscheduler.schedulers.background import BackgroundScheduler

schedule = BackgroundScheduler()


@schedule.scheduled_job('interval', seconds=3)
def timed_job():
    ***REMOVED***
        launch processes here
    :return:
    ***REMOVED***
    print("this jub run every 3 minutes")


@schedule.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

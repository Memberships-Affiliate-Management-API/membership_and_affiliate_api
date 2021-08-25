from _cron.scheduler import cron_scheduler
from config.exceptions import status_codes


@cron_scheduler.scheduled_job(trigger='cron', day_of_week='mon-sun', hour=1)
def cron_affiliate_jobs() -> tuple:
    ***REMOVED***
    **cron_affiliate_jobs**


    :return:
    ***REMOVED***
    return "OK", status_codes.status_ok_code

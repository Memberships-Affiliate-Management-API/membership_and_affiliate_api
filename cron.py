***REMOVED***
    will start cron scheduler as a service
***REMOVED***
from config import config_instance
from _cron.scheduler import cron_scheduler
from config.exceptions import status_codes
import requests


@cron_scheduler.scheduled_job(trigger='cron', day_of_week='mon-sun', hour=1)
def heroku_cron_affiliate_jobs() -> tuple:
    ***REMOVED***
        **cron_affiliate_jobs**


        :return:
    ***REMOVED***
    _endpoint: str = '_cron/v1/affiliates'
    _base_url: str = config_instance.BASE_URL
    _url: str = f"{_base_url}{_endpoint}"

    requests.get(url=_url)
    return "OK", status_codes.status_ok_code


@cron_scheduler.scheduled_job(trigger='cron', day_of_week='mon-sun', hour=3)
def heroku_cron_memberships() -> tuple:
    ***REMOVED***
        **heroku_cron_memberships**

        :return:
    ***REMOVED***
    _endpoint: str = '_cron/v1/memberships'
    _base_url: str = config_instance.BASE_URL
    _url: str = f"{_base_url}{_endpoint}"
    requests.get(url=_url)
    return "OK", status_codes.status_ok_code


@cron_scheduler.scheduled_job(trigger='cron', day_of_week='mon-sun', hour=5)
def heroku_cron_transactions() -> tuple:
    ***REMOVED***

    :return:
    ***REMOVED***
    _endpoint: str = '_cron/v1/transactions'
    _base_url: str = config_instance.BASE_URL
    _url: str = f"{_base_url}{_endpoint}"
    requests.get(url=_url)
    return "OK", status_codes.status_ok_code


@cron_scheduler.scheduled_job(trigger='cron', day_of_week='mon-sun', hour=7)
def heroku_cron_users() -> tuple:
    ***REMOVED***
        **heroku_cron_users**

        :return:
    ***REMOVED***
    _endpoint: str = '_cron/v1/users'
    _base_url: str = config_instance.BASE_URL
    _url: str = f"{_base_url}{_endpoint}"
    requests.get(url=_url)
    return "OK", status_codes.status_ok_code


if __name__ == '__main__':
    cron_scheduler.start()

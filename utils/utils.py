***REMOVED***
    **Module - Common Application Utilities*
***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import os
import datetime
import random
import string
import time
import typing
from datetime import date
from datetime import time as time_class
from config import config_instance
from flask_caching import Cache
char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits


# NOTE : Cannot use current_app
def is_development() -> bool: return False if config_instance.IS_PRODUCTION else True


# NOTE this environment variable is only found on Heroku
def is_heroku() -> bool: return True if os.environ.get("IS_HEROKU") else False


def create_id(size: int = 64, chars: str = char_set) -> str: return ''.join(random.choice(chars) for _ in range(size))


def timestamp() -> int: return int(float(time.time()) * 1000)


def get_days(days: int) -> int: return int(days * 24 * 60 * 60 * 1000)


def timestamp_difference(stamp1: int, stamp2: int) -> int: return int(stamp1 - stamp2)


def date_string_to_date(date_str: str) -> date:
    ***REMOVED***
        date form dd/mm/yyyy
    ***REMOVED***
    if isinstance(date_str, str):
        if "/" in date_str:
            date_list: typing.List[str] = date_str.split("/")
        elif "-" in date_str:
            date_list: typing.List[str] = date_str.split("-")
        else:
            raise ValueError('Date format invalid')
        try:
            year: int = int(date_list[0])
            month: int = int(date_list[1])
            day: int = int(date_list[2])
        except KeyError:
            raise ValueError("Date Format invalid")
        if 0 < month > 12:
            raise ValueError("Date Format Invalid")
        if 0 < day > 31:
            raise ValueError("Date Format invalid")
        if year < 1990:
            raise ValueError("Date Format invalid")
        return date(year=year, month=month, day=day)
    elif isinstance(date_str, date):
        return date_str
    else:
        raise ValueError('Date format invalid')


# cache functions
def end_of_month() -> bool:
    now: date = datetime.datetime.now().date()
    if now.day in [30, 31, 1]:
        return True
    return False


def return_ttl(name: str) -> int:
    cache_ttl_short: int = int(60 * 60 * 0.5)  # 30 minutes
    cache_ttl_medium: int = int(60 * 60 * 1)  # 1 hour
    cache_ttl_long: int = int(60 * 60 * 1.5)  # 1 hour 30 minutes

    if name == "long":
        return cache_ttl_long
    elif name == "short":
        return cache_ttl_short
    elif name == "medium":
        return cache_ttl_medium
    return cache_ttl_short


# TODO Refactor the entire codebase to use this function to obtain todays date
def today() -> date:
    return datetime.datetime.now().date()


def time_now() -> time_class:
    return datetime.datetime.now().time()


def datetime_now() -> datetime:
    return datetime.datetime.now()


def date_days_ago(days: int) -> date:
    days_ago = datetime.datetime.now() - datetime.timedelta(days=days)
    return days_ago.date()


def task_counter(timer_limit: int = 10000) -> any:
    ***REMOVED***
        if request is to create task then
            with connection read task count
            add one to task count
    ***REMOVED***
    y = 0
    while y < timer_limit:
        yield y
        y += 1


counter = task_counter()


def get_counter() -> int:
    return next(counter)


def get_payment_methods() -> typing.List[str]:
    return ['eft', 'paypal']


def get_plan_scheduled_terms() -> typing.List[str]:
    ***REMOVED***
        fetches payment plan schedules from config_instance
    :return: LIST payment_plan_schedules
    ***REMOVED***
    return config_instance.PAYMENT_PLANS_SCHEDULES


def get_scheduled_term_days() -> typing.List[int]:
    ***REMOVED***
        returns the days the transactions can be made once scheduled term has been reached for payment
    :return: list of integers representing days transactions can be made
    ***REMOVED***
    return config_instance.PAYMENT_PLANS_PAYMENT_DAYS


def can_cache() -> any:
    ***REMOVED***NOTE: de activates the cache in case we are running on development server or debug is enabled***REMOVED***
    return is_development() or not config_instance.DEBUG


def clear_cache(app, cache: Cache) -> bool:
    with app.context():
        cache.clear()
        return True


if __name__ == '__main__':
    # today = datetime.datetime.now()
    # last_30_days_timestamp = timestamp() - get_days(days=30)
    # print(date.fromtimestamp(float(last_30_days_timestamp/1000)))
    # print(last_30_days_timestamp)
    # expire_after = datetime.datetime.now() - datetime.timedelta(days=30)
    # print(expire_after.date())
    pass


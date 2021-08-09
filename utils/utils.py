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

# NOTE set of characters to use when generating Unique ID
char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits

# NOTE input character set
input_character_set = string.printable


# Creates an ID for use as a unique ID
def create_id(size: int = 64, chars: str = char_set) -> str: return ''.join(random.choice(chars) for _ in range(size))


def is_valid_chars(value: str, chars: str = input_character_set) -> bool:
    ***REMOVED***
        checks if all characters are valid
    :param value: value to check
    :param chars: valid characters
    :return: bool indicating if characters are valid or not
    ***REMOVED***
    for c in value:
        if c not in chars:
            return False
    return True


# NOTE : Cannot use current_app - is_development is opposite of IS_PRODUCTION
def is_development() -> bool: return not config_instance.IS_PRODUCTION


# NOTE this environment variable is only found on Heroku - will return True of is_heroku is present
def is_heroku() -> bool: return bool(os.environ.get("IS_HEROKU"))


# Returns he timestamp in milliseconds
def timestamp() -> int: return int(float(time.time()) * 1000)


# Returns the number of days in milliseconds
def get_days(days: int) -> int: return int(days * 24 * 60 * 60 * 1000)


# Returns the difference in milliseconds between two timestamps
def timestamp_difference(stamp1: int, stamp2: int) -> int: return int(stamp1 - stamp2)


# Turns a string representation of a date into python date object
def date_string_to_date(date_str: str) -> date:
    ***REMOVED***
    :param date_str: string representation of date
    :return: returns a python date object
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
    ***REMOVED***
        NOTE: True if the present date can be considered end of month or near end of month
        :return: True
    ***REMOVED***
    now: date = datetime.datetime.now().date()
    if now.day in [30, 31, 1]:
        return True
    return False


# Used to control cache ttl
def return_ttl(name: str) -> int:
    ***REMOVED***
       NOTE:  returns ttl for cache depending on long, short, and medium
    :param name:
    :return:
    ***REMOVED***
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


# returns today's date
def today() -> date: return datetime.datetime.now().date()


# Returns the present time
def time_now() -> time_class: return datetime.datetime.now().time()


# NOTE: Returns the present datetime
def datetime_now() -> datetime: return datetime.datetime.now()


# NOTE: returns a date indicated by days in the past
def date_days_ago(days: int) -> date: return (datetime.datetime.now() - datetime.timedelta(days=days)).date()


# NOTE: returns the present supported payment method
def get_payment_methods() -> typing.List[str]: return ['eft', 'paypal']


# NOTE: fetches payment plan schedules from config_instance
def get_plan_scheduled_terms() -> typing.List[str]: return config_instance.PAYMENT_PLANS_SCHEDULES


# NOTE: returns the days the transactions can be made once scheduled term has been reached for payment
def get_scheduled_term_days() -> typing.List[int]: return config_instance.PAYMENT_PLANS_PAYMENT_DAYS


# NOTE: Returns True if cache can be used or is supported,  in-case of debug or development the cache
def can_cache() -> bool: return is_development() or not config_instance.DEBUG


def clear_cache(app, cache: Cache) -> bool:
    with app.context():
        cache.clear()
        return True


# NOTE: Task counter generator
def task_counter(timer_limit: int = 1000000) -> any:
    ***REMOVED***
        **task_counter**
        if request is to create task then
            with connection read task count
            add one to task count

    :param timer_limit:
    :return:
    ***REMOVED***
    y = 0
    while y < timer_limit:
        yield y
        y += 1


counter = task_counter()


# NOTE: get counter - to use the generator
def get_counter() -> int: return next(counter)


if __name__ == '__main__':
    # today = datetime.datetime.now()
    # last_30_days_timestamp = timestamp() - get_days(days=30)
    # print(date.fromtimestamp(float(last_30_days_timestamp/1000)))
    # print(last_30_days_timestamp)
    # expire_after = datetime.datetime.now() - datetime.timedelta(days=30)
    # print(expire_after.date())
    pass

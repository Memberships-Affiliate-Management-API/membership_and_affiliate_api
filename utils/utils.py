***REMOVED***
    **Module - Common Application Utilities**

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
from flask_caching import Cache
from config import config_instance


# NOTE set of characters to use when generating Unique ID
_char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits

# NOTE input character set
_input_character_set = string.printable


# Creates an ID for use as a unique ID
def create_id(size: int = 64, chars: str = _char_set) -> str:
    return ''.join(random.choice(chars) for _ in range(size))


def is_valid_chars(value: str, chars: str = _input_character_set) -> bool:
    ***REMOVED***
        **is_valid_chars**
            checks if all characters are valid

    :param value: value to check
    :param chars: valid characters
    :return: bool indicating if characters are valid or not
    ***REMOVED***
    for c in value:
        if c not in chars:
            return False
    return True



def is_development() -> bool:
    ***REMOVED***
        NOTE : Cannot use current_app - is_development is opposite of IS_PRODUCTION
    ***REMOVED***
    return not config_instance.IS_PRODUCTION



def is_heroku() -> bool:
    ***REMOVED***
        NOTE this environment variable is only found on Heroku - 
        will return True of is_heroku is present
    ***REMOVED***
    return bool(os.environ.get("IS_HEROKU"))


def timestamp() -> int:
    ***REMOVED***
        Returns he timestamp in milliseconds
    ***REMOVED***
    return int(float(time.time()) * 1000)



def get_days(days: int) -> int:
    ***REMOVED***
        Returns the number of days in milliseconds
    ***REMOVED***
    return int(days * 24 * 60 * 60 * 1000)


def timestamp_difference(stamp1: int, stamp2: int) -> int:
    ***REMOVED***
        Returns the difference in milliseconds between two timestamps
    ***REMOVED***
    return int(stamp1 - stamp2) if stamp1 > stamp2 else int(stamp2 - stamp1)


def date_string_to_date(date_str: str) -> date:
    ***REMOVED***
        Turns a string representation of a date into python date object
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


def end_of_month() -> bool:
    ***REMOVED***
        NOTE: True if the present date can be considered end of month or near end of month
    ***REMOVED***
    return today().day in [30, 31, 1]


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


def today() -> date:
    ***REMOVED***
        NOTE: returns todays date
    ***REMOVED***
    return datetime.datetime.now().date()



def time_now() -> time_class:
    ***REMOVED***
        NOTE: Returns the present time
    ***REMOVED***
    return datetime.datetime.now().time()


def datetime_now() -> datetime:
    ***REMOVED***
        NOTE: Returns the present datetime
    ***REMOVED***
    return datetime.datetime.now()


def date_days_ago(days: int) -> date:
    ***REMOVED***
        NOTE: returns a date indicated by days in the past
    ***REMOVED***
    return (datetime.datetime.now() - datetime.timedelta(days=days)).date()



def get_payment_methods() -> typing.List[str]: 
    ***REMOVED***
        NOTE: returns the present supported payment method
    ***REMOVED***
    return ['eft', 'paypal']



def get_plan_scheduled_terms() -> typing.List[str]: 
    ***REMOVED***
        NOTE: fetches payment plan schedules from config_instance
    ***REMOVED***
    return config_instance.PAYMENT_PLANS_SCHEDULES



def get_scheduled_term_days() -> typing.List[int]:
    ***REMOVED***
        NOTE: returns the days the transactions can be made once scheduled term 
        has been reached for payment
    ***REMOVED***
    return config_instance.PAYMENT_PLANS_PAYMENT_DAYS



def can_cache() -> bool: 
    ***REMOVED***
        NOTE: Returns True if cache can be used or is supported,  in-case of debug 
        or development the cache
    ***REMOVED***
    return is_development() or not config_instance.DEBUG


def clear_cache(app, cache: Cache) -> bool:
    ***REMOVED***
        totally clears application cache upon restart
    ***REMOVED***
    with app.app_context():
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



def get_counter() -> int: 
    ***REMOVED***
        # NOTE: get counter - to use the generator
    ***REMOVED***
    return next(counter)


if __name__ == '__main__':
    # today = datetime.datetime.now()
    # last_30_days_timestamp = timestamp() - get_days(days=30)
    # print(date.fromtimestamp(float(last_30_days_timestamp/1000)))
    # print(last_30_days_timestamp)
    # expire_after = datetime.datetime.now() - datetime.timedelta(days=30)
    # print(expire_after.date())
    pass

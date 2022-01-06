"""
    **Module - Common Application Utilities**
        utilities for commonly performed tasks
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import os
import datetime
import random
import string
import time
from functools import wraps
from typing import List, Optional, Union, Callable
from datetime import date
from datetime import time as time_class
from config import config_instance

# NOTE set of characters to use when generating Unique ID
_char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits

# NOTE input character set
_input_character_set = string.printable


def _retry(func: Callable, exception: Exception = Exception, _max_retries: int = 3, delay: int = 0, backoff: int = 1):
    # noinspection PyBroadException
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        tries = 0
        while tries < _max_retries:
            try:
                return func(*args, **kwargs)
            except exception as e:
                _delay = delay * backoff ** tries
                time.sleep(_delay)
                tries += 1
        return func(*args, **kwargs)

    return wrapped_function


# Creates an ID for use as a unique ID
def create_id(size: int = 64, chars: str = _char_set) -> str:
    """
        **create_id**
            create a random unique id for use as indexes in Database Models

    :param size: size of string - leave as default if you can
    :param chars: character set to create Unique identifier from leave as default
    :return: uuid -> randomly generated id
    """
    return ''.join(random.choice(chars) for _ in range(size))


def is_valid_chars(value: str, chars: str = _input_character_set) -> bool:
    """
        **is_valid_chars**
            checks if all characters are valid

    :param value: value to check
    :param chars: valid characters
    :return: bool indicating if characters are valid or not
    """
    return not bool([invalid_char for invalid_char in value if invalid_char not in chars])


def is_development() -> bool:
    """
        **is_development**
            is_development is opposite of IS_PRODUCTION
        :return bool -> True if running on development server
    """
    return not config_instance.IS_PRODUCTION


def is_heroku() -> bool:
    """
        **is_heroku**
            NOTE this environment variable is only found on Heroku -
            will return True of is_heroku is present
        :return bool -> True if the application is running on heroku
    """
    return bool(os.environ.get("IS_HEROKU"))


def timestamp() -> int:
    """
        **timestamp**
            Returns the time as timestamp in milliseconds

        :return present time in milliseconds
    """
    return int(float(time.time()) * 1000)


def get_days_in_milliseconds(days: int) -> int:
    """
        **get_days**
            Returns the number of days in milliseconds
    """
    return int(days * 24 * 60 * 60 * 1000)


def timestamp_difference(stamp1: int, stamp2: int) -> int:
    """
        **timestamp_difference**
            Returns the absolute difference in milliseconds between two timestamps
        :param stamp1 -> integer timestamp 1
        :param stamp2 -> integer timestamp 2
        :return the difference between the two timestamps
    """
    from math import fabs
    return int(fabs(stamp1 - stamp2))


def date_string_to_date(date_str: str) -> date:
    """
        **date_string_to_date**
            Turns a string representation of a date into python date object representing the date
            eval(timestamp_difference.__doc__)
    :param date_str: string representation of date
    :return: returns a python date object
    """
    if isinstance(date_str, date):
        return date_str

    if not isinstance(date_str, str):
        raise ValueError('Date format invalid')

    if not ("/" in date_str or "-" in date_str):
        raise ValueError('Date format invalid')

    date_list: List[str] = date_str.split("/") if "/" in date_str else date_str.split("-")
    if len(date_list) != 3:
        raise ValueError("Date Format invalid")

    year: int = int(date_list[0])
    month: int = int(date_list[1])
    day: int = int(date_list[2])

    if 0 < month > 12:
        raise ValueError("Date Format Invalid")
    if 0 < day > 31:
        raise ValueError("Date Format invalid")
    if year < 1990:
        # Not interested in anything that old
        raise ValueError("Date Format invalid")

    return date(year=year, month=month, day=day)


def end_of_month() -> bool:
    """
        **end_of_month**
            True if the present date can be considered end of month or near end of month
        :return boolean -> True if end of month
    """
    return today().day in [30, 31, 1]


# Used to control cache ttl
def return_ttl(name: str) -> int:
    """
        **return_ttl**
            returns ttl for cache depending on long, short, and medium

    :param name: string -> period = short, medium, long
    :return: int -> time to live
    """
    cache_ttl_short: int = 1800  # (60*60 * 0.5) 30 minutes
    cache_ttl_medium: int = 3600  # (60 * 60) 1 hour
    cache_ttl_long: int = 5400  # (60 * 60 * 1.5) 1 hour 30 minutes

    if name == "long":
        return cache_ttl_long
    elif name == "short":
        return cache_ttl_short
    elif name == "medium":
        return cache_ttl_medium
    return cache_ttl_short


def today() -> date:
    """
    **today**
        returns today's date

    :return present date
    """
    return datetime.datetime.now().date()


def time_now() -> time_class:
    """
        **time_now**
            NOTE: Returns the present time
        :return present time
    """
    return datetime.datetime.now().time()


def datetime_now() -> datetime:
    """
        **datetime_now**
            NOTE: Returns the present datetime
        :return: present datetime
    """
    return datetime.datetime.now()


def date_days_ago(days: int) -> date:
    """
        **date_days_ago**
            NOTE: returns a date indicated by days in the past

        :param days -> int number of days to go backwards
        :return previous date counted by days before
    """
    return (datetime.datetime.now() - datetime.timedelta(days=days)).date()


def get_payment_methods() -> List[str]:
    """
        **get_payment_methods**
            NOTE: returns the present supported payment method
        :return list of usable payment methods
    """
    return ['eft', 'paypal']


def get_plan_scheduled_terms() -> List[str]:
    """
        **get_plan_scheduled_terms**
            NOTE: fetches payment plan schedules from config_instance

        :return list -> list of usable scheduled terms e.g monthly ...
    """
    # TODO - ensure scheduled terms matches those in paypal
    return config_instance.PAYMENT_PLANS_SCHEDULES


def get_scheduled_term_days() -> List[int]:
    """
        **get_scheduled_term_days**
            NOTE: returns the days the transactions can be made once scheduled term
            has been reached for payment

        :return list -> list of usable payment plan days
    """
    return config_instance.PAYMENT_PLANS_PAYMENT_DAYS


def can_cache() -> bool:
    """
        **can_cache**
            this function evaluates if the conditions to cache routes is ok
            basically it wont allow cache when in development and also when DEBUG is active

        NOTE: Returns True if cache can be used or is supported,  in-case of debug 
        or development the cache

    """
    return is_development() or config_instance.DEBUG


# NOTE: Task counter generator
def task_counter(timer_limit: int = 1000000) -> any:
    """
        **task_counter**
            if request is to create task then
            with connection read task count
            add one to task count

    :param timer_limit:
    :return:
    """
    return (y for y in range(timer_limit))


# Counter Generator
counter = task_counter()


def get_counter() -> int:
    """
    **get_counter**
        # NOTE: get counter - to use the generator
    : return -> integer from counter generator
    """
    return next(counter)


if __name__ == '__main__':
    pass

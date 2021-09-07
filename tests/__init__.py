import requests
from flask import current_app
from config import config_instance
from main import create_app
from random import choice, choices, randint
from string import digits


def test_app():
    if not current_app:
        app = create_app(config_class=config_instance)
        app.app_context().push()
    else:
        app = current_app
    app.testing = True
    return app


def random_int_positive():
    return int(choice(choices(population=digits[1:9], k=10))) * randint(1, 100)


def random_int_negative():
    return 0 - int(choice(choices(population=digits[1:9], k=10))) * randint(1, 100)


def random_float_positive():
    return float(int(choice(choices(population=digits[1:9], k=10)))) * randint(1, 100)


def random_float_negative():
    return float(0 - int(choice(choices(population=digits[1:9], k=10)))) * randint(1, 100)


def is_internet_on() -> bool:
    """
    **is_internet_on**
        checks if internet is on if this is the case run alternate tests
    :return:
    """
    try:
        _url: str = 'https://google.com/'
        requests.get(url=_url, timeout=5)
        return True
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False


def get_test_domain() -> str:
    return 'https://memberships-affiliates-man-api.herokuapp.com/' if is_internet_on() else 'http://127.0.0.1:8081/'

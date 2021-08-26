from flask import current_app
from config import config_instance
from main import create_app
from random import choice
from string import digits


def test_app():
    if not current_app:
        app = create_app(config_class=config_instance)
        app.app_context().push()
    else:
        app = current_app
    app.testing = True
    return app


def int_positive():
    num = 0
    for _ in range(3):
        num += int(choice(digits))
    return num


def int_negative():
    num = 0
    for _ in range(3):
        num -= int(choice(digits))
    return num


def float_positive():
    num = 0
    for _ in range(3):
        num += int(choice(digits))
    return float(num)


def float_negative():
    num = 0
    for _ in range(3):
        num -= int(choice(digits))
    return float(num)

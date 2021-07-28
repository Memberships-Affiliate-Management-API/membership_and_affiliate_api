***REMOVED***
    class used to set ndb database properties
***REMOVED***
import typing
from datetime import datetime, date
from utils.utils import get_payment_methods


class ClassSetters:
    def __init__(self):
        pass

    @staticmethod
    def set_id(prop, value: typing.Union[str, None]) -> str:
        if (value is None) or (value == ""):
            raise ValueError(" {} cannot be Null".format(str(prop)))

        if not(isinstance(value, str)):
            raise ValueError(" {} can only be a string".format(str(prop)))
        return value

    @staticmethod
    def set_paypal(prop, value: typing.Union[str, None]) -> str:
        if (value is None) or (value == ""):
            raise ValueError(" {} cannot be Null".format(str(prop)))

        if not(isinstance(value, str)):
            raise ValueError(" {} can only be a string".format(str(prop)))
        return value.strip().lower()

    @staticmethod
    def set_transaction_types(prop, value: typing.Union[str, None]) -> str:
        transaction_types = ['withdrawal', 'deposit']
        if value not in transaction_types:
            raise ValueError(" {} invalid transaction type".format(str(prop)))
        return value

    @staticmethod
    def set_datetime(prop, value: datetime) -> datetime:
        if not(isinstance(value, datetime)):
            raise ValueError("{} invalid argument".format(str(prop)))
        return value

    @staticmethod
    def set_bool(prop, value: typing.Union[bool, None]) -> bool:
        if not(isinstance(value, bool)):
            raise ValueError("{} invalid argument".format(str(prop)))
        return value

    @staticmethod
    def set_status(prop, value: typing.Union[str, None]) -> str:
        if (value is None) or (value == ""):
            raise ValueError("{} cannot be Null".format(str(prop)))
        if not (isinstance(value, str)):
            raise TypeError("{} invalid status".format(str(prop)))
        value = value.strip().lower()
        if value not in ['paid', 'unpaid']:
            raise TypeError("{} invalid status".format(str(prop)))
        return value.strip().lower()

    @staticmethod
    def set_string(prop, value: typing.Union[str, None]) -> str:
        if (value is None) or (value == ""):
            raise ValueError("{} cannot be Null".format(str(prop)))
        if not (isinstance(value, str)):
            raise TypeError("{} can only be a string ".format(str(prop)))
        return value.strip().lower()

    @staticmethod
    def set_schedule_term(prop, value: typing.Union[str, None]) -> str:
        if (value is None) or (value == ""):
            raise ValueError("{} cannot be Null".format(str(prop)))
        if not (isinstance(value, str)):
            raise TypeError("{} can only be a string ".format(str(prop)))
        value = value.strip().lower()
        # TODO - Rewrite this or create a translator for paypal plans payment schedule
        if value in ["monthly", "quarterly", "annually"]:
            return value
        raise ValueError("Invalid scheduled term")

    @staticmethod
    def set_schedule_day(prop, value: typing.Union[int, None]) -> int:
        if not (isinstance(value, int)):
            raise TypeError('{} can only be an integer'.format(str(prop)))
        if value not in [1, 2, 3, 4, 5]:
            raise ValueError('{} can only be between 1 -> 5 of every month'.format(str(prop)))
        return value

    @staticmethod
    def set_number(prop, value: typing.Union[int, None]) -> int:
        if not (isinstance(value, int)):
            raise TypeError('{} can only be an integer'.format(str(prop)))

        if value < 0:
            raise TypeError("{} no negative numbers".format(str(prop)))

        return value

    @staticmethod
    def set_date(prop, value: date) -> date:
        if not (isinstance(value, date)):
            raise TypeError("{}, Invalid Type".format(str(prop)))
        return value

    @staticmethod
    def set_payment_method(prop, value: typing.Union[str, None]) -> str:
        if not (isinstance(value, str)):
            raise TypeError("{}, Invalid Type".format(str(prop)))
        if value not in get_payment_methods():
            raise ValueError("{}, Invalid Payment Method".format(str(prop)))
        return value

    @staticmethod
    def set_percent(prop, value: typing.Union[int, None]) -> int:
        if not isinstance(value, int):
            raise TypeError("{}, Invalid Type".format(str(prop)))
        if 0 < value > 100:
            raise ValueError("{}, Invalid Percentage".format(str(prop)))
        return value

    @staticmethod
    def set_currency(prop, value: typing.Union[str, None]) -> str:
        from config.currencies import currency_symbols
        if not (isinstance(value, str)):
            raise TypeError("{} can only be string".format(prop))
        if value not in currency_symbols():
            raise ValueError("{} not a valid currency symbol".format(str(prop)))
        return value

    @staticmethod
    def set_email(prop, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            TODO validate email here
        ***REMOVED***
        import re
        # TODO fix email regex match
        regex = '\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b'
        # print(value)
        # if re.search(regex, value) is not None:
        #     return value
        if not isinstance(value, str):
            raise TypeError("invalid argument for email")

        return value
        # raise ValueError("{} invalid email address".format(str(prop)))

    # noinspection PyUnusedLocal
    @staticmethod
    def set_cell(prop, value: typing.Union[str, None]) -> str:
        if not isinstance(value, str):
            raise TypeError("invalid argument for cell")
        # TODO check cell number with regex

        return value

    # noinspection PyUnusedLocal
    @staticmethod
    def set_password(prop, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            TODO validate password here, using regex
        ***REMOVED***
        from werkzeug.security import generate_password_hash
        if not isinstance(value, str):
            raise TypeError("invalid argument for password")

        if len(value) < 8:
            raise ValueError("password length must be 8 characters and higher")

        return generate_password_hash(value, method="pbkdf2:sha256", salt_length=8)

    @staticmethod
    def set_value_amount(prop, value: typing.Union[int, None]) -> int:
        if not (isinstance(value, int)):
            raise TypeError("{} can only be integer".format(str(prop)))
        return value

    @staticmethod
    def set_domain(prop, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            :return:
        ***REMOVED***
        import requests
        if not (isinstance(value, str)):
            raise TypeError("domain name can only be a string")
        response = requests.get(url=value)
        if 400 < response.status_code >= 200:
            return value
        raise ValueError("invalid domain name")


setters: ClassSetters = ClassSetters()

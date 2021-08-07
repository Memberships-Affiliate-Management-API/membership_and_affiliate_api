***REMOVED***
    class used to set ndb database properties
***REMOVED***
import typing
from datetime import datetime, date
from utils.utils import get_payment_methods
import re
import socket

class Util:
    def __init__(self):
        pass

    @staticmethod
    def regex_check_email(email: str) -> bool:
        regex_pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        pattern = re.compile(regex_pattern)
        return True if re.match(pattern, email) else False

    @staticmethod
    def password_complexity(password: str) -> bool:
        ***REMOVED***
            password contains upper-case and lower-case characters, numbers and at least 8 characters in length
        :param password:
        :return:
        ***REMOVED***
        regex_pattern = r'[A-Za-z0-9@#$%^&+=]{8,}'
        pattern = re.compile(regex_pattern)
        return True if re.fullmatch(pattern, password) else False

    @staticmethod
    def regex_check_domain(domain: str) -> bool:
        ***REMOVED***

        :param domain:
        :return:
        ***REMOVED***
        regex_pattern = r'^[a-z0-9]([a-z0-9-]+\.){1,}[a-z0-9]+\Z'
        pattern = re.compile(regex_pattern)
        return True if re.fullmatch(pattern, domain) else False

    @staticmethod
    def resolve_domain_name(domain: str) -> bool:
        ***REMOVED***
            checks if domain resolves to an IP address
        :param domain:
        :return:
        ***REMOVED***
        return True if socket.gethostbyname(domain) else False


class ClassSetters(Util):

    def __init__(self):
        super(ClassSetters, self).__init__()

    @staticmethod
    def set_id(prop, value: typing.Union[str, None]) -> str:

        if not (isinstance(value, str)):
            raise ValueError(" {} can only be a string".format(str(prop)))

        if not bool(value.strip()):
            raise ValueError(" {} cannot be Null".format(str(prop)))

        return value.strip()

    @staticmethod
    def set_coupon_code(prop, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            TODO: coupon code length - find a way to standardize this length and not make it a magic number
        :param prop:
        :param value:
        :return:
        ***REMOVED***
        if not (isinstance(value, str)):
            raise ValueError(" {} can only be a string".format(str(prop)))

        if value.strip() > 12:
            raise ValueError(" {} cannot be Null".format(str(prop)))

        return value.strip()

    @staticmethod
    def set_paypal(prop, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            checks if an paypal is email
        :param prop:
        :param value:
        :return:
        ***REMOVED***

        if not (isinstance(value, str)):
            raise ValueError(" {} can only be a string".format(str(prop)))

        if not bool(value.strip()):
            raise ValueError(" {} cannot be Null".format(str(prop)))

        utils_instance: Util = Util()

        if utils_instance.regex_check_email(email=value.strip().lower()):
            return value.strip().lower()
        raise ValueError(" {} is not a valid email address".format(value))

    @staticmethod
    def set_transaction_types(prop, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            set a transaction type
        :param prop:
        :param value:
        :return:
        ***REMOVED***
        if not (isinstance(value, str)):
            raise ValueError(" {} can only be a string".format(str(prop)))

        transaction_types = ['withdrawal', 'deposit']
        if value.strip().lower() not in transaction_types:
            raise ValueError(" {} invalid transaction type".format(str(prop)))

        return value.strip().lower()

    @staticmethod
    def set_datetime(prop, value: datetime) -> datetime:
        if not (isinstance(value, datetime)):
            raise ValueError("{} invalid argument".format(str(prop)))
        return value

    @staticmethod
    def set_bool(prop, value: typing.Union[bool, None]) -> bool:
        if not (isinstance(value, bool)):
            raise ValueError("{} invalid argument".format(str(prop)))
        return value

    @staticmethod
    def set_status(prop, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            only two valid statuses paid and unpaid check if input is valid and set
        :param prop:
        :param value:
        :return:
        ***REMOVED***

        if not (isinstance(value, str)):
            raise TypeError("{} invalid status".format(str(prop)))
        temp = value.strip().lower()
        if not bool(temp):
            raise ValueError("{} cannot be Null".format(str(prop)))

        if temp not in ['paid', 'unpaid']:
            raise TypeError("{} invalid status".format(str(prop)))

        return temp

    @staticmethod
    def set_string(prop, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            check if its string and set
        :param prop:
        :param value:
        :return:
        ***REMOVED***
        if not (isinstance(value, str)):
            raise TypeError("{} can only be a string ".format(str(prop)))

        if not bool(value.strip()):
            raise ValueError("{} cannot be Null".format(str(prop)))

        return value.strip().lower()

    @staticmethod
    def set_schedule_term(prop, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            set scheduled term -
        :param prop:
        :param value:
        :return:
        ***REMOVED***

        if not (isinstance(value, str)):
            raise TypeError("{} can only be a string ".format(str(prop)))

        if not bool(value.strip()):
            raise ValueError("{} cannot be Null".format(str(prop)))
        temp = value.strip().lower()
        # TODO - Rewrite this or create a translator for paypal plans payment schedule
        if temp in ["monthly", "quarterly", "annually"]:
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

        if value.lower().strip() not in get_payment_methods():
            raise ValueError("{}, Invalid Payment Method".format(str(prop)))

        return value.lower().strip()

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

    # noinspection PyUnusedLocal,DuplicatedCode
    @staticmethod
    def set_email(prop, value: typing.Union[str, None]) -> str:
        ***REMOVED***
           used for the following
            If email is valid return email address else raise an error
            :param value: email address
            :param prop: email property
        ***REMOVED***

        if not (isinstance(value, str)):
            raise ValueError(" {} can only be a string".format(str(prop)))

        if not bool(value.strip()):
            raise ValueError(" {} cannot be Null".format(str(prop)))

        utils_instance: Util = Util()

        if utils_instance.regex_check_email(email=value.strip().lower()):
            return value.strip().lower()
        raise ValueError(" {} is not a valid email address".format(value))

    # noinspection PyUnusedLocal
    @staticmethod
    def set_cell(prop, value: typing.Union[str, None]) -> str:
        if not isinstance(value, str):
            raise TypeError("invalid argument for cell")
        # TODO CHECK CELL WITH REGEX

        return value

    # noinspection PyUnusedLocal
    @staticmethod
    def set_password(prop, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            validate the correctness of the password and its complexity if  accurate
            then return the hash of the password to be stored on the database
            :param: value: password in plain-text
            :param : prop: the password property being set
            :return: password in hash format
        ***REMOVED***
        from werkzeug.security import generate_password_hash
        if not isinstance(value, str):
            raise TypeError("invalid argument for password")

        utils_instance: Util = Util()
        if utils_instance.password_complexity(password=value.strip()):
            return generate_password_hash(value, method="pbkdf2:sha256", salt_length=8)
        message: str = '''password must be at least 8 characters in length, and contain lower-case and upper-case letters, 
        numbers and at least a special character'''
        raise ValueError(message)

    @staticmethod
    def set_value_amount(prop, value: typing.Union[int, None]) -> int:
        ***REMOVED***
            amount in integer used to validate amounts in cash on AmountMixin
        :param prop:
        :param value: amount in integer
        :return: integer representing money in cents of whatever currency is being represented
        ***REMOVED***
        if not (isinstance(value, int)):
            raise TypeError("{} can only be integer".format(str(prop)))
        return value

    @staticmethod
    def set_domain(prop, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            check the domain name regex if it passes resolve
            the domain name if it passes then return domain name
            :return:
        ***REMOVED***

        if not (isinstance(value, str)):
            raise TypeError("{} can only be a string".format(str(prop)))

        utils_instance: Util = Util()
        domain = value.strip()
        regex_passes = utils_instance.regex_check_domain(domain=domain)
        domain_valid = utils_instance.resolve_domain_name(domain=domain)
        if regex_passes and domain_valid:
            return domain
        raise ValueError("Invalid domain name")


setters: ClassSetters = ClassSetters()

"""
    module used to set values into ndb database properties,
    this module also has an added function of validating any such values to insure data integrity.
    the module will also trigger events when some database properties are being set or reset.
    allowing certain actions to be triggered if its necessary to do so.
"""

__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from typing import List, Optional, Union

import requests
from flask import escape
from datetime import datetime, date
from google.cloud import ndb
from phonenumbers import NumberParseException
from utils.utils import get_payment_methods, get_plan_scheduled_terms, get_scheduled_term_days
import re
import socket
import phonenumbers


class Events:
    """
        **Class Events**
           asynchronously triggers events when certain values are changed on the database
           events server must be instantiated or a ready made solution added

           **Suggestion:** or could use a memory based data-structure for now to control
           events, and then create a method which will continuously fetch and execute
           the events asynchronously.
    """

    def __init__(self):
        pass


class Util:
    """
        **Class Util**
            ndb property validators utilities, constants and helpers
    """

    def __init__(self):
        # maximum length for coupon codes
        self._max_coupon_code_len: int = 12
        # maximum len for _id
        self._max_id_len: int = 64
        self._payment_statuses: List[str] = ['paid', 'unpaid']
        self._transaction_types: List[str] = [
            'withdrawal', 'deposit', 'refund']

    @staticmethod
    def return_payment_status_list() -> List[str]:
        """
        **return this from config**
        :return:
        """
        return ['paid', 'unpaid']

    @staticmethod
    def return_transaction_types() -> List[str]:
        return ['withdrawal', 'deposit', 'refund']

    @staticmethod
    def _tickets_user_types() -> List[str]:
        return ['support', 'client']

    @staticmethod
    def return_property_name(prop: ndb.Property) -> str:
        """
            **return_property_name**
                Returns the name of the ndb property

            :param prop: -> ndb.Property
            :return str: -> name of class
        """
        return prop._code_name

    @staticmethod
    def regex_check_email(email: str) -> bool:
        """
            **regex_check_email**
                checking if email is valid with regex_pattern

        :param email: email address being checked
        :return: bool True if Valid
        """

        regex_pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        pattern = re.compile(regex_pattern)
        return bool(re.fullmatch(pattern, email))

    @staticmethod
    def password_complexity(password: str) -> bool:
        """
            **password_complexity**
                1. enforces password complexity
                2. password contains upper-case and lower-case characters,
                   numbers and at least 8 characters in length

        :param password: -> text format of the password to be checked
        :return: bool -> True if password is complex enough
        """
        # NOTE: password_complexity checks allows Spaces
        regex_pattern = r'[A-Za-z0-9@#$%^& +=]{8,}'
        pattern = re.compile(regex_pattern)
        return bool(re.fullmatch(pattern, password))

    @staticmethod
    def regex_check_domain(domain: str) -> bool:
        """
            **regex_check_domain**
                1. checks a domain name for validity with regex pattern
                   r'^[a-z0-9]([a-z0-9-]+\.){1,}[a-z0-9]+\Z'
                2. return True if pattern matches

        :param domain: str -> domain name to check
        :return: bool: True -> if pattern matches
        """
        to_check: str = domain.replace(
            'https://', '') if domain.startswith('https://') else domain
        # noinspection HttpUrlsUsage
        to_check: str = to_check.replace(
            'http://', '') if to_check.startswith('http://') else to_check
        to_check: str = to_check.replace(
            '/', '') if to_check.endswith('/') else to_check
        to_check: str = to_check.split(
            sep='/')[0] if '/' in to_check else to_check

        # to_check = 'google.com'

        regex_pattern = r'^[a-z0-9]([a-z0-9-]+\.){1,}[a-z0-9]+\Z'
        new_pattern = "\b((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}\b"

        pattern = re.compile(regex_pattern)
        alt_pattern = re.compile(new_pattern)
        return not not pattern.fullmatch(to_check) or not not alt_pattern.fullmatch(new_pattern)

    @staticmethod
    def resolve_domain_name(domain: str) -> bool:
        """
            **resolve_domain_name**
                checks if domain resolves to a valid IP address e.g (102.103.100.01)

        :param domain: str -> domain name example : google.com
        :return: True if domain resolves else False
        """
        try:
            result = requests.get(domain)
            return result.ok
        except requests.RequestException:
            return False

    @staticmethod
    def format_cell_number(cell: str) -> str:
        """
            **format_cell_number**
                returns an internationally formatted cell_number

        :param cell: str -> cell number with international code
        :return: cell: str -> formatted cell number
        """
        try:
            cell_number = phonenumbers.parse(cell.strip(), None)
            return str(phonenumbers.format_number(cell_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
        except NumberParseException:
            raise ValueError(
                "Please enter cell number in an international format")

    @staticmethod
    def regex_check_cell(cell: str) -> bool:
        """
            **regex_check_cell**
                regex check cell number

        :param cell: str -> cell number in international format
        :return: bool -> true if number is valid
        """
        try:
            cell_object = phonenumbers.parse(cell, None)
            possibly_cell_number: bool = phonenumbers.is_possible_number(
                cell_object)
            valid_cell_number: bool = phonenumbers.is_valid_number(cell_object)
            return possibly_cell_number and valid_cell_number
        except NumberParseException:
            raise ValueError(
                "Please enter cell number in an international format")

    # checks if percentage is valid
    @staticmethod
    def percent_valid(percent: Union[int, float]) -> bool:
        return 0 < percent > 100


class PropertySetters(Events, Util):
    """
        **Class PropertySetters**

            Used to set and validate input to ndb properties.
            If input data is invalid the setters will raise ValueError or
            TypeError depending on the error at hand.
    """

    def __init__(self):
        super(PropertySetters, self).__init__()

    @staticmethod
    def set_id(prop: ndb.StringProperty, value: Optional[str]) -> str:
        """
            **set_id**
                sets a unique id used to differentiate between different records in database

                test if id is string and not a nullish string if that's the
                case returns the id as string to be set into the database
                class Property

        :param prop: property to set
        :param value: value as id to set
        :return: returns id as string
        """
        property_name: str = property_.return_property_name(prop=prop)
        try:
            assert isinstance(value, str)
        except AssertionError:
            message: str = f'{property_name} , can only be a string'
            raise ValueError(message)
        try:
            assert bool(value.strip())
        except AssertionError:
            raise ValueError(f"{property_name} , cannot be Null")

        return value.strip()

    @staticmethod
    def set_coupon_code(prop: ndb.StringProperty, value: Optional[str]) -> str:
        """
            **set_coupon_code**
                validates and sets coupon code for membership payments
        :param prop: coupon code property to set
        :param value: coupon code
        :return:
        """
        property_name: str = property_.return_property_name(prop=prop)
        try:
            assert isinstance(value, str)
        except AssertionError:
            raise ValueError(
                f"Must be an instance of: {property_name} , and can only be a string")
        try:
            assert len(value.strip()) == property_._max_coupon_code_len
        except AssertionError:
            message: str = f"{property_name} , must be 12 characters long"
            raise ValueError(message)

        return value.strip().lower()

    # noinspection DuplicatedCode
    @staticmethod
    def set_paypal(prop: ndb.StringProperty, value: Optional[str]) -> str:
        """
            **set_paypal**
                validate the paypal email if its really an email return the email
                to set on the paypal property

        :param prop: property to set
        :param value: paypal_address to set once validated
         :return: valid paypal_address only
        """
        property_name: str = property_.return_property_name(prop=prop)
        if not isinstance(value, str):
            message: str = f"{property_name} , can only be a string representing paypal_address"
            raise ValueError(message)

        if not bool(value.strip()):
            raise ValueError(f"{property_name} , cannot be Null")

        if property_.regex_check_email(email=value.strip().lower()):
            return value.strip().lower()
        raise ValueError("{} is not a valid email address".format(value))

    @staticmethod
    def set_transaction_types(prop: ndb.StringProperty, value: Optional[str]) -> str:
        """
            **set_transaction_types**
                validated and set transaction_types

        :param prop: property representing transaction_types
        :param value: transaction type to check
        :return: valid transaction type, return to set
        """
        property_name: str = property_.return_property_name(prop=prop)
        if not (isinstance(value, str)):
            raise ValueError(
                f"transaction_type, is an instance of : {property_name} , and can only be a string")

        # NOTE: valid transaction types "withdrawal", "deposit", "refund"
        if value.strip().lower() not in property_.return_transaction_types():
            raise ValueError(
                "{} is not a valid transaction_type".format(value))

        return value.strip().lower()

    @staticmethod
    def set_datetime(prop: ndb.DateTimeProperty, value: datetime) -> datetime:
        """
            **set_datetime**
                checks if value is a python datetime type, if not raise a type error indicating
                what i should be

        :param prop: datetime property to set if value is also a python datetime value
        :param value: python datetime
        :return: datetime
        """
        property_name: str = property_.return_property_name(prop=prop)
        if not (isinstance(value, datetime)):
            raise TypeError(
                f"datetime, is an instance of : {property_name} , must represent a valid python date")
        return value

    @staticmethod
    def set_bool(prop: ndb.BooleanProperty, value: Optional[bool]) -> bool:
        """
            **set_bool**
                checks if value is boolean if not raises a TypeError, then returns the value if valid

        :param prop: property boolean to set if value is a boolean
        :param value: boolean value
        :return: returns value as boolean
        """
        property_name: str = property_.return_property_name(prop=prop)
        if not (isinstance(value, bool)):
            raise TypeError(
                f"boolean, is an instance of : {property_name} , and can only be Either True or False")
        return value

    @staticmethod
    def set_status(prop: ndb.StringProperty, value: Optional[str]) -> str:
        """
            **set payment status**
                only two valid statuses paid and unpaid check if input is valid and set

        :param prop:
        :param value:
        :return:
        """
        property_name: str = property_.return_property_name(prop=prop)
        if value is None:
            raise TypeError(f"{property_name} , cannot be Null")

        if not (isinstance(value, str)):
            message: str = f"""status, is an instance of : {property_name} , and can only be a string 
            representing payment status"""
            raise TypeError(message)

        temp = value.strip().lower()
        if not bool(temp):
            raise ValueError(
                f"status, is an instance of : {property_name} , and cannot be Null")

        if temp not in property_.return_payment_status_list():
            message: str = f"""Status should either paid or unpaid this {value} is not a valid status"""
            raise TypeError(f"{message} invalid status")

        return temp

    @staticmethod
    def set_string(prop: ndb.StringProperty, value: Optional[str]) -> str:
        """
            **Generic String Setter**
                checks only that a string is a string

        :param prop: ndb -> property being set
        :param value: string
        :return:
        """
        property_name: str = property_.return_property_name(prop=prop)
        if value is None or value == "None" or not bool(value.strip()):
            raise TypeError(f"{property_name} , cannot be Null")

        if not (isinstance(value, str)):
            raise TypeError(f"{property_name} , can only be a string")

        return escape(value.strip().lower())

    @staticmethod
    def set_user_type(prop: ndb.StringProperty, value: Optional[str]) -> str:
        """

        :param prop:
        :param value:
        :return:
        """
        property_name: str = property_.return_property_name(prop=prop)
        if value is None or value == "None" or not bool(value.strip()):
            raise TypeError(f"{property_name} , cannot be Null")

        if not (isinstance(value, str)):
            raise TypeError(f"{property_name} , can only be a string")

        if value.strip().lower() not in property_._tickets_user_types():
            raise ValueError(f"{value}, not a valid {property_name}")

        return value.strip().lower()

    @staticmethod
    def set_schedule_term(prop: ndb.StringProperty, value: Optional[str]) -> str:
        """
        **set_schedule_term**
            set scheduled term - raises an error if scheduled term is not a string or not one of
            the valid scheduled terms

        :param prop:
        :param value:
        :return:
        """
        property_name: str = property_.return_property_name(prop=prop)
        if value is None:
            raise TypeError(f"{property_name} , cannot be Null")

        if not (isinstance(value, str)):
            raise TypeError(f"{property_name} ,  and can only be a string ")

        if not bool(value.strip()):
            raise ValueError(f"{property_name}, and cannot be Null")

        temp = value.strip().lower()
        # TODO - Rewrite this or create a translator for paypal plans payment schedule
        schedule_terms: List[str] = get_plan_scheduled_terms()
        if temp not in schedule_terms:
            raise ValueError(
                f"scheduled term, can only be one of the following values : {schedule_terms}")
        return temp

    @staticmethod
    def set_schedule_day(prop: ndb.IntegerProperty, value: Optional[int]) -> int:
        """
        **set_schedule_day**
            set scheduled day for this plan depending on this plans scheduled term the transaction will
            be made on the first transaction day coinciding with the scheduled term
        :param prop: scheduled day property
        :param value: value to set
        :return: scheduled day as integer
        """
        property_name: str = property_.return_property_name(prop=prop)
        if not (isinstance(value, int)):
            raise TypeError(f'{property_name}, can only be an integer')
        if value not in get_scheduled_term_days():
            message: str = f'''{property_name}, can only be a value between 1 -> 5 of every month'''
            raise ValueError(message)
        return value

    @staticmethod
    def set_number(prop: ndb.IntegerProperty, value: Optional[int]) -> int:
        """
        **set_number**
            set an integer number into a database property
            will check if input is really an integer and then returns the number if not
            raises TypeError if value is out of range will raise a ValueError
        :param prop: property to set
        :param value: value being set must be integer
        :return: valid integer
        """
        property_name: str = property_.return_property_name(prop=prop)
        if not (isinstance(value, int)):
            raise TypeError(f'{property_name}, can only be an integer')

        if value < 0:
            raise TypeError(f"{property_name} cannot accept negative numbers")

        return value

    @staticmethod
    def set_date(prop: ndb.DateProperty, value: date) -> date:
        """
            **set_date**
                checks to see if date is valid if yes returns the date
                throws TypeError if an invalid date has been supplied

        :param prop: property representing the date
        :param value: value to set to property
        :return: returns valid date only
        """
        property_name: str = property_.return_property_name(prop=prop)
        if not (isinstance(value, date)):
            raise TypeError(
                f"{property_name}, can only be an instance of date")
        return value

    @staticmethod
    def set_payment_method(prop: ndb.StringProperty, value: Optional[str]) -> str:
        """
            **set_payment_method**
                checks to see if payment method is valid if yes then return payment methods
                raises TypeError in-case of invalid Type and ValueError if value is not a payment method
        :param prop: property we are setting
        :param value: the value to set
        :return: returns a payment method as string
        """
        property_name: str = property_.return_property_name(prop=prop)
        if value is None:
            raise TypeError(f"{property_name} , cannot be Null")

        if not (isinstance(value, str)):
            message: str = f"""{property_name}, and can only be a string representing a valid payment method"""
            raise TypeError(message)

        if value.lower().strip() not in get_payment_methods():
            message: str = f"""this value : {value}, is not a valid payment method, supported payment 
            methods are : {get_payment_methods()}"""
            raise ValueError(message)

        return value.lower().strip()

    @staticmethod
    def set_percent(prop: ndb.IntegerProperty, value: Union[int, float]) -> int:
        """
            **set_percent**
                set_percent will check if the percentage value is an integer and then return the percentage value
                if not then it will raise ValueError or TypeError depending on the reason
        :param prop: property to set the percentage
        :param value: percentage as integer to set in property
        :return: percentage as an integer
        """
        property_name: str = property_.return_property_name(prop=prop)
        utils_instance: Util = Util()

        if not isinstance(value, int):
            message: str = f"""{property_name} and can only be an integer representing a percentage"""
            raise TypeError(message)

        if utils_instance.percent_valid(percent=value):
            message: str = f"""This value : {value}, is not a valid Percentage, percent may be a value 
            from 0 to 100"""
            raise ValueError(message)
        return value

    @staticmethod
    def set_currency(prop: ndb.StringProperty, value: Optional[str]) -> str:
        """
            **set_currency**
                checks if currency symbol is one of valid currency symbol if yes returns the symbol
                if not raise ValueError or TypeError depending on why the value is invalid
        :param prop: property where the currency symbol may be set
        :param value: value representing the currency symbol
        :return: will return currency symbol representing a string
        """
        from config.currencies import currency_util
        property_name: str = property_.return_property_name(prop=prop)
        if value is None:
            raise TypeError(f"{property_name} , cannot be Null")

        if not (isinstance(value, str)):
            message: str = f'''{property_name}, should be a string representation of a currency symbol'''
            raise TypeError(message)
        if value not in currency_util.currency_symbols():
            raise ValueError(
                f"This value : {value} is not a valid currency symbol")
        return value

    # noinspection PyUnusedLocal,DuplicatedCode
    @staticmethod
    def set_email(prop: ndb.StringProperty, value: Optional[str]) -> str:
        """
            **set_email**
                used for the following
                If email is valid return email address else raise an error
            :param value: email address
            :param prop: email property
        """
        property_name: str = property_.return_property_name(prop=prop)
        if value is None:
            raise TypeError(f"{property_name} , cannot be Null")

        if not (isinstance(value, str)):
            message: str = f"{property_name},  can only be a string representing email"
            raise ValueError(message)

        if not bool(value.strip()):
            raise ValueError(f"{property_name} cannot be Null")

        if property_.regex_check_email(email=value.strip().lower()):
            return value.strip().lower()
        raise ValueError(f" {value} is not a valid email address")

    @staticmethod
    def set_cell(prop: ndb.StringProperty, value: Optional[str]) -> str:
        """
            **set_cell**
                check if value is string , regex check the cell number
                then format the number internationally and return the formatted value
        :param prop: the property as string the cell number will be stored in
        :param value: cell number
        :return: formatted cell number as string
        """
        property_name: str = property_.return_property_name(prop=prop)
        if value is None:
            raise TypeError(f"{property_name} , cannot be Null")

        if not isinstance(value, str):
            message: str = f'''{property_name}, should be a string representing a 
            cell number in international format'''
            raise TypeError(message)
        if property_.regex_check_cell(cell=value.strip()):
            return property_.format_cell_number(cell=value)
        raise ValueError(f"This value: {value} , is not a valid cell number")

    # noinspection PyUnusedLocal
    @staticmethod
    def set_password(prop: ndb.StringProperty, value: Optional[str]) -> str:
        """
            **set_password**
                validate the correctness of the password and its complexity if  accurate
                then return the hash of the password to be stored on the database
            :param: value: password in plain-text
            :param : prop: the password property being set
            :return: password in hash format
        """
        from werkzeug.security import generate_password_hash
        property_name: str = property_.return_property_name(prop=prop)
        if value is None:
            raise TypeError(f"{property_name} , cannot be Null")

        if not isinstance(value, str):
            message: str = f'''{property_name} :  should be a string representing 
            user password'''
            raise TypeError(message)

        if property_.password_complexity(password=value.strip()):
            return generate_password_hash(value, method="pbkdf2:sha256", salt_length=8)
        message: str = '''password must be at least 8 characters in length, and contain lower-case and upper-case 
        letters, numbers and at least a special character'''
        raise ValueError(message)

    @staticmethod
    def set_value_amount(prop: ndb.IntegerProperty, value: Optional[int]) -> int:
        """
            DOCS:
                1. amount in integer used to validate amounts in cash on AmountMixin
                2. amount is in cents
        :param prop:
        :param value: amount in integer representing cents
        :return: integer representing money in cents of whatever currency is being represented
        """
        property_name: str = property_.return_property_name(prop=prop)
        if not (isinstance(value, int)):
            message: str = f'''{property_name} : can only be an Integer representing money in cents'''
            raise TypeError(message)

        # NOTE: does not allow negative values
        if value < 0:
            message: str = f"""This value : {value} , is not valid, it must be a currency amount in cents and 
            must always be a positive integer"""
            raise ValueError(message)

        return value

    @staticmethod
    def set_domain(prop: ndb.StringProperty, value: Optional[str]) -> str:
        """
            Docs:
                check the domain name regex if it passes resolve
                the domain name if it passes then return domain name
            :param: prop: ndb.StringProperty where the domain name will be stored
            :param: value: value in string format representing a domain name
            :return: str representing verified domain name
        """
        property_name: str = property_.return_property_name(prop=prop)
        if value is None:
            raise TypeError(f"{property_name} , cannot be Null")

        if not (isinstance(value, str)):
            message: str = f"""{property_name}, can only be a string, representing a valid domain name"""
            raise TypeError(message)

        domain = value.strip()

        regex_passes = property_.regex_check_domain(domain=domain)
        domain_valid = property_.resolve_domain_name(domain=domain)

        if regex_passes or domain_valid:
            return domain
        raise ValueError(
            f"This : {domain} is not a valid domain name, or the domain may not be accessible")


property_: PropertySetters = PropertySetters()
# NOTE: insures that setters is a singleton or declared only once
# del PropertySetters

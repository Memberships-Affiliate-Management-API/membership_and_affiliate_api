***REMOVED***
    module used to set values into ndb database properties,
    this module also has an added function of validating any such values to insure data integrity.
    the module will also trigger events when some database properties are being set or reset.
    allowing certain actions to be triggered if its necessary to do so.
***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import typing
from datetime import datetime, date
from google.cloud import ndb
from phonenumbers import NumberParseException
from utils.utils import get_payment_methods, get_plan_scheduled_terms, get_scheduled_term_days
import re
import socket
import phonenumbers


class Events:
    ***REMOVED***
        **Class Events**
           asynchronously triggers events when certain values are changed on the database
           events server must be instantiated or a ready made solution added

           **Suggestion:** or could use a memory based data-structure for now to control
           events, and then create a method which will continuously fetch and execute
           the events asynchronously.
    ***REMOVED***

    def __init__(self):
        pass


class Util:
    ***REMOVED***
        **Class Util**
            ndb property validators utilities, constants and helpers
    ***REMOVED***
    def __init__(self):
        # maximum length for coupon codes
        self.__max_coupon_code_len: int = 12
        # maximum len for _id
        self.__max_id_len: int = 64
        self.__payment_statuses: typing.List[str] = ['paid', 'unpaid']
        self.__transaction_types: typing.List[str] = ['withdrawal', 'deposit', 'refund']

    @staticmethod
    def return_class_name(prop: ndb.Property) -> str:
        ***REMOVED***
            Returns the name of the ndb property
        ***REMOVED***
        return prop.__class__.__name__

    @staticmethod
    def regex_check_email(email: str) -> bool:
        ***REMOVED***
            checking if email is valid with regex_pattern
        :param email: email address being checked
        :return: bool True if Valid
        ***REMOVED***

        regex_pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        pattern = re.compile(regex_pattern)
        return bool(re.fullmatch(pattern, email))

    @staticmethod
    def password_complexity(password: str) -> bool:
        ***REMOVED***
            password contains upper-case and lower-case characters, numbers and at least 8 characters in length
        :param password: -> text format of the password to be checked
        :return: bool -> True if password is complex enough
        ***REMOVED***
        regex_pattern = r'[A-Za-z0-9@#$%^&+=]{8,}'
        pattern = re.compile(regex_pattern)
        return bool(re.fullmatch(pattern, password))

    @staticmethod
    def regex_check_domain(domain: str) -> bool:
        ***REMOVED***
            **Check a Domain Name**
                checks a domain name for validity with regex pattern
                return True if pattern matches
        :param domain:
        :return:
        ***REMOVED***
        regex_pattern = r'^[a-z0-9]([a-z0-9-]+\.){1,}[a-z0-9]+\Z'
        pattern = re.compile(regex_pattern)
        return bool(re.fullmatch(pattern, domain))

    @staticmethod
    def resolve_domain_name(domain: str) -> bool:
        ***REMOVED***
            checks if domain resolves to an IP address
        :param domain:
        :return: True if domain resolves else False
        ***REMOVED***
        try:
            return bool(socket.gethostbyname_ex(domain))
        except socket.gaierror:
            return False

    @staticmethod
    def format_cell_number(cell: str) -> str:
        try:
            cell_number = phonenumbers.parse(cell.strip(), None)
            return str(phonenumbers.format_number(cell_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
        except NumberParseException:
            raise ValueError("Please enter cell number in an international format")

    @staticmethod
    def regex_check_cell(cell: str) -> bool:
        ***REMOVED***
            regex check cell number
        :param cell:
        :return:
        ***REMOVED***
        try:
            cell_object = phonenumbers.parse(cell, None)
            possibly_cell_number: bool = phonenumbers.is_possible_number(cell_object)
            valid_cell_number: bool = phonenumbers.is_valid_number(cell_object)
            if possibly_cell_number and valid_cell_number:
                return True
            return False
        except NumberParseException:
            raise ValueError("Please enter cell number in an international format")

    # checks if percentage is valid
    @staticmethod
    def percent_valid(percent: typing.Union[int, float]) -> bool: return 0 < percent > 100


class PropertySetters(Events, Util):
    ***REMOVED***
        **Class PropertySetters**

            Used to set and validate input to ndb properties.
            If input data is invalid the setters will raise ValueError or
            TypeError depending on the error at hand.
    ***REMOVED***

    def __init__(self):
        super(PropertySetters, self).__init__()

    @staticmethod
    def set_id(prop: ndb.StringProperty, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            **set_id**
                sets a unique id used to differentiate between different records in database

                test if id is string and not a nullish string if that's the
                case returns the id as string to be set into the database
                class Property

        :param prop: property to set
        :param value: value as id to set
        :return: returns id as string
        ***REMOVED***
        class_name: str = property_.return_class_name(prop=prop)
        if not (isinstance(value, str)):
            message: str = '''isinstance ID, should be an instance of : {} , and should represent an instance id'''.format(
                class_name)
            raise ValueError(message)

        if not bool(value.strip()):
            raise ValueError(
                "isinstance ID, should be an instance of : {} , and  cannot be Null".format(str(class_name)))

        return value.strip()

    @staticmethod
    def set_coupon_code(prop: ndb.StringProperty, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            **set_coupon_code**
                validates and sets coupon code for membership payments
        :param prop: coupon code property to set
        :param value: coupon code
        :return:
        ***REMOVED***
        class_name: str = property_.return_class_name(prop=prop)
        if not (isinstance(value, str)):
            raise ValueError("Coupon Code, is an instance of: {} , and can only be a string".format(str(class_name)))

        if len(value.strip()) != property_.__max_coupon_code_len:
            message: str = ***REMOVED***Coupon Code, is an instance of: {} , and must be 12 characters long
            ***REMOVED***.format(str(class_name))
            raise ValueError(message)

        return value.strip().lower()

    # noinspection DuplicatedCode
    @staticmethod
    def set_paypal(prop: ndb.StringProperty, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            **set_paypal**
                validate the paypal email if its really an email return the email
                to set on the paypal property

        :param prop: property to set
        :param value: paypal_address to set once validated
         :return: valid paypal_address only
        ***REMOVED***
        class_name: str = property_.return_class_name(prop=prop)
        if not isinstance(value, str):
            message: str = ***REMOVED***paypal address, an instance of: {} , and can only be a string representing 
            a paypal email address***REMOVED***.format(class_name)
            raise ValueError(message)

        if not bool(value.strip()):
            raise ValueError("paypal address, is an instance of : {} , and cannot be Null".format(class_name))

        if property_.regex_check_email(email=value.strip().lower()):
            return value.strip().lower()
        raise ValueError("{} is not a valid email address".format(value))

    @staticmethod
    def set_transaction_types(prop: ndb.StringProperty, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            **set_transaction_types**
                validated and set transaction_types
        :param prop: property representing transaction_types
        :param value: transaction type to check
        :return: valid transaction type, return to set
        ***REMOVED***
        class_name: str = property_.return_class_name(prop=prop)
        if not (isinstance(value, str)):
            raise ValueError("transaction_type, is an instance of : {} , and can only be a string".format(class_name))

        # NOTE: valid transaction types "withdrawal", "deposit", "refund"
        if value.strip().lower() not in property_.__transaction_types:
            raise ValueError("{} is not a valid transaction_type".format(value))

        return value.strip().lower()

    @staticmethod
    def set_datetime(prop: ndb.DateTimeProperty, value: datetime) -> datetime:
        ***REMOVED***
            **set_datetime**
                checks if value is a python datetime type, if not raise a type error indicating
                what i should be
        :param prop: datetime property to set if value is also a python datetime value
        :param value: python datetime
        :return: datetime
        ***REMOVED***
        class_name: str = property_.return_class_name(prop=prop)
        if not (isinstance(value, datetime)):
            raise TypeError("datetime, is an instance of : {} , must represent a valid python date".format(class_name))
        return value

    @staticmethod
    def set_bool(prop: ndb.BooleanProperty, value: typing.Union[bool, None]) -> bool:
        ***REMOVED***
            **set_bool**
                checks if value is boolean if not raises a TypeError, then returns the value if valid
        :param prop: property boolean to set if value is a boolean
        :param value: boolean value
        :return: returns value as boolean
        ***REMOVED***
        class_name: str = property_.return_class_name(prop=prop)
        if not (isinstance(value, bool)):
            raise TypeError("boolean, is an instance of : {} , and can only be Either True or False".format(class_name))
        return value

    @staticmethod
    def set_status(prop: ndb.StringProperty, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            **set payment status**
                only two valid statuses paid and unpaid check if input is valid and set
        :param prop:
        :param value:
        :return:
        ***REMOVED***
        class_name: str = property_.return_class_name(prop=prop)
        if not (isinstance(value, str)):
            message: str = ***REMOVED***status, is an instance of : {} , and can only be a string 
            representing payment status***REMOVED***.format(class_name)
            raise TypeError(message)

        temp = value.strip().lower()
        if not bool(temp):
            raise ValueError("status, is an instance of : {} , and cannot be Null".format(class_name))

        if temp not in property_.__payment_statuses:
            message: str = ***REMOVED*** status should either paid or unpaid this {} is not a valid status***REMOVED***.format(value)
            raise TypeError("{} invalid status".format(message))

        return temp

    @staticmethod
    def set_string(prop: ndb.StringProperty, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            **Generic String Setter**
                checks only that a string is a string
        :param prop: ndb -> property being set
        :param value: string
        :return:
        ***REMOVED***
        class_name: str = property_.return_class_name(prop=prop)
        if not (isinstance(value, str)):
            raise TypeError("Is an instance of : {} , and can only be a string".format(class_name))

        if not bool(value.strip()):
            raise ValueError("is an Instance of : {} , and cannot be Null".format(class_name))

        return value.strip().lower()

    @staticmethod
    def set_schedule_term(prop: ndb.StringProperty, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            set scheduled term - raises an error if scheduled term is not a string or not one of
            the valid scheduled terms
        :param prop:
        :param value:
        :return:
        ***REMOVED***
        class_name: str = property_.return_class_name(prop=prop)
        if not (isinstance(value, str)):
            raise TypeError("scheduled term, is an instance of : {} ,  and can only be a string ".format(class_name))

        if not bool(value.strip()):
            raise ValueError("schedule term, is an instance of : {}, and cannot be Null".format(class_name))

        temp = value.strip().lower()
        # TODO - Rewrite this or create a translator for paypal plans payment schedule
        schedule_terms: typing.List[str] = get_plan_scheduled_terms()
        if temp in schedule_terms:
            return temp
        raise ValueError("scheduled term, can only be one of the following values : {} ".format(schedule_terms))

    @staticmethod
    def set_schedule_day(prop: ndb.IntegerProperty, value: typing.Union[int, None]) -> int:
        ***REMOVED***
            set scheduled day for this plan depending on this plans scheduled term the transaction will
            be made on the first transaction day coinciding with the scheduled term
        :param prop: scheduled day property
        :param value: value to set
        :return: scheduled day as integer
        ***REMOVED***
        class_name: str = property_.return_class_name(prop=prop)

        if not (isinstance(value, int)):
            raise TypeError('scheduled day, is an instance of : {}, and can only be an integer'.format(class_name))
        if value not in get_scheduled_term_days():
            message: str = '''scheduled day, is an instance of : {}, and can 
            only be a value between 1 -> 5 of every month'''.format(class_name)
            raise ValueError(message)
        return value

    @staticmethod
    def set_number(prop: ndb.IntegerProperty, value: typing.Union[int, None]) -> int:
        ***REMOVED***
            set an integer number into a database property
            will check if input is really an integer and then returns the number if not
            raises TypeError if value is out of range will raise a ValueError
        :param prop: property to set
        :param value: value being set must be integer
        :return: valid integer
        ***REMOVED***
        class_name: str = property_.return_class_name(prop=prop)
        if not (isinstance(value, int)):
            raise TypeError('Number, is a instance of : {}, and can only be an integer'.format(class_name))

        if value < 0:
            raise TypeError("Number, is an instance of :{} and cannot accept negative numbers".format(class_name))

        return value

    @staticmethod
    def set_date(prop: ndb.DateProperty, value: date) -> date:
        ***REMOVED***
            **set_date**
                checks to see if date is valid if yes returns the date
                throws TypeError if an invalid date has been supplied

        :param prop: property representing the date
        :param value: value to set to property
        :return: returns valid date only
        ***REMOVED***
        class_name: str = property_.return_class_name(prop=prop)
        if not (isinstance(value, date)):
            raise TypeError("date is an instance of : {}, and can only be an instance of date".format(class_name))
        return value

    @staticmethod
    def set_payment_method(prop: ndb.StringProperty, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            **set_payment_method**
                checks to see if payment method is valid if yes then return payment methods
                raises TypeError in-case of invalid Type and ValueError if value is not a payment method
        :param prop: property we are setting
        :param value: the value to set
        :return: returns a payment method as string
        ***REMOVED***
        class_name: str = property_.return_class_name(prop=prop)
        if not (isinstance(value, str)):
            message: str = ***REMOVED***payment method, is an instance of : {}, and can only be a string representing a 
            valid payment method***REMOVED***.format(class_name)
            raise TypeError(message)

        if value.lower().strip() not in get_payment_methods():
            message: str = ***REMOVED***this value : {}, is not a valid payment method, 
            supported payment methods are : {}***REMOVED***.format(value, get_payment_methods())
            raise ValueError(message)

        return value.lower().strip()

    @staticmethod
    def set_percent(prop: ndb.IntegerProperty, value: typing.Union[int, None]) -> int:
        ***REMOVED***
            **set_percent**
                set_percent will check if the percentage value is an integer and then return the percentage value
                if not then it will raise ValueError or TypeError depending on the reason
        :param prop: property to set the percentage
        :param value: percentage as integer to set in property
        :return: percentage as an integer
        ***REMOVED***
        class_name: str = property_.return_class_name(prop=prop)
        utils_instance: Util = Util()

        if not isinstance(value, int):
            message: str = ***REMOVED***Percent is an instance of : {} and can only be an 
            integer representing a percentage***REMOVED***.format(class_name)
            raise TypeError(message)

        if utils_instance.percent_valid(percent=value):
            message: str = ***REMOVED***This value : {}, is not a valid Percentage, percent may be a value 
            from 0 to 100***REMOVED***.format(value)
            raise ValueError(message)
        return value

    @staticmethod
    def set_currency(prop: ndb.StringProperty, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            **set_currency**
                checks if currency symbol is one of valid currency symbol if yes returns the symbol
                if not raise ValueError or TypeError depending on why the value is invalid
        :param prop: property where the currency symbol may be set
        :param value: value representing the currency symbol
        :return: will return currency symbol representing a string
        ***REMOVED***
        from config.currencies import currency_util
        class_name: str = property_.return_class_name(prop=prop)
        if not (isinstance(value, str)):
            message: str = '''Currency is an Instance of : {}, and should be a string representation 
            of a currency symbol'''.format(class_name)
            raise TypeError(message)
        if value not in currency_util.currency_symbols():
            raise ValueError("This value : {} is not a valid currency symbol".format(value))
        return value

    # noinspection PyUnusedLocal,DuplicatedCode
    @staticmethod
    def set_email(prop: ndb.StringProperty, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            **set_email**
                used for the following
                If email is valid return email address else raise an error
            :param value: email address
            :param prop: email property
        ***REMOVED***
        if not (isinstance(value, str)):
            message: str = '''An Instance of : {} ::  can only be a string representing email'''.format(
                str(prop.__class__.__name__))
            raise ValueError(message)

        if not bool(value.strip()):
            raise ValueError(" {} cannot be Null".format(str(prop.__class__.__name__)))

        if property_.regex_check_email(email=value.strip().lower()):
            return value.strip().lower()
        raise ValueError(" {} is not a valid email address".format(value))

    @staticmethod
    def set_cell(prop: ndb.StringProperty, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            **set_cell**
                check if value is string , regex check the cell number
                then format the number internationally and return the formatted value
        :param prop: the property as string the cell number will be stored in
        :param value: cell number
        :return: formatted cell number as string
        ***REMOVED***
        class_name: str = property_.return_class_name(prop=prop)
        if not isinstance(value, str):
            message: str = '''An Instance of: {} : should be a string representing a 
            cell number in international format'''.format(class_name)
            raise TypeError(message)
        if property_.regex_check_cell(cell=value.strip()):
            return property_.format_cell_number(cell=value)
        raise ValueError("This value: {} , is not a valid cell number".format(value))

    # noinspection PyUnusedLocal
    @staticmethod
    def set_password(prop: ndb.StringProperty, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            **set_password**
                validate the correctness of the password and its complexity if  accurate
                then return the hash of the password to be stored on the database
            :param: value: password in plain-text
            :param : prop: the password property being set
            :return: password in hash format
        ***REMOVED***
        from werkzeug.security import generate_password_hash
        class_name: str = property_.return_class_name(prop=prop)
        if not isinstance(value, str):
            message: str = '''password is an instance of : {} :  should be a string representing 
            user password'''.format(class_name)
            raise TypeError(message)

        if property_.password_complexity(password=value.strip()):
            return generate_password_hash(value, method="pbkdf2:sha256", salt_length=8)
        message: str = '''password must be at least 8 characters in length, and contain lower-case and upper-case letters, 
        numbers and at least a special character'''
        raise ValueError(message)

    @staticmethod
    def set_value_amount(prop: ndb.IntegerProperty, value: typing.Union[int, None]) -> int:
        ***REMOVED***
            DOCS:
                1. amount in integer used to validate amounts in cash on AmountMixin
                2. amount is in cents
        :param prop:
        :param value: amount in integer representing cents
        :return: integer representing money in cents of whatever currency is being represented
        ***REMOVED***
        class_name: str = property_.return_class_name(prop=prop)
        if not (isinstance(value, int)):
            message: str = '''Amount is an instance of : {} : can only be an Integer 
            representing money in cents'''.format(class_name)
            raise TypeError(message)

        # NOTE: does not allow negative values
        if value < 0:
            message: str = ***REMOVED***This value : {} , is not valid, it must be a currency amount in cents and 
            must always be a positive integer***REMOVED***.format(value)
            raise ValueError(message)

        return value

    @staticmethod
    def set_domain(prop: ndb.StringProperty, value: typing.Union[str, None]) -> str:
        ***REMOVED***
            Docs:
                check the domain name regex if it passes resolve
                the domain name if it passes then return domain name
            :param: prop: ndb.StringProperty where the domain name will be stored
            :param: value: value in string format representing a domain name
            :return: str representing verified domain name
        ***REMOVED***
        class_name: str = property_.return_class_name(prop=prop)
        if not (isinstance(value, str)):
            message: str = ***REMOVED***domain, is an instance of : {} and can only be a string, representing 
            a valid domain name***REMOVED***.format(class_name)
            raise TypeError(message)

        domain = value.strip()
        regex_passes = property_.regex_check_domain(domain=domain)
        domain_valid = property_.resolve_domain_name(domain=domain)
        if regex_passes and domain_valid:
            return domain
        raise ValueError("This value : {} is not a valid domain name, or the domain may not be accessible".format(value))


property_: PropertySetters = PropertySetters()
# NOTE: insures that setters is a singleton or declared only once
del PropertySetters

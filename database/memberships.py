***REMOVED***
    **Memberships Module**
        *Class Definitions for: Memberships, Memberships Plans and Coupons*
        This classes are related to creating and management of organizational memberships and their membership plans
        for organizations products or services in order to collect payments from clients

***REMOVED***

__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

import typing
from typing import Optional
from datetime import datetime, date
from google.cloud import ndb
from config.exception_handlers import handle_store_errors
from config.exceptions import InputError, error_codes
from database.mixins import AmountMixin
from database.setters import property_
from utils.utils import get_days_in_milliseconds, today
from database.basemodel import BaseModel


class MembershipValidators:
    ***REMOVED***
        **Class Memberships Validators**
            validating input and authenticating calls to memberships database
    ***REMOVED***

    @staticmethod
    def start_date_valid(start_date: date) -> bool:
        ***REMOVED***
            **start_date_valid**
                check if date is from today and falls within normal parameters
        ***REMOVED***
        return isinstance(start_date, date) and start_date > today()

    @staticmethod
    async def start_date_valid_async(start_date: date) -> bool:
        ***REMOVED***
            **asynchronous version of start_date_valid_async**
                check if date is from today and falls within normal parameters
        ***REMOVED***

        return start_date > today()


class PlanValidators:
    ***REMOVED***
        **Class PlanValidators**
            validating and authenticating calls to MembershipPlans Database

    ***REMOVED***

    # noinspection DuplicatedCode
    @staticmethod
    @handle_store_errors
    def plan_exist(organization_id: str, plan_id: str) -> Optional[bool]:
        ***REMOVED***
            **plan_exist**
                checks if plan exist using plan_id if this is the case the returns True else False
                raises InputError or TypeError in case of an invalid input


        :param organization_id: unique organization id
        :param plan_id: unique plan_id
        :return: True if plan exist or False Otherwise
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(plan_id, str) or not bool(plan_id.strip()):
            message: str = "plan_id cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        plan_instance: MembershipPlans = MembershipPlans.query(MembershipPlans.organization_id == organization_id,
                                                               MembershipPlans.plan_id == plan_id).get()
        return bool(plan_instance)

    # noinspection DuplicatedCode
    @staticmethod
    @handle_store_errors
    async def plan_exist_async(organization_id: str, plan_id: str) -> Optional[bool]:
        ***REMOVED***
            **asynchronous version of of plan_exist_async**
                checks if plan already exist returns True if it does - uses plan id to check
                raises InputError or TypeError in case of an invalid input

        :param organization_id:
        :param plan_id:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(plan_id, str) or not bool(plan_id.strip()):
            message: str = "plan_id cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        plan_instance: MembershipPlans = MembershipPlans.query(
            MembershipPlans.organization_id == organization_id,
            MembershipPlans.plan_id == plan_id).get_async().get_result()

        return bool(plan_instance)

    # noinspection DuplicatedCode
    @staticmethod
    @handle_store_errors
    def plan_name_exist(organization_id: str, plan_name: str) -> Optional[bool]:
        ***REMOVED***
            **plan_name_exist**
                checks if a plan exists by using the plan name , if plan is found returns True, False otherwise
                raises InputError or TypeError in case of an invalid input

        :param organization_id: unique organization_id
        :param plan_name:  unique plan_name
        :return: bool -> True / False
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(plan_name, str) or not bool(plan_name.strip()):
            message: str = "plan_name cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        plan_instance: MembershipPlans = MembershipPlans.query(
            MembershipPlans.organization_id == organization_id,
            MembershipPlans.plan_name == plan_name.strip().lower()).get()

        return bool(plan_instance)

    # noinspection DuplicatedCode
    @staticmethod
    @handle_store_errors
    async def plan_name_exist_async(organization_id: str, plan_name: str) -> Optional[bool]:
        ***REMOVED***
            **async version of plan_name_exist**
                returns true in-case the plan name is already taken false otherwise
                raises an error in case of input error
        :param organization_id:
        :param plan_name:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(plan_name, str) or not bool(plan_name.strip()):
            message: str = "plan_name cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        plan_instance: MembershipPlans = MembershipPlans.query(
            MembershipPlans.organization_id == organization_id,
            MembershipPlans.plan_name == plan_name.strip().lower()).get_async().get_result()

        return bool(plan_instance)


class CouponsValidator:
    ***REMOVED***
        **Class Coupons Validator**
            validating input and authenticating calls to Coupons database
    ***REMOVED***
    def __init__(self) -> None:
        pass

    # noinspection DuplicatedCode
    @staticmethod
    @handle_store_errors
    def coupon_exist(organization_id: str, code: str) -> Optional[bool]:
        ***REMOVED***
        **coupon_exist**
            checks if a coupon is already created
        :param organization_id:
        :param code:
        :return: True if a coupon is present
        ***REMOVED***

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(code, str) or not bool(code.strip()):
            message: str = "code cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        coupons_instance: Coupons = Coupons.query(Coupons.organization_id == organization_id,
                                                  Coupons.code == code.strip().lower()).get()

        return bool(coupons_instance)

    # noinspection DuplicatedCode
    @staticmethod
    @handle_store_errors
    async def coupon_exist_async(organization_id: str, code: str) -> Optional[bool]:
        ***REMOVED***
        **coupon_exist_async**
            an asynchronous version of coupon_exist

        :param organization_id:
        :param code:
        :return:
        ***REMOVED***

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(code, str) or not bool(code.strip()):
            message: str = "code cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        coupons_instance: Coupons = Coupons.query(
            Coupons.organization_id == organization_id, Coupons.code == code.strip().lower()).get_async().get_result()

        return bool(coupons_instance)

    @staticmethod
    def expiration_valid(expiration_time: int) -> bool:
        ***REMOVED***
        **expiration_valid**
            checks if expiration_time is valid

        :param expiration_time:
        :return:
        ***REMOVED***
        if not (isinstance(expiration_time, int)):
            message: str = "expiration_time can only be an integer"
            raise InputError(status=error_codes.input_error_code, description=message)

        return not expiration_time < get_days_in_milliseconds(days=1)

    @staticmethod
    async def expiration_valid_async(expiration_time: int) -> bool:
        ***REMOVED***
            **expiration_valid_async**
                checks if expiration time is valid

        :param expiration_time:
        :return: return bool indicating if membership hasn't expired
        ***REMOVED***

        if not (isinstance(expiration_time, int)):
            message: str = "expiration_time can only be an integer"
            raise InputError(status=error_codes.input_error_code, description=message)

        return not expiration_time < get_days_in_milliseconds(days=1)

    @staticmethod
    def discount_valid(discount_valid: int) -> bool:
        ***REMOVED***
        **discount_valid**
            checks if discount percentage is valid

        :param discount_valid:
        :return: returns True or False
        ***REMOVED***
        if not (isinstance(discount_valid, int)):
            message: str = "discount_valid can only be an integer"
            raise InputError(status=error_codes.input_error_code, description=message)

        return 0 < discount_valid > 100

    @staticmethod
    async def discount_valid_async(discount_valid: int) -> bool:
        ***REMOVED***
        **discount_valid_async**
            checks if discount percentage is valid

        :param discount_valid:
        :return: returns True or False
        ***REMOVED***
        if not (isinstance(discount_valid, int)):
            message: str = "discount_valid can only be an integer"
            raise InputError(status=error_codes.input_error_code, description=message)

        return 0 < discount_valid > 100


# noinspection DuplicatedCode
class Memberships(BaseModel):
    ***REMOVED***
        **Class Memberships**
            **AKA Subscriptions**
            NOTE: Tracks down which user belongs to which plan from which organization_id  and if the user is paid up or unpaid
            for the month it also captures the payment_method selected for the plan


        `Class Properties`
            1. property organization_id: the id of the organization a client is a member of
            2. property uid: the user id of the client
            3. property plan_id: the plan of payment the client is subscribed to
            4. property status: status in terms of payments of this membership
            5. property date_created: the date the membership has been created
            6. property plan_start_date: the date the plan has been activated
            7. property payment_method: method of payment for the membership plan
            8. property is_active_subscription: is user still actively subscribed or not
    ***REMOVED***
    organization_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    uid: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    plan_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    payment_status: str = ndb.StringProperty(default="unpaid", validator=property_.set_status, required=True)  # Paid/ Unpaid
    date_created: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=property_.set_datetime)
    plan_start_date: date = ndb.DateProperty(validator=property_.set_date)  # the date this plan will
    payment_method: str = ndb.StringProperty(default="paypal", validator=property_.set_payment_method)
    is_active_subscription: bool = ndb.BooleanProperty(default=True, validator=property_.set_bool)

    # become active

    def __eq__(self, other) -> bool:

        if self.__class__ != other.__class__:
            return False
        if self.uid != other.uid:
            return False
        if self.plan_id != other.plan_id:
            return False
        if self.date_created != other.date_created:
            return False
        if self.plan_start_date != other.plan_start_date:
            return False
        return True

    def __str__(self) -> str:
        return "<Memberships: organization_id: {}, uid: {}, plan_id: {}, status: {}, date_created: {}, " \
               "start_date: {}".format(self.organization_id, self.uid, self.plan_id, self.payment_status, self.date_created,
                                       self.plan_start_date)

    def __bool__(self) -> bool:
        return bool(self.uid) and bool(self.organization_id) and bool(self.plan_id)


# noinspection DuplicatedCode
class MembershipPlans(BaseModel):
    ***REMOVED***
        **Class Membership Plans**
            Payment plans for services and products belonging to an organization that created it,
            clients of such organization will subscribe to such payment plans in order to get access to services or products
            being offered by the organization.

        Contains a definition of all Membership Plans
        TODO - Memberships Plans must relate to PayPal Service Plans, when a plan gets created here
        it must also be created on PayPal, plan_id here must be the same as plan_id in paypal or
        another field to relate the two plans may be created...

    `Class Properties`
        1. property : organization_id : the id of the organization which created the membership plan.
        2. property : service_id: the id of the service or product the payment plan belong to.
        3. property : plan_id: the id of the membership plan.
        4. property : plan_name: the name of the payment plan.
        5. property : description : description of the created payment plan.
        6. property : total_members: total members subscribed to the membership plan.
        7. property : schedule_term: the terms of payment for a plan , determined the period upon which
                    collections / payments can be made.
        8. property : schedule_day: the days scheduled for payment collection for a plan-- see scheduled_term for context.
        9. property : term_payment_amount: the amount which would be paid when the time of collection has been reached.
        10. property : registration_amount: the amount which would be paid upon activation of the payment plan for a member.
        11. property : is_active: when true people can activate a membership under this payment plan for a service / product.
        12. property : date_created: the date the payment plan has been created

    ***REMOVED***
    organization_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    # Service ID will relate the plan to a specific service_id on Services here and on PayPal Products
    service_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    # NOTE a single service_id can be found on multiple plans
    plan_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    plan_name: str = ndb.StringProperty(validator=property_.set_string, indexed=True, required=True)
    description: str = ndb.StringProperty(validator=property_.set_string, required=True)
    total_members: int = ndb.IntegerProperty(default=0, validator=property_.set_number)
    schedule_day: int = ndb.IntegerProperty(default=0, validator=property_.set_schedule_day)  # 1 or 2 or 3 of
    # every month or # week, or three months
    schedule_term: str = ndb.StringProperty(default="monthly", validator=property_.set_schedule_term)  # Monthly,
    # Quarterly, Annually
    term_payment_amount: AmountMixin = ndb.StructuredProperty(AmountMixin)
    registration_amount: AmountMixin = ndb.StructuredProperty(AmountMixin)
    is_active: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)
    date_created: int = ndb.DateProperty(auto_now_add=True, validator=property_.set_datetime)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.plan_id != other.plan_id:
            return False
        if self.plan_name != other.plan_name:
            return False
        if self.total_members != other.total_members:
            return False
        return True

    def __str__(self) -> str:
        return "<MembershipPlans: organization_id: {}, uid: {}, plan_id:{}, plan_name: {}, description: {}, total_members: {}, schedule_day: {}, " \
               "term : {}".format(self.organization_id, self.uid, self.plan_id, self.plan_name, self.description,
                                  self.total_members, self.schedule_day, self.schedule_term)

    def __bool__(self) -> bool:
        return bool(self.plan_id) and bool(self.organization_id) and bool(self.service_id)


# noinspection DuplicatedCode
class MembershipInvoices(BaseModel):
    ***REMOVED***
        **Class Memberships Invoices**
            Invoices created for clients, based on payments made on service payment plans

        `**Class Properties**`
            1. property : organization_id: string: the id of the organization who's services and products the payment is based
            2. property :uid: string:  the ID of the user the invoice refers to
            3. property : plan_id: string: the id of the payment plan the invoice is related to
            4. property : invoice_id: string : unique id of this invoice
            5. property : invoice_number: string: sequential number of this invoice
            6. property : date_created: datetime : the date the invoice is created
            7. property : invoice_sent: bool : indicates if the invoice has been sent to the user / client
            8. property : invoice_paid: bool: indicates if invoice has been paid
            9. property : date_paid: date : the date payment has been made
            10. property : payment_amount: AmountMixin : the amount to be paid for this invoice
            11. property : amount_paid: AmountMixin : the amount which has been paid for this invoice

    ***REMOVED***
    organization_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True)
    uid: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True)
    plan_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True)
    invoice_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True)
    invoice_number: str = ndb.StringProperty(validator=property_.set_id, indexed=True)
    date_created: date = ndb.DateProperty(auto_now_add=True, validator=property_.set_date)
    invoice_sent: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)
    invoice_paid: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)
    date_paid: date = ndb.DateProperty(validator=property_.set_date)
    payment_amount: AmountMixin = ndb.StructuredProperty(AmountMixin)
    amount_paid: AmountMixin = ndb.StructuredProperty(AmountMixin)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.uid != other.uid:
            return False
        if self.invoice_id != other.invoice_id:
            return False
        if self.payment_amount.amount_cents != other.payment_amount.amount_cents:
            return False
        if self.payment_amount.currency != other.payment_amount.currency:
            return False
        if self.amount_paid.amount_cents != other.amount_paid.amount_cents:
            return False
        if self.amount_paid.currency != other.amount_paid.currency:
            return False
        return True

    def __sub__(self, other) -> AmountMixin:
        if self.payment_amount.currency != other.payment_amount.currency:
            raise TypeError("Incompatible currencies")
        self.payment_amount.amount_cents -= other.payment_amount.amount_cents
        return self.payment_amount

    def __add__(self, other) -> AmountMixin:
        if self.payment_amount.currency != other.payment_amount.currency:
            raise TypeError("Incompatible currencies")
        self.payment_amount.amount_cents += other.payment_amount.amount_cents
        return self.payment_amount

    def __str__(self) -> str:
        return "<Invoice invoice_number: organization_id: {}, uid: {}, plan_id: {}, invoice_id: {}, " \
               "invoice_number: {} date_created: {}, payment: {}, paid: {}".format(
                self.organization_id, self.uid, self.plan_id, self.invoice_id, self.invoice_number, self.date_created,
                self.payment_amount.__str__(), self.amount_paid.__str__())

    def __bool__(self) -> bool:
        ***REMOVED***
        **__bool__**
            returns true if MembershipInvoices is valid
        :return: bool
        ***REMOVED***
        user_bool: bool = bool(self.uid) and bool(self.organization_id)
        return user_bool and bool(self.uid) and bool(self.plan_id) and bool(self.invoice_id)


# noinspection DuplicatedCode
class Coupons(BaseModel):
    ***REMOVED***
        **Coupons**
            Class for the management and storage of Coupons in the Database
            applied on checkout of memberships
            front end should read coupons on checkout and apply the code to registration fees only ...
            the admin app should setup the coupon codes.
            endpoints should be provided via view and api

        `Coupons properties`
            1. property: organization_id: string: the string relating the organization which created the Coupon Code
               for application in its services
            2. property: code: string(12): the coupon code which must be applied in order for the coupon to be
               applied on memberships
            3. property: discount_percent: int : the percentage to apply to the price in case a client or user supplies
               the coupon code (see code).
            4. property: is_valid: bool : when true the coupon_code can be used
            5. property: date_created: datetime: the date and time the coupon code was created
            6. property: expiration_time: int: time in milliseconds when the coupon code will expire

    ***REMOVED***
    organization_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True)
    code: str = ndb.StringProperty(default=None, validator=property_.set_coupon_code, indexed=True)
    discount_percent: int = ndb.IntegerProperty(default=0, validator=property_.set_number)
    is_valid: bool = ndb.BooleanProperty(default=True, validator=property_.set_bool)
    date_created: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=property_.set_datetime)
    expiration_time: int = ndb.IntegerProperty(default=0, validator=property_.set_number)

    def __str__(self) -> str:
        return "<Coupons: organization_id: {}, Code: {}, Discount: {}, Is Valid: {}, Date Created: {}, " \
               "Expire at : {}".format(self.organization_id, self.code, self.discount, self.is_valid, self.date_created,
                                       self.expiration_time)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.code != other.code:
            return False
        if self.discount != other.discount:
            return False
        if self.expiration_time != other.expiration_time:
            return False
        return True

    def __bool__(self) -> bool:
        return bool(self.code) and bool(self.organization_id)


# noinspection DuplicatedCode
class AccessRights(BaseModel):
    ***REMOVED***
        TODO safely remove this class
        There should be a route that the client app can call to get permission for a route,
        the route should accept route and uid and then respond with True or False
        of all the routes he or she can access
        `Class Properties`

    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=property_.set_id, indexed=True)
    plan_id: str = ndb.StringProperty(validator=property_.set_id, indexed=True)
    access_rights_list: typing.List[str] = ndb.StringProperty(repeated=True)  # a list containing the rights of users

    # TODO - finish this

    def __bool__(self) -> bool:
        return bool(self.plan_id)


class MembershipDailyStats(BaseModel):
    ***REMOVED***
        provides information and settings pertaining to paying members
        run update stats task against this class daily
    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=property_.set_id, indexed=True)
    daily_id: str = ndb.StringProperty(validator=property_.set_id, indexed=True)
    total_users: int = ndb.IntegerProperty(default=0, validator=property_.set_number)
    total_members: int = ndb.IntegerProperty(default=0, validator=property_.set_number)
    expected_monthly_earnings: AmountMixin = ndb.StructuredProperty(AmountMixin)
    expected_quarterly_earnings: AmountMixin = ndb.StructuredProperty(AmountMixin)
    expected_annual_earnings: AmountMixin = ndb.StructuredProperty(AmountMixin)
    expected_earnings_this_month: AmountMixin = ndb.StructuredProperty(AmountMixin)
    total_earned_so_far: AmountMixin = ndb.StructuredProperty(AmountMixin)
    date_created: date = ndb.DateProperty(validator=property_.set_date)

    def __str__(self) -> str:
        return "<MembershipDailyStats organization_id: {},  Users: {}, Members: {}, Earnings: {}, Total: {}".format(
                self.organization_id, self.daily_id, self.total_users, self.total_members,
                self.expected_earnings_this_month, self.total_earned_so_far)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.daily_id != other.daily_id:
            return False
        if self.total_users != other.total_users:
            return False
        if self.total_members != other.total_members:
            return False
        if self.expected_earnings_this_month != other.expected_earnings_this_month:
            return False
        if self.total_earned_so_far != other.total_earned_so_far:
            return False
        return True

    def __bool__(self) -> bool:
        return bool(self.daily_id) and bool(self.organization_id)

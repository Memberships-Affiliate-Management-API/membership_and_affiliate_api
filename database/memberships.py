import typing
from datetime import datetime, date
from google.api_core.exceptions import RetryError, Aborted
from google.cloud import ndb
from database.mixins import AmountMixin
from database.setters import setters
from utils.utils import get_days


class MembershipValidators:

    @staticmethod
    def start_date_valid(start_date: date) -> bool:
        ***REMOVED***
            check if date is from today and falls within normal parameters
        ***REMOVED***
        now = datetime.now().date()
        if isinstance(start_date, date) and start_date > now:
            return True
        return False

    @staticmethod
    async def start_date_valid_async(start_date: date) -> bool:
        ***REMOVED***
            check if date is from today and falls within normal parameters
        ***REMOVED***
        now = datetime.now().date()
        if isinstance(start_date, date) and start_date > now:
            return True
        return False


class PlanValidators:

    @staticmethod
    def plan_exist(plan_id: str) -> typing.Union[None, bool]:
        ***REMOVED***
            return True or False
            return None if Error
        ***REMOVED***
        if not isinstance(plan_id, str):
            return False
        plan_id = plan_id.strip()
        if plan_id == "":
            return False
        try:
            plan_instance: MembershipPlans = MembershipPlans.query(MembershipPlans.plan_id == plan_id).get()
            if isinstance(plan_instance, MembershipPlans):
                return True
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        except Aborted:
            return None
        return False

    @staticmethod
    async def plan_exist_async(plan_id: str) -> typing.Union[None, bool]:
        ***REMOVED***
            return True or False
            return None if Error
        ***REMOVED***
        if not isinstance(plan_id, str):
            return False
        plan_id = plan_id.strip()
        if plan_id == "":
            return False
        try:
            plan_instance: MembershipPlans = MembershipPlans.query(
                MembershipPlans.plan_id == plan_id).get_async().get_result()
            if isinstance(plan_instance, MembershipPlans):
                return True
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        except Aborted:
            return None
        return False

    @staticmethod
    def plan_name_exist(plan_name: str) -> typing.Union[None, bool]:
        ***REMOVED***
            returns True or False if plan exist or dont exist
            returns None if an error occurred
        ***REMOVED***
        if not isinstance(plan_name, str):
            return False
        plan_name = plan_name.strip().lower()
        if plan_name == "":
            return False
        try:
            plan_instance: MembershipPlans = MembershipPlans.query(MembershipPlans.plan_name == plan_name).get()
            if isinstance(plan_instance, MembershipPlans):
                return True
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        return False

    @staticmethod
    async def plan_name_exist_async(plan_name: str) -> typing.Union[None, bool]:
        ***REMOVED***
            returns True or False if plan exist or dont exist
            returns None if an error occurred
        ***REMOVED***
        if not isinstance(plan_name, str):
            return False
        plan_name = plan_name.strip().lower()
        if plan_name == "":
            return False
        try:
            plan_instance: MembershipPlans = MembershipPlans.query(
                MembershipPlans.plan_name == plan_name).get_async().get_result()
            if isinstance(plan_instance, MembershipPlans):
                return True
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        return False


class CouponsValidator:
    def __init__(self):
        pass

    @staticmethod
    def coupon_exist(code: str) -> typing.Union[None, bool]:
        if not (isinstance(code, str)):
            return False
        if code == "":
            return False
        try:
            coupons_instance: Coupons = Coupons.query(Coupons.code == code).get()
            if isinstance(coupons_instance, Coupons):
                return True
            return False
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None

    @staticmethod
    async def coupon_exist_async(code: str) -> typing.Union[None, bool]:
        if not (isinstance(code, str)):
            return False
        if code == "":
            return False
        try:
            coupons_instance: Coupons = Coupons.query(Coupons.code == code).get_async().get_result()
            if isinstance(coupons_instance, Coupons):
                return True
            return False
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None

    @staticmethod
    def expiration_valid(expiration_time: int) -> bool:
        if not (isinstance(expiration_time, int)):
            return False
        if expiration_time < get_days(days=1):
            return False
        return True

    @staticmethod
    async def expiration_valid_async(expiration_time: int) -> bool:
        if not (isinstance(expiration_time, int)):
            return False
        if expiration_time < get_days(days=1):
            return False
        return True

    @staticmethod
    def discount_valid(discount_valid: int) -> bool:
        if not (isinstance(discount_valid, int)):
            return False
        if 0 < discount_valid > 100:
            return False
        return True

    @staticmethod
    async def discount_valid_async(discount_valid: int) -> bool:
        if not (isinstance(discount_valid, int)):
            return False
        if 0 < discount_valid > 100:
            return False
        return True


# noinspection DuplicatedCode
class Memberships(ndb.Model):
    ***REMOVED***
        TODO - add validators
    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    uid: str = ndb.StringProperty(validator=setters.set_id)
    plan_id: str = ndb.StringProperty(validator=setters.set_id)
    status: str = ndb.StringProperty(default="unpaid", validator=setters.set_status)  # Paid/ Unpaid
    date_created: date = ndb.DateTimeProperty(auto_now_add=True, validator=setters.set_date)
    plan_start_date: date = ndb.DateProperty(validator=setters.set_datetime)  # the date this plan will
    payment_method: str = ndb.StringProperty(validator=setters.set_payment_method)

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
        return "<Memberships: status: {}, date_created: {}, start_date: {}".format(self.status, str(self.date_created),
                                                                                   str(self.plan_start_date))

    def __repr__(self) -> str:
        return "Memberships: {}{}{}".format(self.uid, self.plan_id, self.status)

    def __bool__(self) -> bool:
        return bool(self.uid)

    def __len__(self) -> int:
        return int(self.__bool__())


# noinspection DuplicatedCode
class MembershipPlans(ndb.Model):
    ***REMOVED***
        contains a definition of all membership plans
        TODO - add validators
    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    plan_id: str = ndb.StringProperty(validator=setters.set_id)
    plan_name: str = ndb.StringProperty(validator=setters.set_string)
    description: str = ndb.StringProperty(validator=setters.set_string)
    total_members: int = ndb.IntegerProperty(validator=setters.set_number)
    schedule_day: int = ndb.IntegerProperty(default=0, validator=setters.set_schedule_day)  # 1 or 2 or 3 of
    # every month or # week, or three months
    schedule_term: str = ndb.StringProperty(default="monthly", validator=setters.set_schedule_term)  # Monthly,
    # Quarterly, Annually
    term_payment_amount: AmountMixin = ndb.StructuredProperty(AmountMixin)
    registration_amount: AmountMixin = ndb.StructuredProperty(AmountMixin)
    is_active: bool = ndb.BooleanProperty(default=False, validator=setters.set_bool)
    date_created: int = ndb.DateProperty(auto_now_add=True, validator=setters.set_datetime)

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
        return "<MembershipPlans: plan_name: {}, description: {}, total_members: {}, schedule_day: {}, " \
               "term : {}".format(self.plan_name, self.description, self.total_members,
                                  self.schedule_day, self.schedule_term)

    def __repr__(self) -> str:
        return "<Memberships: {}{}".format(self.plan_id, self.plan_name)

    def __bool__(self) -> bool:
        return bool(self.plan_id)

    def __len__(self) -> int:
        return int(self.__bool__())


# noinspection DuplicatedCode
class MembershipInvoices(ndb.Model):
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    uid: str = ndb.StringProperty(validator=setters.set_id)
    plan_id: str = ndb.StringProperty(validator=setters.set_id)
    invoice_id: str = ndb.StringProperty(validator=setters.set_id)
    invoice_number: str = ndb.StringProperty(validator=setters.set_id)
    date_created: date = ndb.DateProperty(auto_now_add=True, validator=setters.set_date)
    invoice_sent: bool = ndb.BooleanProperty(default=False, validator=setters.set_bool)
    invoice_paid: bool = ndb.BooleanProperty(default=False, validator=setters.set_bool)
    date_paid: date = ndb.DateProperty(validator=setters.set_date)
    payment_amount: AmountMixin = ndb.StructuredProperty(AmountMixin)
    amount_paid: AmountMixin = ndb.StructuredProperty(AmountMixin)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.uid != other.uid:
            return False
        if self.invoice_id != other.invoice_id:
            return False
        if self.payment_amount.amount != other.payment_amount.amount:
            return False
        if self.payment_amount.currency != other.payment_amount.currency:
            return False
        if self.amount_paid.amount != other.amount_paid.amount:
            return False
        if self.amount_paid.currency != other.amount_paid.currency:
            return False
        return True

    def __sub__(self, other) -> int:
        if self.payment_amount.currency != other.payment_amount.currency:
            raise TypeError("Incompatible currencies")
        return self.payment_amount.amount - other.payment_amount.amount

    def __add__(self, other) -> int:
        if self.payment_amount.currency != other.payment_amount.currency:
            raise TypeError("Incompatible currencies")
        return self.payment_amount.amount + other.payment_amount.amount

    def __str__(self) -> str:
        return "<Invoice invoice_number: {} , date_created: {}, payment: {}, paid: {}".format(self.invoice_number,
                                                                                              self.date_created,
                                                                                              self.payment_amount,
                                                                                              self.amount_paid)

    def __repr__(self) -> str:
        return self.__str__()

    def __bool__(self) -> bool:
        return bool(self.uid)

    def __len__(self) -> int:
        return int(self.__bool__())


# noinspection DuplicatedCode
class Coupons(ndb.Model):
    ***REMOVED***
        applied on checkout of memberships
        front end should read coupons on checkout and apply the code to registration fees only ...
        the admin app should setup the coupon codes.
        endpoints should be provided via view and api
    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    code: str = ndb.StringProperty(validator=setters.set_id)
    discount: AmountMixin = ndb.StructuredProperty(AmountMixin)
    is_valid: bool = ndb.BooleanProperty(default=True, validator=setters.set_bool)
    date_created: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=setters.set_datetime)
    expiration_time: int = ndb.IntegerProperty(default=0, validator=setters.set_number)

    def __str__(self) -> str:
        return "Code: {} Discount: {} Is Valid: {} Date Created: {} Expire at : {}".format(self.code, self.discount,
                                                                                           self.is_valid,
                                                                                           self.date_created,
                                                                                           self.expiration_time)

    def __repr__(self) -> str:
        return self.__str__()

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
        return bool(self.code)

    def __len__(self) -> int:
        return int(self.__bool__())


# noinspection DuplicatedCode
class AccessRights(ndb.Model):
    ***REMOVED***
        # TODO - add validators
        # TODO - use access rights to protect routes on the client app
        # There should be a route that the client app can call to get permission for a route,
        #  the route should accept route and uid and then respond with True or False
        # of all the routes he or she can access
    ***REMOVED***
    plan_id: str = ndb.StringProperty(validator=setters.set_id)
    access_rights_list: typing.List[str] = ndb.StringProperty(repeated=True)  # a list containing the rights of users

    # TODO - finish this

    def __bool__(self) -> bool:
        return bool(self.plan_id)

    def __len__(self) -> int:
        return int(self.__bool__())


class MembershipDailyStats(ndb.Model):
    ***REMOVED***
        provides information and settings pertaining to paying members

        run update stats task against this class daily
    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    daily_id: str = ndb.StringProperty(validator=setters.set_id)
    total_users: int = ndb.IntegerProperty(default=0, validator=setters.set_number)
    total_members: int = ndb.IntegerProperty(default=0, validator=setters.set_number)
    expected_monthly_earnings: AmountMixin = ndb.StructuredProperty(AmountMixin)
    expected_quarterly_earnings: AmountMixin = ndb.StructuredProperty(AmountMixin)
    expected_annual_earnings: AmountMixin = ndb.StructuredProperty(AmountMixin)
    expected_earnings_this_month: AmountMixin = ndb.StructuredProperty(AmountMixin)
    total_earned_so_far: AmountMixin = ndb.StructuredProperty(AmountMixin)
    date_created: date = ndb.DateProperty(validator=setters.set_date)

    def __str__(self) -> str:
        return "<Stats Users: {} Members: {}  Earnings: {} Total: {}".format(self.total_users,
                                                                             self.total_members,
                                                                             self.expected_earnings_this_month,
                                                                             self.total_earned_so_far)

    def __repr__(self) -> str:
        return self.__str__()

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
        return bool(self.daily_id)

    def __len__(self) -> int:
        return int(self.__bool__())

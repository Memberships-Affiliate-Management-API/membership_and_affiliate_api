"""
    **Affiliates NDB database Class **
    used to store and manage access and storage of affiliate data record
    this module also handles Class Errors and Validations while accessing and storing data into the
    class instance for database storage
"""

__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from typing import Optional, List, Union
from google.cloud import ndb
from datetime import date, datetime
from config.exception_handlers import handle_store_errors
from config.exceptions import InputError, error_codes
from database.mixins import AmountMixin
from database.setters import property_
from database.basemodel import BaseModel


class AffiliatesValidators:
    """
        **Class AffiliatesValidators**
            Input Validations for Affiliates
    """

    def __init__(self):
        super(AffiliatesValidators, self).__init__()

    @staticmethod
    @handle_store_errors
    def affiliate_exist(affiliate_id: Optional[str]) -> Optional[bool]:
        """
            **affiliate_exist**
                test if an affiliate already exists in the organization
                TODO- ensure this search takes into account the organization_id
        :param affiliate_id:
        :return: boolean -> indicating if affiliate_exist or not
        """
        if not isinstance(affiliate_id, str) or not bool(affiliate_id.strip()):
            message: str = 'affiliate_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        affiliate_instance: Affiliates = Affiliates.query(Affiliates.affiliate_id == affiliate_id).get()

        # returns true if affiliate exists
        return bool(affiliate_instance)

    @staticmethod
    @handle_store_errors
    def recruiter_registered(organization_id: Optional[str],
                             uid: Optional[str]) -> Optional[bool]:
        """
            **recruiter_registered**
                returns true or False according to registration status None otherwise

        :param organization_id:
        :param uid:
        :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        affiliate_instance: Affiliates = Affiliates.query(Affiliates.organization_id == organization_id,
                                                          Affiliates.uid == uid).get()
        # NOTE returns true if affiliate_instance is found
        return bool(affiliate_instance)


class RecruitsValidators:
    """
        **RecruitsValidators**
            Input Validations for recruits class
    """

    def __init__(self) -> None:
        super(RecruitsValidators, self).__init__()

    # noinspection DuplicatedCode
    @staticmethod
    @handle_store_errors
    def user_already_recruited(uid: Optional[str]) -> Optional[bool]:
        """
            **user_already_recruited**
                method user_already_recruited -> checks if user has already been recruited
                in this organization

        :param uid:
        :return:
        """
        # TODO - an organization_id
        if not (isinstance(uid, str)) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        recruit_instance: Recruits = Recruits.query(Recruits.uid == uid).get()

        # NOTE: returns true if user is already recruited
        return bool(recruit_instance)

    @staticmethod
    @handle_store_errors
    def user_already_an_affiliate(uid: Optional[str]) -> Optional[bool]:
        """
            ** method user_already_an_affiliate**
                checks if user is already an affiliate
        :param uid:
        :return:
        """
        # TODO - an organization_id
        if not (isinstance(uid, str)) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        affiliate_instance: Affiliates = Affiliates.query(Affiliates.uid == uid).get()

        # NOTE: returns true if user is already recruited
        return bool(affiliate_instance)


class EarningsValidators:
    """
        **Class EarningsValidators**
            class used to validate user earnings based on affiliate recruitments and
            membership payments
    """

    def __init__(self) -> None:
        super(EarningsValidators, self).__init__()

    @staticmethod
    @handle_store_errors
    def unclosed_earnings_already_exist(affiliate_id: str) -> Optional[bool]:
        if not (isinstance(affiliate_id, str)) or not bool(affiliate_id.strip()):
            message: str = "affiliate_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        earnings_instance: List[EarningsData] = EarningsData.query(EarningsData.affiliate_id == affiliate_id).get()

        # returns true if earnings already exists
        return bool(earnings_instance)


class Affiliates(BaseModel):
    """
        **Class Affiliates**
            class used to track affiliates registered

        **Class Properties**
            1. organization_id: string -> unique id to identify the organization for each affiliate instance
            2. affiliate_id: string -> unique id to identify the recruited affiliate
            3. uid: string -> user id to identify the user - same user as affiliate_id
            4. last_updated: datetime -> time indicating the last time this record was updated
            5. datetime_recruited: datetime -> time the affiliate was registered
            6. total_recruits: int -> indicates the total number of recruits under this affiliate
            7. is_active: bool -> indicates if the affiliate is active
            8. is_deleted: bool -> indicates if an affiliate is deleted or not.
    """
    organization_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    affiliate_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    uid: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    last_updated: datetime = ndb.DateTimeProperty(auto_now=True, validator=property_.set_datetime)
    datetime_recruited: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=property_.set_datetime)
    total_recruits: int = ndb.IntegerProperty(default=0, validator=property_.set_number)
    is_active: bool = ndb.BooleanProperty(default=True, validator=property_.set_bool)
    is_deleted: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.affiliate_id != other.affiliate_id:
            return False
        if self.uid != other.uid:
            return False
        return True

    def __str__(self) -> str:
        return "<Affiliates: organization_id: {}, affiliate_id: {}, uid: {}, date_recruited: {}, " \
               "total_recruits: {}".format(self.organization_id, self.affiliate_id, self.uid, self.datetime_recruited,
                                           self.total_recruits)

    def __bool__(self) -> bool:
        return bool(self.affiliate_id) and bool(self.organization_id) and bool(self.uid)
        # return True if self.affiliate_id else False


class Recruits(BaseModel):
    """
        **Class Recruits**
            class used to track recruited affiliates

        **Class Properties**
            1. organization_id: string -> identifies the organization the recruit belongs to
            2. affiliate_id: string -> the newly created affiliate_id for the recruited affiliate
            3. referrer_uid: string -> the same as affiliate_id on main Affiliates Class identify
                the affiliate who recruited this recruit
            4. datetime_recruited: datetime -> the date the affiliate recruit was recruited
            5. datetime_updated: datetime -> the date the affiliate recruit was updated
            6. is_member: bool -> true if recruit has subscribed into a membership plan
            7. recruit_plan_id: str -> if a recruit has subscribed to a plan this holds the payment plan id
            8. is_active: bool -> indicates if a recruit is active
            9. is_deleted: bool -> indicates if a recruit is deleted

    """
    organization_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    affiliate_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    referrer_uid: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    datetime_recruited: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=property_.set_date)
    datetime_updated: datetime = ndb.DateTimeProperty(auto_now=True, validator=property_.set_date)
    is_member: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)
    # TODO - test this first may need to remove plan ID
    # Membership plan id allows to get payment fees
    recruit_plan_id: str = ndb.StringProperty(validator=property_.set_id)
    is_active: bool = ndb.BooleanProperty(default=True, validator=property_.set_bool)
    is_deleted: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)

    def __str__(self) -> str:
        return "<Recruits: organization_id: {} , affiliate_id: {}, referrer_uid: {}, datetime_recruited: {}, " \
               "plan_id: {}".format(self.organization_id, self.affiliate_id, self.referrer_uid, self.datetime_recruited,
                                    self.recruit_plan_id)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.affiliate_id != other.affiliate_id:
            return False
        if self.referrer_uid != other.referrer_uid:
            return False
        return True

    def __bool__(self) -> bool:
        return bool(self.affiliate_id) and bool(self.organization_id) and bool(self.referrer_uid)
        # return True if self.affiliate_id else False


class EarningsData(BaseModel):
    """
        **Class EarningsData**
            class used to track periodical earnings per affiliate

        **Class Properties**
            1. organization_id: string -> id indicating the organization the earnings belong to
            2. affiliate_id: string -> id indicating the affiliate the earnings belong to
            3. start_date: date -> The date the earnings has been calculated from
            4. last_updated: date -> the date the earnings record has last been updated
            5. total_earned: AmountMixin -> Total earned earnings in AmountMixin
            6. is_paid: bool -> true if earnings has been paid
            7. on_hold: bool -> True if earnings has been put on hold
    """
    organization_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    affiliate_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    start_date: date = ndb.DateProperty(auto_now_add=True)
    last_updated: date = ndb.DateProperty(validator=property_.set_date)
    total_earned: AmountMixin = ndb.StructuredProperty(AmountMixin)
    is_paid: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)
    on_hold: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.affiliate_id != other.affiliate_id:
            return False
        if self.start_date != other.start_date:
            return False
        if self.total_earned != other.transactions_total:
            return False
        return True

    def __str__(self) -> str:
        return "<EarningsClass organization_id: {}, affiliate_id: {},  start_date: {}, end_date: {}, total_earned: {}, " \
               "is_paid: {}, on_hold: {}".format(self.organization_id, self.affiliate_id, self.start_date,
                                                 self.last_updated, self.total_earned, self.is_paid, self.on_hold)

    def __bool__(self) -> bool:
        # return True if self.affiliate_id else False
        return bool(self.affiliate_id) and bool(self.organization_id)


class AffiliateTransactionItems(BaseModel):
    """
        **Class AffiliateTransactionItems**
            keeps track of singular transaction items, the transaction id's can be found on
            AffiliateEarningsTransactions.transaction_id_list

        **Class Properties**
            1. transaction_id: string -> unique identifier for each transaction
            2. amount: string -> amount in the transaction
            3. transaction_date: datetime -> the date the transaction took place

        **NOTE:**
            Transactions here only relates to affiliate earnings so there is no transaction types
    """
    uid: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    transaction_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    amount: AmountMixin = ndb.StructuredProperty(AmountMixin, required=True)
    transaction_date: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=property_.set_date)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.amount != other.amount_cents:
            return False
        if self.transaction_id != other.transaction_id:
            return False
        return True

    def __str__(self) -> str:
        return "<AffiliateTransactionItem: transaction_id: {}, Amount: {}, date: {}".format(
            self.transaction_id, self.amount.__str__(), str(self.transaction_date))

    def __bool__(self) -> bool:
        # return True if self.transaction_id else False
        return bool(self.transaction_id) and bool(self.uid)


class AffiliateSettingsStats(BaseModel):
    """
        **Class AffiliateSettingsStats**
            if earnings are recurring then an affiliate will continue to earn income
            on their down-line ,
            if not then income will be earned once off when a recruited
            user becomes a member.

        **NOTE**
            the cron job for calculating affiliate income must take this class into consideration
            in order to accurately calculate affiliate income

        **Class Properties**
            1. organization_id: string -> organization identity
            2. earnings_percent: string -> amount in percentage that can be earned by an affiliate
            3. recurring_earnings: bool -> true if earnings can be earned in a recurring fashion false Otherwise
            4. total_affiliates_earnings: AmountMixin -> total amount earned by affiliates so far

        **NOTE**
            all amounts are in cents
    """
    organization_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    earnings_percent: int = ndb.IntegerProperty(default=0, validator=property_.set_percent, required=True)
    recurring_earnings: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)
    total_affiliates_earnings: AmountMixin = ndb.StructuredProperty(AmountMixin)
    total_affiliates: int = ndb.IntegerProperty(default=0, validator=property_.set_number)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.earnings_percent != other.earnings_percent:
            return False
        if self.total_affiliates_earnings != other.total_affiliates_earnings:
            return False
        if self.total_affiliates != other.total_affiliates:
            return False
        return True

    def __str__(self) -> str:
        return "<AffiliateSettingsStats organization_id: {},  Earnings Percent: {}, Recurring Earnings: {}, Total Affiliates Earnings: {}, " \
               "Total Affiliates: {}".format(self.organization_id, self.earnings_percent, self.recurring_earnings,
                                             self.total_affiliates_earnings.__str__(), self.total_affiliates)

    def __bool__(self) -> bool:
        # return True if self.earnings_percent is not None else False
        return bool(self.earnings_percent) and bool(self.organization_id)

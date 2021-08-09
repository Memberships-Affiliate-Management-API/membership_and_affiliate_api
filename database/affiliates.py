***REMOVED***
    **Affiliates NDB database Class **
    used to store and manage access and storage of affiliate data record
    this module also handles Class Errors and Validations while accessing and storing data into the
    class instance for database storage
***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import typing
from google.cloud import ndb
from datetime import date, datetime
from google.api_core.exceptions import RetryError, Aborted
from config.exception_handlers import handle_store_errors
from database.mixins import AmountMixin
from database.setters import setters


class AffiliatesValidators:
    ***REMOVED***
        **Class AffiliatesValidators**
            Input Validations for Affiliates
    ***REMOVED***
    def __init__(self):
        super(AffiliatesValidators, self).__init__()

    @staticmethod
    @handle_store_errors
    def affiliate_exist(affiliate_id: typing.Union[str, None]) -> typing.Union[None, bool]:
        ***REMOVED***
            returns true
        :param affiliate_id:
        :return: boolean -> indicating if affiliate_exist or not
        ***REMOVED***
        affiliate_instance: Affiliates = Affiliates.query(Affiliates.affiliate_id == affiliate_id).get()
        return isinstance(affiliate_instance, Affiliates)

    @staticmethod
    @handle_store_errors
    def recruiter_registered(organization_id: typing.Union[str, None],
                             uid: typing.Union[str, None]) -> typing.Union[None, bool]:
        ***REMOVED***
            returns true or False according to registration status None otherwise
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        affiliate_instance: Affiliates = Affiliates.query(Affiliates.organization_id == organization_id,
                                                          Affiliates.uid == uid).get()

        return isinstance(affiliate_instance, Affiliates)


class RecruitsValidators:
    ***REMOVED***
        **RecruitsValidators**
            Input Validations for recruits class
    ***REMOVED***
    def __init__(self):
        super(RecruitsValidators, self).__init__()

    # noinspection DuplicatedCode
    @staticmethod
    @handle_store_errors
    def user_already_recruited(uid: typing.Union[str, None]) -> typing.Union[None, bool]:
        ***REMOVED***
            TODO - an organization_id
            method user_already_recruited -> checks if user has already been recruited
            in this organization
        :param uid:
        :return:
        ***REMOVED***
        if not(isinstance(uid, str)) or (uid == ""):
            raise ValueError("UID cannot be Null, and can only be a string")

        recruit_instance: Recruits = Recruits.query(Recruits.uid == uid).get()
        if isinstance(recruit_instance, Recruits):
            return True
        return False

    @staticmethod
    @handle_store_errors
    def user_already_an_affiliate(uid: typing.Union[str, None]) -> typing.Union[None, bool]:
        ***REMOVED***
            TODO - an organization_id
            ** method user_already_an_affiliate**
                checks if user is already an affiliate
        :param uid:
        :return:
        ***REMOVED***
        if not(isinstance(uid, str)) or (uid == ""):
            raise ValueError("UID cannot be Null, and can only be a string")
        affiliate_instance: Affiliates = Affiliates.query(Affiliates.uid == uid).get()
        if isinstance(affiliate_instance, Affiliates):
            return True
        return False


class EarningsValidators:
    ***REMOVED***
        **Class EarningsValidators**
            class used to validate user earnings based on affiliate recruitments and
            membership payments
    ***REMOVED***
    def __init__(self):
        super(EarningsValidators, self).__init__()

    @staticmethod
    @handle_store_errors
    def unclosed_earnings_already_exist(affiliate_id: str) -> typing.Union[None, bool]:
        if not(isinstance(affiliate_id, str)) or (affiliate_id == ""):
            raise ValueError("Affiliate_id cannot be Null, and can only be a string")
        earnings_list: typing.List[EarningsData] = EarningsData.query(
            EarningsData.affiliate_id == affiliate_id).fetch()
        if isinstance(earnings_list, list) and len(earnings_list) > 0:
            return True
        return False


class Affiliates(ndb.Model):
    ***REMOVED***
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
    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    affiliate_id: str = ndb.StringProperty(validator=setters.set_id)
    uid: str = ndb.StringProperty(validator=setters.set_id)
    last_updated: datetime = ndb.DateTimeProperty(auto_now=True, validator=setters.set_datetime)
    datetime_recruited: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=setters.set_datetime)
    total_recruits: int = ndb.IntegerProperty(default=0, validator=setters.set_number)
    is_active: bool = ndb.BooleanProperty(default=True, validator=setters.set_bool)
    is_deleted: bool = ndb.BooleanProperty(default=False, validator=setters.set_bool)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.affiliate_id != other.affiliate_id:
            return False
        if self.uid != other.uid:
            return False
        return True

    def __str__(self) -> str:
        return "<Affiliates: date_recruited: {}, total_recruits: {}".format(self.datetime_recruited,
                                                                            self.total_recruits)

    def __repr__(self) -> str:
        return "<Affiliates: {}{}".format(self.affiliate_id, self.uid)

    def __bool__(self) -> bool:
        return bool(self.affiliate_id)
        # return True if self.affiliate_id else False

    def __len__(self) -> int:
        return int(self.__bool__())


class Recruits(ndb.Model):
    ***REMOVED***
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

    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    affiliate_id: str = ndb.StringProperty(validator=setters.set_id)
    referrer_uid: str = ndb.StringProperty(validator=setters.set_id)
    datetime_recruited: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=setters.set_date)
    datetime_updated: datetime = ndb.DateTimeProperty(auto_now=True, validator=setters.set_date)
    is_member: bool = ndb.BooleanProperty(default=False, validator=setters.set_bool)
    # TODO - test this first may need to remove plan ID
    recruit_plan_id: str = ndb.StringProperty(validator=setters.set_id)  # Membership plan id allows to get payment fees
    is_active: bool = ndb.BooleanProperty(default=True, validator=setters.set_bool)
    is_deleted: bool = ndb.BooleanProperty(default=False, validator=setters.set_bool)

    def __str__(self) -> str:
        return "<Recruits: {}{}{}".format(self.affiliate_id, self.referrer_uid, self.datetime_recruited)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.affiliate_id != other.affiliate_id:
            return False
        if self.referrer_uid != other.referrer_uid:
            return False
        return True

    def __bool__(self) -> bool:
        return bool(self.affiliate_id)
        # return True if self.affiliate_id else False

    def __len__(self) -> int:
        return int(self.__bool__())


class EarningsData(ndb.Model):
    ***REMOVED***
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
    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    affiliate_id: str = ndb.StringProperty(validator=setters.set_id)
    start_date: date = ndb.DateProperty(auto_now_add=True)
    last_updated: date = ndb.DateProperty(validator=setters.set_date)
    total_earned: AmountMixin = ndb.StructuredProperty(AmountMixin)
    is_paid: bool = ndb.BooleanProperty(default=False, validator=setters.set_bool)
    on_hold: bool = ndb.BooleanProperty(default=False, validator=setters.set_bool)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.affiliate_id != other.affiliate_id:
            return False
        if self.start_date != other.start_date:
            return False
        if self.total_earned != other.total_earned:
            return False
        return True

    def __str__(self) -> str:
        return "<EarningsClass start_date: {}, end_date: {}, total_earned: {}, is_paid: {}, on_hold: {}".format(
            self.start_date, self.last_updated, self.total_earned, self.is_paid, self.on_hold)

    def __repr__(self) -> str:
        return self.__str__()

    def __bool__(self) -> bool:
        # return True if self.affiliate_id else False
        return bool(self.affiliate_id)

    def __len__(self) -> int:
        return int(self.__bool__())


class AffiliateEarningsTransactions(ndb.Model):
    ***REMOVED***
        keeps track of amounts paid from earningsData
    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    affiliate_id: str = ndb.StringProperty(validator=setters.set_id)
    total_earned: AmountMixin = ndb.StructuredProperty(AmountMixin)
    transaction_id_list: typing.List[str] = ndb.StringProperty(repeated=True)
    last_transaction_time: datetime = ndb.DateTimeProperty(auto_now=True, validator=setters.set_date)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.affiliate_id != other.affiliate_id:
            return False
        if self.total_earned != other.total_earned:
            return False
        return True

    def __str__(self) -> str:
        return "<Total Earned: {} ".format(str(self.total_earned))

    def __repr__(self) -> str:
        return self.__str__()

    def __bool__(self) -> bool:
        # return True if self.affiliate_id else False
        return bool(self.affiliate_id)

    def __len__(self) -> int:
        return int(self.__bool__())


class AffiliateTransactionItems(ndb.Model):
    ***REMOVED***
        keeps track of singular transaction items
    ***REMOVED***
    transaction_id: str = ndb.StringProperty(validator=setters.set_id)
    amount: AmountMixin = ndb.StructuredProperty(AmountMixin)
    transaction_date: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=setters.set_date)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.amount != other.amount:
            return False
        if self.transaction_id != other.transaction_id:
            return False
        return True

    def __str__(self) -> str:
        return "<AffiliateTransactionItem Amount: {}, date: {}".format(str(self.amount), str(self.transaction_date))

    def __repr__(self) -> str:
        return self.__str__()

    def __bool__(self) -> bool:
        # return True if self.transaction_id else False
        return bool(self.transaction_id)

    def __len__(self) -> int:
        return int(self.__bool__())


class AffiliateSettingsStats(ndb.Model):
    ***REMOVED***
        if earnings are recurring then an affiliate will continue to earn income
        on their down-line ,
        if not then income will be earned once off when a recruited
        user becomes a member.
    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    earnings_percent: int = ndb.IntegerProperty(validator=setters.set_percent)
    recurring_earnings: bool = ndb.BooleanProperty(default=False, validator=setters.set_bool)
    total_affiliates_earnings: AmountMixin = ndb.StructuredProperty(AmountMixin)
    total_affiliates: int = ndb.IntegerProperty(default=0, validator=setters.set_number)

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
        return "Earnings Percent: {}, Recurring Earnings: {}, Total Affiliates Earnings: {}, " \
               "Total Affiliates: {}".format(str(self.earnings_percent), str(self.recurring_earnings),
                                             str(self.total_affiliates_earnings), str(self.total_affiliates))

    def __repr__(self) -> str:
        return self.__str__()

    def __bool__(self) -> bool:
        # return True if self.earnings_percent is not None else False
        return bool(self.earnings_percent)

    def __len__(self) -> int:
        # return self.earnings_percent
        return int(self.__bool__())

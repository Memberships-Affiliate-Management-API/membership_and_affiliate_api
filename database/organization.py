"""
    **Organization Module**
        *NDB. Class Definitions for Managing Organizations Data*
        ndb. Database Class to handle Organizational Data related
        to Memberships & Affiliates Management API , the Models will saves
        the data to GCP DataStore.

        Also Contain all validator classes related to Organizational Classes
"""

__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

import typing
from datetime import datetime
from google.cloud import ndb
from config.exception_handlers import handle_store_errors
from config.exceptions import InputError, error_codes
from database.mixins import AmountMixin
from database.setters import property_
from database.basemodel import BaseModel


class OrgValidators:
    """
        Main Class for Validators related to Organization
    """
    def __init__(self) -> None:
        pass

    @staticmethod
    @handle_store_errors
    def is_organization_exist(organization_id: typing.Union[str, None]) -> typing.Union[None, bool]:
        """
            **is_organization_exist**
                checks if an organization exist
        :param organization_id: unique identifier for the organization
        :return: True if Organization Exist
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()
        return bool(organization_instance)


class Organization(BaseModel):
    """
        **Organization Documentation**
            class contains information on organizations registered to use our API, this class enables users to
            be registered for under a specific organization as Users, Affiliates, Recruits, and or Memberships on
            Specific Plans, once a user creates an account the first step is to create an organization, and then start
            using the API.

        **NOTE:**
            Once an Organization is created its wallet must also be created and its key be stored here.
        `Class Properties`
            1. owner_uid: str -> organization owner uid usually this user is also admin
            2. organization_id: str -> unique id to identify this organization
            3. wallet_id: str -> unique id to identify the wallet belonging to this organization
            4. organization_name: str -> the name of this organization
            5. description: str -> detailed description for the organization
            6. total_affiliates: int -> a number equalling the total number of affiliates recruited by this organization
            7. total_paid: AmountMixin -> total amount of money in cents paid out from this organization to clients and etc
            8. total_members: int -> total number of users or clients who are paying members or subscribers
            9. total_users: int -> overall number of users
            9. projected_membership_payments : AmountMixin -> total expected earnings for this month
            10. total_membership_payments: AmountMixin -> total payments to the organization which came from memberships
            11. home_url: String -> Home page for the organization being registered
            12. login_callback_url: string -> login page url - the page to redirect the user to after successfull authentication
            13. recovery_callback_url: string -> recovery page callback url - specify where the user must be redirected to in order to complete password recovery process

    """
    # TODO - fully intergrate total users and total members
    owner_uid: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    organization_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    wallet_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    organization_name: str = ndb.StringProperty(validator=property_.set_string, required=True)
    description: str = ndb.StringProperty(validator=property_.set_string, required=True)
    total_affiliates: int = ndb.IntegerProperty(default=0, validator=property_.set_number)
    total_paid: AmountMixin = ndb.StructuredProperty(AmountMixin)
    total_members: int = ndb.IntegerProperty(default=0, validator=property_.set_number)
    total_users: int = ndb.IntegerProperty(default=0, validator=property_.set_number)
    projected_membership_payments: AmountMixin = ndb.StructuredProperty(AmountMixin)
    total_membership_payments: AmountMixin = ndb.StructuredProperty(AmountMixin)
    date_created: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=property_.set_datetime)
    date_updated: datetime = ndb.DateTimeProperty(auto_now=True, validator=property_.set_datetime)
    home_url: str = ndb.StringProperty(validator=property_.set_domain)
    login_callback_url: str = ndb.StringProperty(validator=property_.set_domain)
    recovery_callback_url: str = ndb.StringProperty(validator=property_.set_domain)

    def __str__(self) -> str:
        return "<Organization organization_id: {}, owner_uid: {}, wallet_id: {}, Name: {} Description: {} " \
               "Affiliates: {} Members: {}".format(self.organization_id, self.owner_uid, self.wallet_id,
                                                   self.organization_name, self.description, self.total_affiliates,
                                                   self.total_members)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.organization_id != other.organization_id:
            return False
        return True

    def __bool__(self) -> bool:
        return bool(self.organization_id) and bool(self.owner_uid) and bool(self.wallet_id)

    @ndb.model.ComputedProperty
    def balance(self) -> AmountMixin:
        amount = self.total_membership_payments.amount_cents - self.total_paid.amount_cents
        return AmountMixin(amount=amount, currency=self.total_paid.currency)


class AuthUserValidators:
    """
        `Validator Class Organization Authenticated Users`
            Used to validate users and input data for those accessing the Users View / API
    """
    def __init__(self) -> None:
        pass

    @staticmethod
    @handle_store_errors
    def user_is_member_of_org(uid: typing.Union[str, None],
                              organization_id: typing.Union[str, None]) -> typing.Union[None, bool]:
        """
            **user_is_member_of_org**
                checks if a specific user is a member of an organization
        :param uid: unique identifier of the user
        :param organization_id: unique organization identity
        :return: True if organization exist
        """
        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        auth_user_instance: typing.List[AuthorizedUsers] = AuthorizedUsers.query(
            AuthorizedUsers.uid == uid, AuthorizedUsers.organization_id == organization_id).get()

        return bool(auth_user_instance)

    @staticmethod
    @handle_store_errors
    def org_user_is_admin(uid: typing.Union[str, None],
                          organization_id: typing.Union[str, None]) -> typing.Union[None, bool]:
        """
            **org_user_is_admin**
                checks if user belongs to the organization and also if user is an admin of the organization

        :param uid:
        :param organization_id:
        :return:
        """
        if not (isinstance(uid, str)):
            raise InputError(status=500, description="uid cannot be Null")
        if not (isinstance(organization_id, str)):
            raise InputError(status=500, description="organization_id cannot be Null")

        auth_user_instance: AuthorizedUsers = AuthorizedUsers.query(
            AuthorizedUsers.uid == uid, AuthorizedUsers.organization_id == organization_id).get()

        return isinstance(auth_user_instance, AuthorizedUsers) and (auth_user_instance.role == "admin")


class AuthorizedUsers(BaseModel):
    """
        **AuthorizedUsers Class**
            details of the users authorized to update organization details and other data structures for this organization
            the roles are admin, super user, and support.
            if active is set to false the user role is suspended

        **AuthorizedUsers Properties**
            1. organization_id : str -> unique id for the organization
            2. uid: str -> user id representing the authorized user
            3. role: str -> role of the Authorized user
            4. is_active: str -> indicates if the user role has been activated
            5. date_created: datetime -> date this instance was created
            6. date_updated: datetime -> last date this instance was updated

    """
    organization_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    uid: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    role: str = ndb.StringProperty(validator=property_.set_string)
    is_active: bool = ndb.BooleanProperty(default=True, validator=property_.set_bool)
    date_created: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=property_.set_datetime)
    date_updated: datetime = ndb.DateTimeProperty(auto_now=True, validator=property_.set_datetime)

    def __str__(self) -> str:
        return f"""<AuthorizedUser organization_id: {self.organization_id}, uid: {self.uid}, role: {self.role}, 
        is_active: {self.is_active}"""

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.organization_id != other.organization_id:
            return False
        if self.uid != other.uid:
            return False
        if self.role != other.role:
            return False
        return True

    def __bool__(self) -> bool:
        return bool(self.organization_id) and bool(self.uid)


class OrgAccounts(BaseModel):
    """
        # TODO - Deprecate this not useful Wallets will store org wallets

        include details of the main organization payments accounts here
        # NOTE: OrgAccounts PayPal Email will be used for making payments out
        # to the Organization Upon successful collection
        # NOTE: Funds must be available in wallet in order to be withdrawn to
        # NOTE: the organization PayPal account

        # organizational Wallets in Wallets class can be indicated as such see Wallet Class
    """
    organization_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    paypal_email: str = ndb.StringProperty(default=None, validator=property_.set_email, indexed=True, required=True)
    is_verified: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool, indexed=True, required=True)

    def __str__(self) -> str:
        return f"""<OrgAccounts: organization_id: {self.organization_id}, Paypal Email {self.paypal_email}, 
        is_verified: {self.is_verified}"""

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.organization_id != other.organization_id:
            return False
        return True

    def __bool__(self) -> bool:
        return bool(self.organization_id) and bool(self.is_verified) and bool(self.paypal_email)


class PaymentResults(BaseModel):
    """
        # NOTE: this are payments from Organization Wallets to Organization PayPal Accounts
        for every payment which is approved by admin, retain the result of the
        payment here

        Mainly this class is updated by the system through cron jobs and users can read its details

    """
    organization_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    transaction_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    payment_result: str = ndb.StringProperty(validator=property_.set_string)
    time_created: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=property_.set_datetime)
    last_updated: datetime = ndb.DateTimeProperty(auto_now=True, validator=property_.set_datetime)

    def __str__(self) -> str:
        return f"""<PaymentResults: Organization_id: {self.organization_id}, Transaction_id: {self.transaction_id}, 
        Payment_result: {self.payment_result}"""

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.organization_id != other.organization_id:
            return False
        return True

    def __bool__(self) -> bool:
        return bool(self.organization_id) and bool(self.transaction_id)

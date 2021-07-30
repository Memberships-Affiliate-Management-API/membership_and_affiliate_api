***REMOVED***
    ndb. Database Class to handle Organizational Data related
    to Memberships & Affiliates Management API , the Models will saves
    the data to GCP DataStore.

    Also Contain all validator classes related to Organizational Classes
***REMOVED***
import typing
from datetime import datetime
from google.cloud import ndb
from config.exception_handlers import handle_store_errors
from config.exceptions import InputError
from database.mixins import AmountMixin
from database.setters import setters


class OrgValidators:
    ***REMOVED***
        Main Class for Validators related to Organization
    ***REMOVED***
    def __init__(self) -> None:
        pass

    @staticmethod
    @handle_store_errors
    def is_organization_exist(organization_id: typing.Union[str, None]) -> typing.Union[None, bool]:
        if not (isinstance(organization_id, str)):
            raise InputError(status=500, description="organization_id cannot be null")

        organization_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()
        if isinstance(organization_instance, Organization):
            return False
        return True


class Organization(ndb.Model):
    ***REMOVED***
        class contains information on organizations registered to use our API, this class enables users to
        be registered for under a specific organization as Users, Affiliates, Recruits, and or Memberships on
        Specific Plans, once a user creates an account the first step is to create an organization, and then start
        using the API.

        NOTE: Once an Organization is created its wallet must also be created and its key be stored here.
    ***REMOVED***
    owner_uid: str = ndb.StringProperty(validator=setters.set_id)
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    wallet_id: str = ndb.StringProperty(validator=setters.set_string)
    organization_name: str = ndb.StringProperty(validator=setters.set_string)
    description: str = ndb.StringProperty(validator=setters.set_string)
    total_affiliates: int = ndb.IntegerProperty(validator=setters.set_number)
    total_paid: AmountMixin = ndb.StructuredProperty(AmountMixin)
    total_members: int = ndb.IntegerProperty(validator=setters.set_number)
    projected_membership_payments: AmountMixin = ndb.StructuredProperty(AmountMixin)
    total_membership_payments: AmountMixin = ndb.StructuredProperty(AmountMixin)

    def __str__(self) -> str:
        return "<Organization Name: {} Affiliates: {} Members: {}".format(self.organization_name, self.total_affiliates,
                                                                          self.total_members)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.organization_id != other.organization_id:
            return False
        return True

    def __bool__(self) -> bool:
        return bool(self.organization_id)

    def __len__(self) -> int:
        return int(self.__bool__())


class AuthUserValidators:
    ***REMOVED***
        Used to validate users and input data for those accessing the Users View / API
    ***REMOVED***
    def __init__(self) -> None:
        pass

    @staticmethod
    @handle_store_errors
    def user_is_member_of_org(uid: typing.Union[str, None],
                              organization_id: typing.Union[str, None]) -> typing.Union[None, bool]:
        if not (isinstance(uid, str)):
            raise InputError(status=500, description="uid cannot be Null")
        if not (isinstance(organization_id, str)):
            raise InputError(status=500, description="organization_id cannot be Null")

        auth_users_list: typing.List[AuthorizedUsers] = AuthorizedUsers.query(AuthorizedUsers.uid == uid).fetch()
        for user_instance in auth_users_list:
            if user_instance.organization_id == organization_id:
                return True
        return False

    @staticmethod
    @handle_store_errors
    def org_user_is_admin(uid: typing.Union[str, None],
                          organization_id: typing.Union[str, None]) -> typing.Union[None, bool]:
        if not (isinstance(uid, str)):
            raise InputError(status=500, description="uid cannot be Null")
        if not (isinstance(organization_id, str)):
            raise InputError(status=500, description="organization_id cannot be Null")

        auth_user_instance: AuthorizedUsers = AuthorizedUsers.query(
            AuthorizedUsers.uid == uid, AuthorizedUsers.organization_id == organization_id).get()

        if isinstance(auth_user_instance, AuthorizedUsers) and (auth_user_instance.role == "admin"):
            return True
        return False


class AuthorizedUsers(ndb.Model):
    ***REMOVED***
        details of the users authorized to update organization details and other data structures for this organization
        the roles are admin, super user, and support.
        if active is set to false the user role is suspended
    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    uid: str = ndb.StringProperty(validator=setters.set_id)
    role: str = ndb.StringProperty(validator=setters.set_string)
    is_active: bool = ndb.BooleanProperty(default=True, validator=setters.set_bool)

    def __str__(self) -> str:
        return "<AuthorizedUser role: {}, is_active: {}".format(self.role, self.is_active)

    def __repr__(self) -> str:
        return self.__str__()

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
        return bool(self.organization_id)

    def __len__(self) -> int:
        return int(self.__bool__())


class OrgAccounts(ndb.Model):
    ***REMOVED***
        include details of the main organization payments accounts here
        # NOTE: OrgAccounts PayPal Email will be used for making payments out
        # to the Organization Upon successful collection
        # NOTE: Funds must be available in wallet in order to be withdrawn to
        # NOTE: the organization PayPal account

        # organizational Wallets in Wallets class can be indicated as such see Wallet Class
    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    paypal_email: str = ndb.StringProperty(validator=setters.set_email)
    is_verified: bool = ndb.BooleanProperty(default=setters.set_bool)

    def __str__(self) -> str:
        return "<OrgAccounts : Paypal {} ".format(self.paypal_email)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.organization_id != other.organization_id:
            return False
        return True

    def __bool__(self) -> bool:
        return bool(self.organization_id)

    def __len__(self) -> int:
        return int(self.__bool__())


class PaymentResults(ndb.Model):
    ***REMOVED***
        # NOTE: this are payments from Organization Wallets to Organization PayPal Accounts
        for every payment which is approved by admin, retain the result of the
        payment here

        Mainly this class is updated by the system through cron jobs and users can read its details

    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    transaction_id: str = ndb.StringProperty(validator=setters.set_id)
    payment_result: str = ndb.StringProperty(validator=setters.set_string)
    time_created: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=setters.set_datetime)
    last_updated: datetime = ndb.DateTimeProperty(auto_now=True, validator=setters.set_datetime)


    def __str__(self) -> str:
        return "<PaymentResults : PaymentResults {} ".format(self.payment_result)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.organization_id != other.organization_id:
            return False
        return True

    def __bool__(self) -> bool:
        return bool(self.organization_id)

    def __len__(self) -> int:
        return int(self.__bool__())

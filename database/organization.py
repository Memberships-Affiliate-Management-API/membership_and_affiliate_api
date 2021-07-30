import typing
from google.cloud import ndb
from config.exception_handlers import handle_store_errors
from config.exceptions import InputError
from database.mixins import AmountMixin
from database.setters import setters


class OrgValidators:
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
    owner_uid: str = ndb.StringProperty(validator=setters.set_id)
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
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
    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    transaction_id: str = ndb.StringProperty(validator=setters.set_id)
    payment_result: str = ndb.StringProperty(validator=setters.set_string)

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

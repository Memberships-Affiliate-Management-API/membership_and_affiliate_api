import typing
from google.cloud import ndb
from config.exception_handlers import handle_store_errors
from config.exceptions import InputError
from database.mixins import AmountMixin
from database.setters import setters


class OrgValidators:
    def __init__(self):
        pass

    @staticmethod
    @handle_store_errors
    def is_organization_exist(organization_id: typing.Union[str, None]) -> typing.Union[None, bool]:
        if not(isinstance(organization_id, str)):
            raise InputError(status=500, description="organization_id cannot be null")

        organization_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()
        if isinstance(organization_instance, Organization):
            return False
        return True


class Organization(ndb.Model):
    owner_uid: str = ndb.StringProperty(validator=setters.set_id)
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    organization_name: str = ndb.StringProperty(validator=setters.set_string)
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
        return 1 if self.__bool__() else 0


class OrgAccounts(ndb.Model):
    ***REMOVED***
        include details of the main organization payments accounts here
    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    paypal_email: str = ndb.StringProperty(validator=setters.set_email)

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
        return 1 if self.__bool__() else 0


class PaymentResults(ndb.Model):
    ***REMOVED***
        for every payment which is approved by admin, retain the result of the payment here
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
        return 1 if self.__bool__() else 0

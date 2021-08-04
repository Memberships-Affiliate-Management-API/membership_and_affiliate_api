from google.cloud import ndb
from config import config_instance
from database.setters import setters


class AmountMixin(ndb.Model):
    amount: int = ndb.IntegerProperty(default=None, validator=setters.set_value_amount)
    currency: str = ndb.StringProperty(default=config_instance.CURRENCY, validator=setters.set_currency)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.amount != other.amount:
            return False
        if self.currency != other.currency:
            return False
        return True

    def __add__(self, other) -> int:
        if self.__class__ != other.__class__:
            raise TypeError("Invalid type")
        if self.currency != other.currency:
            raise TypeError("Incompatible Currency")
        self.amount += other.amount
        return self.amount

    def __sub__(self, other) -> int:
        if self.__class__ != other.__class__:
            raise TypeError("Invalid type")
        if self.currency != other.currency:
            raise TypeError("Incompatible Currency")
        self.amount -= other.amount
        return self.amount

    def __str__(self) -> str:
        return "Amount: {} {}".format(self.currency, self.amount)

    def __repr__(self) -> str:
        return self.__str__()

    def __bool__(self) -> bool:
        # if term payment amount is set to even zero bool will return True
        return True if self.amount is not None else False

    def __len__(self) -> int:
        return int(self.__bool__())


class UserMixin(ndb.Model):
    email: str = ndb.StringProperty(validator=setters.set_email)
    password: str = ndb.StringProperty(validator=setters.set_password)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.email != other.email:
            return False
        if self.password != other.password:
            return False
        return True

    def __str__(self) -> str:
        return "<User {}".format(self.email)

    def __repr__(self) -> str:
        return self.__str__()

    def __bool__(self) -> bool:
        return bool(self.email)

    def __len__(self) -> int:
        return int(self.__bool__())


# TODO add validators for address
class AddressMixin(ndb.Model):
    ***REMOVED***
        a mixin for user addresses
    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    uid: str = ndb.StringProperty(validator=setters.set_id)
    line_1: str = ndb.StringProperty(default=None, validator=setters.set_string)
    city: str = ndb.StringProperty(default=None, validator=setters.set_string)
    zip_code: str = ndb.StringProperty(default=None, validator=setters.set_string)
    province: str = ndb.StringProperty(default=None, validator=setters.set_string)
    state: str = ndb.StringProperty(default=None, validator=setters.set_string)
    country: str = ndb.StringProperty(default=None, validator=setters.set_string)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.line_1 != other.line_1:
            return False
        if self.city != other.city:
            return False
        if self.zip_code != other.zip_code:
            return False
        if self.province != other.province:
            return False
        return True

    def __str__(self) -> str:
        return "<Address : {} {} {} {}".format(self.line_1, self.city, self.zip_code,
                                               self.province)

    def __repr__(self) -> str:
        return self.__str__()

    def __bool__(self) -> bool:
        return bool(self.line_1)

    def __len__(self) -> int:
        return int(self.__bool__())

***REMOVED***
    **NDB Database Common Mixins**
        This Module defines common Mixins which are useful in defining main database classes on the applications
***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from dataclasses import dataclass
from google.cloud import ndb
from config import config_instance
from database.setters import property_


class AmountMixin(ndb.Model):
    ***REMOVED***
    **Class AmountMixin**
        A mixin to represent Money in cents

    **Class Properties**
        1. property: Amount: Integer -> Money in Cents
        2. property: Currency: String ->  Currency symbol
    ***REMOVED***
    amount: int = ndb.IntegerProperty(default=None, validator=property_.set_value_amount)
    currency: str = ndb.StringProperty(default=config_instance.CURRENCY, validator=property_.set_currency)

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

    @property
    def urlsafe_key(self) -> bytes:
        return self.key.urlsafe()

    # Turns the class to dict and include instance key
    def to_dict(self) -> dict: return super().to_dict().update(key=self.urlsafe_key)

    @staticmethod
    def get_instance_by_key(key: bytes) -> ndb.Model:
        ***REMOVED***
            returns the model instance from a key in byte string format
        :param key:
        :return:
        ***REMOVED***
        return ndb.Key(urlsafe=key).get()


class UserMixin(ndb.Model):
    ***REMOVED***
        **Class UserMixin**
            handling user login properties of User Class -
            Passwords Hash are handled by werkzeug.security using the method : "pbkdf2:sha256"

        **Class Properties**
            1. Property: Email : String -> email password
            2. Property: Password : String -> User Password - will be converted to a password hash
    ***REMOVED***
    email: str = ndb.StringProperty(validator=property_.set_email)
    password: str = ndb.StringProperty(validator=property_.set_password)

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

    @property
    def urlsafe_key(self) -> bytes:
        return self.key.urlsafe()

    # Turns the class to dict and include instance key
    def to_dict(self) -> dict: return super().to_dict().update(key=self.urlsafe_key)

    @staticmethod
    def get_instance_by_key(key: bytes) -> ndb.Model:
        ***REMOVED***
            returns the model instance from a key in byte string format
        :param key:
        :return:
        ***REMOVED***
        return ndb.Key(urlsafe=key).get()


# TODO add validators for address
class AddressMixin(ndb.Model):
    ***REMOVED***
        **Class AddressMixin**
            a mixin for user addresses
        **Class Properties**
            1. organization_id: string -> the id of the organization the owner of the address has registered to
            2. uid: string -> the unique identifying id for the user who owns the address
            3. line_1: string -> Physical Address Line 1
            4. city: string -> The City or Town of the address
            5. zip_code: string -> Zip Code or postal code for the address
            6. province: string -> in-case of a country with provinces
            7. state: string -> in-case of a countries with states
            8. country: string -> physical address country
    # TODO - validate countries through a country list the membership API Supports
    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=property_.set_id)
    uid: str = ndb.StringProperty(validator=property_.set_id)
    line_1: str = ndb.StringProperty(default=None, validator=property_.set_string)
    city: str = ndb.StringProperty(default=None, validator=property_.set_string)
    zip_code: str = ndb.StringProperty(default=None, validator=property_.set_string)
    province: str = ndb.StringProperty(default=None, validator=property_.set_string)
    state: str = ndb.StringProperty(default=None, validator=property_.set_string)
    country: str = ndb.StringProperty(default=None, validator=property_.set_string)

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

    @property
    def urlsafe_key(self) -> bytes:
        return self.key.urlsafe()

    # Turns the class to dict and include instance key
    def to_dict(self) -> dict: return super().to_dict().update(key=self.urlsafe_key)

    @staticmethod
    def get_instance_by_key(key: bytes) -> ndb.Model:
        ***REMOVED***
            returns the model instance from a key in byte string format
        :param key:
        :return:
        ***REMOVED***
        return ndb.Key(urlsafe=key).get()


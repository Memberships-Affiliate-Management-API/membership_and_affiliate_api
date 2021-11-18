"""
    **NDB Database Common Mixins**
        This Module defines common Mixins which are useful in defining main database classes on the applications
"""

__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from dataclasses import dataclass
from google.cloud import ndb
from config import config_instance
from database.basemodel import BaseModel
from database.setters import property_


class AmountMixin(BaseModel):
    """
    **Class AmountMixin**
        A mixin to represent Money in cents

    **Class Properties**
        1. property: Amount: Integer -> Money in Cents
        2. property: Currency: String ->  Currency symbol
    """
    amount_cents: int = ndb.IntegerProperty(default=None, validator=property_.set_value_amount)
    currency: str = ndb.StringProperty(default=config_instance.CURRENCY, validator=property_.set_currency)

    @property
    def amount(self) -> int:
        return self.amount_cents

    @amount.setter
    def amount(self, value) -> None:
        self.amount_cents = value

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.amount_cents != other.amount_cents:
            return False
        if self.currency != other.currency:
            return False
        return True

    def __add__(self, other) -> any:
        # TODO - does not function properly it needs to return AmountMixin as results
        if self.__class__ != other.__class__:
            raise TypeError("Invalid type")
        if self.currency != other.currency:
            raise TypeError("Incompatible Currency")
        self.amount_cents += other.amount_cents
        return self

    def __sub__(self, other) -> any:
        # TODO - does not function properly it needs to return AmountMixin as results
        if self.__class__ != other.__class__:
            raise TypeError("Invalid type")
        if self.currency != other.currency:
            raise TypeError("Incompatible Currency")
        self.amount_cents -= other.amount_cents
        return self

    def __str__(self) -> str:
        return "Amount: {} {}".format(self.currency, self.amount_cents)

    def __bool__(self) -> bool:
        # if term payment amount is set to even zero bool will return True
        return bool(self.amount_cents) and bool(self.currency)


class UserMixin(BaseModel):
    """
        **Class UserMixin**
            handling user login properties of User Class -
            Passwords Hash are handled by werkzeug.security using the method : "pbkdf2:sha256"

        **Class Properties**
            1. Property: Email : String -> email password
            2. Property: Password : String -> User Password - will be converted to a password hash
    """
    email: str = ndb.StringProperty(validator=property_.set_email)
    password: str = ndb.StringProperty(validator=property_.set_password)


    def verify_login(self, password: str, email: str) -> bool:
        """
        **Method verify_login**
            Verify the user password

        **Parameters**
            1. password: String -> User Password

        **Returns**
            Boolean -> True if password matches else False
        """
        return self.email == email and self.password == password
    

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

    def __bool__(self) -> bool:
        return bool(self.email)


class AddressMixin(BaseModel):
    """
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
    """
    organization_id: str = ndb.StringProperty(validator=property_.set_id)
    uid: str = ndb.StringProperty(validator=property_.set_id)
    line_1: str = ndb.StringProperty(default=None, validator=property_.set_string)
    city: str = ndb.StringProperty(default=None, validator=property_.set_string)
    zip_code: str = ndb.StringProperty(default=None, validator=property_.set_string)
    province: str = ndb.StringProperty(default=None, validator=property_.set_string)
    state: str = ndb.StringProperty(default=None, validator=property_.set_string)
    country: str = ndb.StringProperty(default=None, validator=property_.set_string)


    @property
    def address_line(self) -> str:
        return "{} {} {} {} {} {}".format(self.line_1, self.city, self.zip_code,
                                          self.province, self.state, self.country)

    @property
    def address_dict(self) -> dict:
        return {
            "line_1": self.line_1,
            "city": self.city,
            "zip_code": self.zip_code,
            "province": self.province,
            "state": self.state,
            "country": self.country
        }


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

    def __bool__(self) -> bool:
        return bool(self.line_1)


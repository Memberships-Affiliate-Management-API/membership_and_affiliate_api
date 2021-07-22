import typing
from google.api_core.exceptions import RetryError
from google.cloud import ndb
from werkzeug.security import generate_password_hash
from database.mixins import AddressMixin
from utils.utils import timestamp
from database.setters import setters


class UserValidators:
    # Which ever module calls this validators it will provide its own context

    @staticmethod
    def is_user_valid(uid: str) -> typing.Union[None, bool]:
        if not(isinstance(uid, str)) or (uid == ""):
            return False
        try:
            user_instance: UserModel = UserModel.query(UserModel.uid == uid).get()
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        if isinstance(user_instance, UserModel):
            return True
        return False

    @staticmethod
    async def is_user_valid_async(uid: str) -> typing.Union[None, bool]:
        if not(isinstance(uid, str)) or (uid == ""):
            return False
        try:
            user_instance: UserModel = UserModel.query(UserModel.uid == uid).get_async().get_result()
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        if isinstance(user_instance, UserModel):
            return True
        return False


class UserModel(ndb.Model):
    organization_id: str = ndb.StringProperty(required=True, indexed=True, validator=setters.set_id)
    uid: str = ndb.StringProperty(required=True, indexed=True,  validator=setters.set_id)
    names: str = ndb.StringProperty(validator=setters.set_string)
    surname: str = ndb.StringProperty(validator=setters.set_string)
    cell: str = ndb.StringProperty(indexed=True, validator=setters.set_cell)
    email: str = ndb.StringProperty(indexed=True, validator=setters.set_email)
    password: str = ndb.StringProperty(validator=setters.set_password)
    is_active: bool = ndb.BooleanProperty(default=True, validator=setters.set_bool)
    time_registered: int = ndb.IntegerProperty(default=timestamp(), validator=setters.set_number)
    is_admin: bool = ndb.BooleanProperty(default=False, validator=setters.set_bool)
    is_support: bool = ndb.BooleanProperty(default=False, validator=setters.set_bool)
    address: AddressMixin = ndb.StructuredProperty(AddressMixin)

    def __str__(self) -> str:
        return "<User Names: {}, Surname: {}, Email: {}, Cell: {}".format(self.names, self.surname, self.email,
                                                                          self.cell)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.uid != other.uid:
            return False
        if self.email != other.email:
            return False
        return True

    def __len__(self) -> int:
        return len(self.uid)

    def __bool__(self) -> bool:
        # return True if self.transaction_id else False
        return bool(self.uid)

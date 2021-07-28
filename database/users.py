import typing
from google.api_core.exceptions import RetryError
from google.cloud import ndb

from config.exception_handlers import handle_store_errors
from database.mixins import AddressMixin
from utils.utils import timestamp
from database.setters import setters


class UserValidators:
    # Which ever module calls this validators it will provide its own context

    @staticmethod
    @handle_store_errors
    def is_user_valid(uid: str) -> typing.Union[None, bool]:
        if not(isinstance(uid, str)) or (uid == ""):
            return False
        user_instance: UserModel = UserModel.query(UserModel.uid == uid).get()
        if isinstance(user_instance, UserModel):
            return True
        return False

    @staticmethod
    @handle_store_errors
    async def is_user_valid_async(uid: str) -> typing.Union[None, bool]:
        if not(isinstance(uid, str)) or (uid == ""):
            return False
        user_instance: UserModel = UserModel.query(UserModel.uid == uid).get_async().get_result()
        if isinstance(user_instance, UserModel):
            return True
        return False

    @staticmethod
    @handle_store_errors
    def is_user_org_admin(uid: str, organization_id: str) -> typing.Union[None, bool]:
        user_instance: UserModel = UserModel.query(UserModel.uid == uid).get()
        if isinstance(user_instance, UserModel) and user_instance.organization_id == organization_id:
            return user_instance.is_admin
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

    def __bool__(self) -> bool:
        # return True if self.transaction_id else False
        return bool(self.uid)

    def __len__(self) -> int:
        return int(self.__bool__())

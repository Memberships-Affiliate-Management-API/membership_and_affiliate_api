import typing
from google.cloud import ndb
from config.exception_handlers import handle_store_errors
from config.exceptions import InputError, error_codes
from database.mixins import AddressMixin
from utils.utils import timestamp
from database.setters import setters


class UserValidators:
    # Which ever module calls this validators it will provide its own context

    @staticmethod
    @handle_store_errors
    def is_user_valid(organization_id: str, uid: str) -> typing.Union[None, bool]:
        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(
            UserModel.organization_id == organization_id, UserModel.uid == uid).get()

        return user_instance.is_active if isinstance(user_instance, UserModel) else False

    @staticmethod
    @handle_store_errors
    async def is_user_valid_async(organization_id: str, uid: str) -> typing.Union[None, bool]:
        if not(isinstance(uid, str)) or not bool(uid.strip()):
            message: str = "uid cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(
            UserModel.organization_id == organization_id, UserModel.uid == uid).get_async().get_result()

        return user_instance.is_active if isinstance(user_instance, UserModel) else False

    @staticmethod
    @handle_store_errors
    def is_email_available(organization_id: str, email: str) -> typing.Union[None, bool]:
        ***REMOVED***
            return False if email is not available True otherwise
        :param organization_id:
        :param email:
        :return:
        ***REMOVED***
        if not isinstance(email, str) or not bool(email.strip()):
            message: str = "Email cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.email == email).get()
        return not isinstance(user_instance, UserModel)

    @staticmethod
    @handle_store_errors
    def is_cell_available(organization_id: str, cell: str) -> typing.Union[None, bool]:
        ***REMOVED***

        :param organization_id:
        :param cell:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(cell, str) or not bool(cell.strip()):
            message: str = "cell cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.cell == cell).get()

        return not isinstance(user_instance, UserModel)


class UserModel(ndb.Model):
    ***REMOVED***
        UserModel
        TODO if email/account is not verified in 7 days lock the account - by turning active to False
    ***REMOVED***
    organization_id: str = ndb.StringProperty(required=True, indexed=True, validator=setters.set_id)
    uid: str = ndb.StringProperty(required=True, indexed=True,  validator=setters.set_id)
    names: str = ndb.StringProperty(validator=setters.set_string)
    surname: str = ndb.StringProperty(validator=setters.set_string)
    cell: str = ndb.StringProperty(indexed=True, validator=setters.set_cell)
    email: str = ndb.StringProperty(indexed=True, validator=setters.set_email)
    email_verified: bool = ndb.BooleanProperty(default=False, validator=setters.set_bool)
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

    def to_dict(self) -> dict:
        ***REMOVED***
            ensuring that password is not returned when calling to_dict()
        :return: user_instance.to_dict()
        ***REMOVED***
        return {"organization_id": self.organization_id, "uid": self.uid, "names": self.names, "surname": self.surname,
                "cell": self.cell, "email": self.email, "email_verified": self.email_verified,
                "is_active": self.is_active, "time_registered": self.time_registered, "is_admin": self.is_admin,
                "is_support": self.is_support}

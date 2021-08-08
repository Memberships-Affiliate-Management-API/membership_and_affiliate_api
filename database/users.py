***REMOVED***
    **Users Database Module**
    *Class Definitions for Accessing And Management of Users and Clients Data**
***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import typing
from google.cloud import ndb
from config.exception_handlers import handle_store_errors
from config.exceptions import InputError, error_codes
from database.mixins import AddressMixin
from utils.utils import timestamp, get_days
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
        if not (isinstance(uid, str)) or not bool(uid.strip()):
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
        class UserModels allows to store user details to database and also organize the information
        in an easy to use manner

        **Class Properties**

    ***REMOVED***
    organization_id: str = ndb.StringProperty(required=True, indexed=True, validator=setters.set_id)
    uid: str = ndb.StringProperty(required=True, indexed=True, validator=setters.set_id)
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
        return "<User: UID: {}, Names: {}, Surname: {}, Email: {}, Cell: {}".format(self.uid, self.names, self.surname,
                                                                                    self.email, self.cell)

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

    # Properties represents values that can be calculated from present values but will not be stored on database

    @property
    def full_names(self) -> str:
        ***REMOVED***
            represents a users full_names meaning surnames and name together
        :return: users full names
        ***REMOVED***
        return '{} {}'.format(self.names, self.surname)

    @property
    def user_auth(self) -> dict:
        ***REMOVED***
            user authentication provide user uid, email and hashed password
        :return: organization_id, uid, email , password
        ***REMOVED***
        return {
            'organization_id': self.organization_id,
            'uid': self.uid,
            'email': self.email,
            'password': self.password}

    @property
    def account_locked(self) -> bool:
        ***REMOVED***
            checks to see if email is verified if not checks to see if seven days haven't passed since registered
        :return: boolean indicating if the account is locked
        ***REMOVED***
        if self.email_verified:
            return True if (self.time_registered > (timestamp() - get_days(days=7))) else False
        return False

    @property
    def access_rights(self) -> dict:
        ***REMOVED***
            property indicating what a user can and cannot do together with the organization_id and uid
        :return: a dict with a full list of user access_rights
        ***REMOVED***
        return {
            'organization_id': self.organization_id,
            'uid': self.uid,
            'is_admin': self.is_admin,
            'is_support': self.is_support,
            'is_active': self.is_active,
            'email_verified': self.email_verified,
            'account_locked': self.account_locked}

    @property
    def user_details(self) -> dict:
        ***REMOVED***
            user personal details
        :return: user personal details contains organization_id, uid, names, surname, cell, email
        ***REMOVED***
        return {
            'organization_id': self.organization_id,
            'uid': self.uid,
            'names': self.names,
            'surname': self.surname,
            'cell': self.cell,
            'email': self.email}

    @property
    def organization_details(self) -> dict:
        ***REMOVED***
            fetches organization_details belonging to the user
        :return: organization name and description
        ***REMOVED***
        # TODO fetch organization details from an API
        return {
            'organization_name': '',
            'description': ''}

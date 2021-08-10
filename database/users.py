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
from database.setters import property_
from database.basemodel import BaseModel


class UserValidators:
    # Which ever module calls this validators it will provide its own context

    @staticmethod
    @handle_store_errors
    def is_user_valid(organization_id: str, uid: str) -> typing.Union[None, bool]:
        ***REMOVED***
            **is_user_valid**
                returns true if user_instance is found and user_instance.is_active
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(
            UserModel.organization_id == organization_id, UserModel.uid == uid).get()
        # if user_instance is valid return user_instance.is_active
        return bool(user_instance) and user_instance.is_active

    @staticmethod
    @handle_store_errors
    async def is_user_valid_async(organization_id: str, uid: str) -> typing.Union[None, bool]:
        ***REMOVED***
            **is_user_valid_async**
                returns true if user_instance is valid and user_instance.is_active
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        if not (isinstance(uid, str)) or not bool(uid.strip()):
            message: str = "uid cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(
            UserModel.organization_id == organization_id, UserModel.uid == uid).get_async().get_result()

        # if user_instance is valid return user_instance.is_active
        return bool(user_instance) and user_instance.is_active

    @staticmethod
    @handle_store_errors
    def is_email_available(organization_id: str, email: str) -> typing.Union[None, bool]:
        ***REMOVED***
            **is_email_available**
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

        # returns False if user_instance is a valid User
        return not bool(user_instance)

    @staticmethod
    @handle_store_errors
    def is_cell_available(organization_id: str, cell: str) -> typing.Union[None, bool]:
        ***REMOVED***
            **is_cell_available**
                checks if cell is available returns true if that's the case
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
        # Returns False if user_instance is a valid user
        return not bool(user_instance)


class UserModel(BaseModel):
    ***REMOVED***
        Documentation
            `Class UserModel`
                1. class UserModels allows to store user details to database and also organize the information in an
                easy to use manner

        **Class Properties**
            1. organization_id : organization the user belongs to
            2. uid: the user id to identify the presentation
            3. names: names of user
            4. surname: surname of user
            5. cell: users cell number must be in international format
            6. email: users email when email is verified email_verified will be True
            7. email_verified: boolean value indicating if the users email has been verified
            8. password: a string representing the password, the property will hash the password before storing it through the setter method
            9. is_active: indicates if the user is active
            10. time_registered: the time in timestamp (milliseconds) the user has been registered
            11. is_admin: indicates if user is admin user - this relates to the organization the user is registered in
            12. is_support: indicates if user is a support user
            13. address: users address see address mixin in mixins

        **Property Methods**
            1. full_names: returns full names for the user which is names and surnames
            2. user_auth: returns fields in dict relating to user authentication i.e organization_id, uid, email , password
            3. account_locked: boolean ->  indicates if user account has been locked due to the account email not being verified
            4. access_rights: dict -> values indicates what access type the user has relating to their organization
            5. user_details: dict -> user general details in dict form

    ***REMOVED***
    organization_id: str = ndb.StringProperty(required=True, indexed=True, validator=property_.set_id)
    uid: str = ndb.StringProperty(required=True, indexed=True, validator=property_.set_id)
    names: str = ndb.StringProperty(validator=property_.set_string)
    surname: str = ndb.StringProperty(validator=property_.set_string)
    cell: str = ndb.StringProperty(indexed=True, validator=property_.set_cell)
    email: str = ndb.StringProperty(indexed=True, validator=property_.set_email)
    email_verified: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)
    password: str = ndb.StringProperty(validator=property_.set_password)
    is_active: bool = ndb.BooleanProperty(default=True, validator=property_.set_bool)
    time_registered: int = ndb.IntegerProperty(default=timestamp(), validator=property_.set_number)
    is_admin: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)
    is_support: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)
    address: AddressMixin = ndb.StructuredProperty(AddressMixin)

    def __str__(self) -> str:
        return "<User: UID: {}, Names: {}, Surname: {}, Email: {}, Cell: {}".format(self.uid, self.names, self.surname,
                                                                                    self.email, self.cell)

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
            checks to see if email is verified if yes checks to see if seven days haven't passed since registered
        :return: boolean indicating if the account is locked
        ***REMOVED***
        return self.email_verified and (self.time_registered > (timestamp() - get_days(days=7)))

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

    def to_dict(self, include=all, exclude=None) -> dict:
        # excluding password from dict
        exclude: typing.List[str] = ['password']
        return super().to_dict(include=include, exclude=exclude)



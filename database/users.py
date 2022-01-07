"""
    **Users Database Module**
    *Class Definitions for Accessing And Management of Users and Clients Data**
"""

__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

import typing
from typing import Optional, List
from datetime import date
from google.cloud import ndb
from config.exception_handlers import handle_store_errors
from config.exceptions import InputError, error_codes
from database.mixins import AddressMixin
from utils.utils import timestamp, get_days_in_milliseconds
from database.setters import property_
from database.basemodel import BaseModel


class UserValidators:
    # Which ever module calls this validators it will provide its own context

    @staticmethod
    @handle_store_errors
    def is_user_valid(organization_id: str, uid: str) -> Optional[bool]:
        """
            **is_user_valid**
                returns true if user_instance is found and user_instance.is_active
        :param organization_id:
        :param uid:
        :return:
        """
        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id cannot be Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(
            UserModel.organization_id == organization_id, UserModel.uid == uid).get()
        # if user_instance is valid return user_instance.is_active
        return bool(user_instance) and user_instance.is_active

    @staticmethod
    @handle_store_errors
    async def is_user_valid_async(organization_id: str, uid: str) -> Optional[bool]:
        """
            **is_user_valid_async**
                returns true if user_instance is valid and user_instance.is_active
        :param organization_id:
        :param uid:
        :return:
        """
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
    def is_email_available(organization_id: str, email: str) -> Optional[bool]:
        """
            **is_email_available**
                return False if email is not available True otherwise
        :param organization_id:
        :param email:
        :return:
        """
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
    def is_cell_available(organization_id: str, cell: str) -> Optional[bool]:
        """
            **is_cell_available**
                checks if cell is available returns true if that's the case
        :param organization_id:
        :param cell:
        :return:
        """
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
    """
        **Documentation**
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

    """
    organization_id: str = ndb.StringProperty(default=None, required=True, indexed=True, validator=property_.set_id)
    uid: str = ndb.StringProperty(default=None, required=True, indexed=True, validator=property_.set_id)
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
    recovery_code: str = ndb.StringProperty(validator=property_.set_string)
    last_login_date: date = ndb.DateProperty(validator=property_.set_date)

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
        # return True if self.uid else False
        return bool(self.uid) and bool(self.organization_id)

    @ndb.model.ComputedProperty
    def full_names(self) -> str:
        """
            **property -> full_names**
                represents a users full_names meaning surnames and name together

        :return: {names}{surname}
        """
        return f'{self.names} {self.surname}'

    @ndb.model.ComputedProperty
    def user_auth(self) -> dict:
        """
            **property user_auth**
                user authentication provide user uid, email and hashed password

        :return: dict -> organization_id, uid, email , password
        """
        return {
            'organization_id': self.organization_id,
            'uid': self.uid,
            'email': self.email,
            'password': self.password}

    @ndb.model.ComputedProperty
    def account_locked(self) -> bool:
        """
            **property account_locked**
                checks to see if email is verified if yes checks to see if seven days haven't passed since registered

        :return: boolean indicating if the account is locked
        """
        return self.email_verified and (self.time_registered > (timestamp() - get_days_in_milliseconds(days=7)))

    @ndb.model.ComputedProperty
    def access_rights(self) -> dict:
        """
            **property access_rights**
                property indicating what a user can and cannot do together with the organization_id and uid

        :return: dict -> organization_id, uid, is_admin, is_active, email_verified, account_locked
        """
        return {
            'organization_id': self.organization_id,
            'uid': self.uid,
            'is_admin': self.is_admin,
            'is_support': self.is_support,
            'is_active': self.is_active,
            'email_verified': self.email_verified,
            'account_locked': self.account_locked}

    @ndb.model.ComputedProperty
    def user_details(self) -> dict:
        """
            **property user_details**
                user personal details
        :return: dict -> organization_id, uid, names, surname, cell, email
        """
        return {
            'organization_id': self.organization_id,
            'uid': self.uid,
            'names': self.names,
            'surname': self.surname,
            'cell': self.cell,
            'email': self.email}

    @ndb.model.ComputedProperty
    def organization_details(self) -> dict:
        """
            **property organization_details**
                fetches organization_details belonging to the user
        :return: organization name and description
        """
        # TODO fetch organization details from an API
        return {
            'organization_name': '',
            'description': ''}

    def to_dict(self, include: Optional[List[str]] = None, exclude: Optional[List[str]] = None) -> dict:
        """
            **to_dict method**
                returns a full dict representing user except password property

        :param include: all
        :param exclude: password
        :return: dict -> all user properties excluding password
        """

        exclude: List[str] = ['password']
        return super().to_dict(include=include, exclude=exclude)


class GithubUser(BaseModel):
    """
        used to stored login with github client details
    """
    uid: str = ndb.StringProperty(default=None, required=True, validator=property_.set_id)
    organization_id: str = ndb.StringProperty(default=None, required=True, validator=property_.set_id)
    # TODO - May need to exclude access_token from to_dict results
    access_token: str = ndb.StringProperty(default=None, required=True, validator=property_.set_string)
    email: str = ndb.StringProperty(required=True, validator=property_.set_email)
    twitter_username: str = ndb.StringProperty(validator=property_.set_string)
    github_name: str = ndb.StringProperty(required=True, validator=property_.set_string)
    avatar_url: str = ndb.StringProperty(required=True, validator=property_.set_domain)
    api_url: str = ndb.StringProperty(required=True, validator=property_.set_domain)
    html_url: str = ndb.StringProperty(required=True, validator=property_.set_domain)
    followers_url: str = ndb.StringProperty(required=True, validator=property_.set_domain)
    following_url: str = ndb.StringProperty(required=True, validator=property_.set_domain)
    gists_url: str = ndb.StringProperty(required=True, validator=property_.set_domain)
    repos_url: str = ndb.StringProperty(required=True, validator=property_.set_domain)
    is_deleted: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)

    def __eq__(self, other) -> bool:
        if not super().__eq__(other):
            return False

        if self.uid != other.uid:
            return False
        if self.email != other.email:
            return False
        if self.html_url != other.html_url:
            return False
        return True

    def __str__(self) -> str:
        return "<GitHubUser uid: {}, email: {}, twitter: {}, github_name: {}, avatar_url: {}, html_url: {}".format(
            self.uid, self.email, self.twitter_username, self.github_name, self.avatar_url, self.html_url)

    def __bool__(self) -> bool:
        return bool(self.uid) and bool(self.organization_id) and bool(self.access_token)


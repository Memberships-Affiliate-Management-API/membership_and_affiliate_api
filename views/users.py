"""
    ** Module UserView Controller**
    classes used to manage:
        registering new users for both the client and main app
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from typing import Optional, List
from flask import jsonify, current_app
from google.cloud import ndb
from werkzeug.security import check_password_hash
from _sdk._email import Mailgun
from config.exceptions import (error_codes, status_codes, InputError, UnAuthenticatedError,
                               DataServiceError, RequestError)
from database.mixins import AddressMixin
from database.organization import OrgValidators

from database.users import UserModel, UserValidators
from security.users_authenticator import encode_auth_token
from utils.utils import create_id, return_ttl
from config.exception_handlers import handle_view_errors
from config.use_context import use_context
from cache.cache_manager import app_cache


# noinspection DuplicatedCode
class UserEmails(Mailgun):
    """
        **Class UserEmails**
            used to send emails and notifications to users
    """

    def __init__(self) -> None:
        """
           NOTE: initializing mail gun rest api
        """
        super(UserEmails, self).__init__()

    def send_welcome_to_admins_email(self, organization_id: str, uid: str) -> None:
        """
            **send_welcome_to_admins_email**
                send an email to admin welcoming him to the admins club
                NOTE: class __do_send_mail with the finally composed email

        :param uid:
        :param organization_id:
        :return:
        """
        user_data, organization_data = self.return_organization_user(organization_id=organization_id, uid=uid)
        email_verified: bool = user_data.get('email_verified')
        subject: str = f"{organization_data.get('organization_name')} Welcome to to Admins"

        text: str = f'''
        hi {user_data.get('names', " ")} {user_data.get('surname', " ")}
        you have been successfully registered as an administrator of {organization_data.get('organization_name')}
        
        Please contact fellow admins @ {organization_data.get('home_url')} 
        to find out what your responsibilities entails 
        
        Thank You
        {organization_data.get('organization_name')}        
        '''

        html: str = f'''
        <h3>hi {user_data.get('names', " ")} {user_data.get('surname', " ")}</h3>
        <p>you have been successfully registered as an administrator of {organization_data.get('organization_name')}</p>
        
        <p>Please contact fellow admins @ {organization_data.get('home_url')} 
        to find out what your responsibilities entails</p> 
        
        <h4>Thank You</h4>
        <strong>{organization_data.get('organization_name')}</strong>                    
        '''
        if email_verified:
            self._do_schedule_mail(to_email=user_data.get('email'), subject=subject, text=text, html=html)

        message: str = "Bad Request Error: Email not verified please verify your account"
        raise RequestError(status=error_codes.bad_request_error_code, description=message)

    def send_goodbye_admin_email(self, organization_id: str, uid: str) -> None:
        """
            **send_goodbye_admin_email**
                send an email informing the user he or she is no longer admin

        :param uid:
        :param organization_id:
        :return:
        """
        user_data, organization_data = self.return_organization_user(organization_id=organization_id, uid=uid)
        email_verified: bool = user_data.get('email_verified')

        subject: str = f"{organization_data.get('organization_name')} You are not longer admin"
        text: str = f'''
        hi {user_data.get('names', " ")} {user_data.get('surname', " ")}
        you are no longer an admin of  {organization_data.get('organization_name')}

        Please contact fellow admins @ {organization_data.get('home_url')} 
        to find out why that is the case 

        Thank You
        {organization_data.get('organization_name')}        
        '''

        html: str = f'''
        <h3>hi {user_data.get('names', " ")} {user_data.get('surname', " ")}</h3>
        <p>you are no longer an admin of  {organization_data.get('organization_name')}</p>

        <p>Please contact fellow admins @ {organization_data.get('home_url')} 
        to find out why that is the case</p> 

        <h4>Thank You</h4>
        <strong>{organization_data.get('organization_name')}</strong>        
        '''
        if email_verified:
            self._do_schedule_mail(to_email=user_data.get('email'), subject=subject, text=text, html=html)

        message: str = "Bad Request Error: Email not verified please verify your account"
        raise RequestError(status=error_codes.bad_request_error_code, description=message)

    def send_welcome_to_support_email(self, organization_id: str, uid: str) -> None:
        """
            **send_welcome_to_support_email**
                send welcome to support email when users joins the support staff

        :param uid:
        :param organization_id:
        :return:
        """
        user_data, organization_data = self.return_organization_user(organization_id=organization_id, uid=uid)
        email_verified: bool = user_data.get('email_verified')

        subject: str = f"{organization_data.get('organization_name')} Welcomes you to its support team"
        text: str = f'''
        hi {user_data.get('names', " ")} {user_data.get('surname', " ")}
        You are a member of the support team of : {organization_data.get('organization_name')}

        Please contact fellow support members  @ {organization_data.get('home_url')} 
        for more information on how to proceed.        

        Thank You
        {organization_data.get('organization_name')}        
        '''

        html: str = f'''
        <h3>hi {user_data.get('names', " ")} {user_data.get('surname', " ")}</h3>
        <p>You are a member of the support team of : {organization_data.get('organization_name')}</p>

        <p>Please contact fellow support members  @ {organization_data.get('home_url')} 
        for more information on how to proceed.</p>        

        <h4>Thank You</h4>
        <strong>{organization_data.get('organization_name')}</strong>        
        '''
        if email_verified:
            self._do_schedule_mail(to_email=user_data.get('email'), subject=subject, text=text, html=html)

        message: str = "Bad Request Error: Email not verified please verify your account"
        raise RequestError(status=error_codes.bad_request_error_code, description=message)

    def send_goodbye_support_email(self, organization_id: str, uid: str) -> None:
        """
            **send_goodbye_support_email**
                used to send emails when users are no longer part of the support roles

        :param uid:
        :param organization_id:
        :return:
        """
        user_data, organization_data = self.return_organization_user(organization_id=organization_id, uid=uid)
        email_verified: bool = user_data.get('email_verified')

        subject: str = f"{organization_data.get('organization_name')} You are not longer a member of our support team"
        text: str = f'''
        hi {user_data.get('names', " ")} {user_data.get('surname', " ")}
        You are no longer a member of the support team of : {organization_data.get('organization_name')}

        Please contact fellow support members  @ {organization_data.get('home_url')} 
        for more information on how to proceed.        

        Thank You
        {organization_data.get('organization_name')}        
        '''

        html: str = f'''
        <h3>hi {user_data.get('names', " ")} {user_data.get('surname', " ")}</h3>
        <p>You are no longer a member of the support team of : {organization_data.get('organization_name')}</p>

        <p>Please contact fellow support members  @ {organization_data.get('home_url')} 
        for more information on how to proceed.</p>        

        <h4>Thank You</h4>
        <strong>{organization_data.get('organization_name')}</strong>        
        '''
        if email_verified:
            self._do_schedule_mail(to_email=user_data.get('email'), subject=subject, text=text, html=html)

        message: str = "Bad Request Error: Email not verified please verify your account"
        raise RequestError(status=error_codes.bad_request_error_code, description=message)

    def send_recovery_email(self, organization_id: Optional[str], uid: Optional[str], recovery_code: str) -> None:
        """
            **send_recovery_email**
                send an email informing the user a recovery action has been activated on their account

        :param uid:
        :param organization_id:
        :param recovery_code
        :return:
        """
        user_data, organization_data = self.return_organization_user(organization_id=organization_id, uid=uid)

        # NOTE during password recovery the link display should fit the look of the user of the api
        email_verified: bool = user_data.get('email_verified')

        _url: str = organization_data.get('recovery_callback_url', self._base_url + 'password-reset')
        # NOTE splitting the forward slash if url endswith forward slash
        _url = _url[:-1] if _url.endswith("/") else _url

        password_reset_link: str = f"{_url}/{recovery_code}"
        subject = f"{organization_data.get('organization_name')} Please reset your password"
        text: str = f'''
         Hi {user_data.get('names', " ")} {user_data.get('surname', " ")}
        
         You are receiving this email because you requested
         a password reset please click on the following link to reset your password 
         
         {password_reset_link}
         
         if you did not make this request please ignore this email
         
         Thank You
         {organization_data.get('organization_name')}
         '''
        html: str = f'''
         <h3>Hi {user_data.get('names', " ")} {user_data.get('surname', " ")}</h3>
         
         <p>You are receiving this email because you requested
         a password reset please click on the following link to reset your password</p>
          
         <p><a class='btn' href="{password_reset_link}">password reset link</a></p>

         if you did not make this request please ignore this email
         
         <h4>Thank You</h4>
         <strong>{organization_data.get('organization_name')}</strong>             
         '''
        if email_verified:
            self._do_schedule_mail(to_email=user_data.get('email'), subject=subject, text=text, html=html)

        message: str = "Bad Request Error: Email not verified please verify your account"
        raise RequestError(status=error_codes.bad_request_error_code, description=message)


class Validators(UserValidators, OrgValidators):
    """
        User Validators
    """

    def __init__(self) -> None:
        super(Validators, self).__init__()
        self._max_retries: int = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout: int = current_app.config.get('DATASTORE_TIMEOUT')

    @staticmethod
    def check_required(organization_id: Optional[str], email: Optional[str],
                       cell: Optional[str]) -> None:
        """
            check organization_id email and cell if they are valid
        :param organization_id:
        :param email:
        :param cell:
        :return:
        """

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(email, str) or not bool(email.strip()):
            message: str = "email is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(cell, str) or not bool(cell.strip()):
            message: str = "cell is required"
            raise InputError(status=error_codes.input_error_code, description=message)

    @staticmethod
    def check_org_and_uid(organization_id: Optional[str], uid: Optional[str]) -> None:
        """
            check if organization_id or uid are available if not throw input_error_code and exit
        :param organization_id:
        :param uid:
        :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

    def can_add_user(self, organization_id: Optional[str], email: Optional[str],
                     cell: Optional[str]) -> bool:
        """
            if this returns true the user can be added

            :param email: required - check if email is available to be used on this organization
            :param cell: required - check if the cell number related to this user is not already registered for another user
            :param organization_id: required - check if user has logged into this organization
            :return: boolean indicate if the user can be added or not
        """
        is_organization_exist: Optional[bool] = self.is_organization_exist(organization_id=organization_id)
        # is_user_valid: Optional[bool] = self.is_user_valid(organization_id=organization_id, uid=uid)
        is_email_valid: Optional[bool] = self.is_email_available(organization_id=organization_id, email=email)
        is_cell_available: Optional[bool] = self.is_cell_available(organization_id=organization_id, cell=cell)

        if isinstance(is_organization_exist, bool) and isinstance(is_email_valid, bool) and \
                isinstance(is_cell_available, bool):
            return is_organization_exist and is_email_valid and is_cell_available

        message: str = '''Database Error: unable to check the validity of your input due to database 
        errors try again later'''
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)


# TODO create test cases for User View and Documentations
# noinspection DuplicatedCode
class UserView(Validators, UserEmails):
    """
        User-View handling business logic for UserModel
    """

    def __init__(self) -> None:
        super(UserView, self).__init__()

    @staticmethod
    def __delete_user_cache(organization_id, uid, user_instance):
        cell: str = user_instance.cell
        email: str = user_instance.email
        _kwargs: dict = dict(user_view=UserView, organization_id=organization_id, uid=uid, email=email, cell=cell)
        app_cache._schedule_cache_deletion(func=app_cache._delete_user_cache, kwargs=_kwargs)

    @staticmethod
    def __delete_user(organization_id: str, uid: str, user_instance: UserModel):
        UserView.__delete_user_cache(organization_id, uid, user_instance)
        # TODO- rather mark user as deleted
        user_instance.key.delete()
        return jsonify(dict(status=True,
                            payload=user_instance.to_dict(),
                            message='successfully deleted user')), status_codes.successfully_updated_code

    @staticmethod
    def is_user(user_instance: Optional[UserModel], _uid: str) -> bool:
        return isinstance(user_instance, UserModel) and user_instance.uid == _uid

    def _create_unique_uid(self) -> str:
        _uid = create_id()
        user_instance: UserModel = UserModel.query(UserModel.uid == _uid).get()
        return self._create_unique_uid() if self.is_user(user_instance=user_instance, _uid=_uid) else _uid

    # TODO - note that user manipulations invalidates organizations cache

    # ----------------------------------------Main API Functions------------------------->
    @use_context
    @handle_view_errors
    def add_user(self, organization_id: Optional[str], names: Optional[str],
                 surname: Optional[str], cell: Optional[str], email: Optional[str],
                 password: Optional[str], uid: Optional[str] = None) -> tuple:
        """
            **add_user**
                Register a new User
                this is called for registering a new user
            :param organization_id:
            :param names:
            :param surname:
            :param cell:
            :param email:
            :param password:
            :param uid: Optional gets to be used if client is using an external Oauth Service
            :return: returns user record
        """
        # Check if all required values are present if not throw inputError and exit
        self.check_required(organization_id=organization_id, email=email, cell=cell)

        if not self.can_add_user(organization_id=organization_id, email=email, cell=cell):
            message: str = 'Error Adding User: could be that the user already exist, please login or check your input'
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            # This is a new user who has not created a uid from another login service - create a unique uid
            uid = self._create_unique_uid()

        if not isinstance(names, str) or not bool(names.strip()):
            message: str = 'names are required'
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(surname, str) or not bool(surname.strip()):
            message: str = 'surname is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(password, str) or not bool(password.strip()):
            message: str = 'password is required boss'
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel(organization_id=organization_id, uid=uid, names=names,
                                             surname=surname, cell=cell, email=email, password=password,
                                             is_active=True)

        key = user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not isinstance(key, ndb.Key):
            message: str = "Unable to save database"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        _kwargs: dict = dict(user_view=UserView, organization_id=organization_id, uid=uid, email=email, cell=cell)
        app_cache._schedule_cache_deletion(func=app_cache._delete_user_cache, kwargs=_kwargs)
        message: str = "successfully created new user"
        return jsonify(dict(status=True,
                            payload=user_instance.to_dict(),
                            message=message)), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    async def add_user_async(self, organization_id: Optional[str], names: Optional[str], surname: Optional[str],
                             cell: Optional[str], email: Optional[str],
                             password: Optional[str], uid: Optional[str] = None) -> tuple:
        """
        **add_user_async**
            creates a new user asynchronously - all parameters are required

        :param organization_id:
        :param names:
        :param surname:
        :param cell:
        :param email:
        :param password:
        :param uid:
        :return:
        """
        # Check if all required values are present if not throw inputError and exit
        # TODO- use async version
        self.check_required(organization_id=organization_id, email=email, cell=cell)

        # TODO- use async version
        if not self.can_add_user(organization_id=organization_id, email=email, cell=cell):
            message: str = "You are not authorized to create a user record in this organization"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            uid = self._create_unique_uid()

        user_instance: UserModel = UserModel(organization_id=organization_id, uid=uid, names=names, surname=surname,
                                             cell=cell, email=email, password=password, is_active=True)

        key = user_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
        if not isinstance(key, ndb.Key):
            message: str = "Unable to save user database"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        _kwargs: dict = dict(user_view=UserView, organization_id=organization_id, uid=uid, email=email, cell=cell)
        app_cache._schedule_cache_deletion(func=app_cache._delete_user_cache, kwargs=_kwargs)
        message: str = "successfully created new user"
        return jsonify(dict(status=True,
                            payload=user_instance.to_dict(),
                            message=message)), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def update_user(self, organization_id: Optional[str], uid: Optional[str],
                    names: Optional[str], surname: Optional[str],
                    cell: Optional[str], email: Optional[str], is_admin: bool,
                    is_support: bool) -> tuple:
        """
                update user details all fields are required -
                if the purpose is to update only one of the fields use one of the specialized methods
            :param organization_id:
            :param uid:
            :param names:
            :param surname:
            :param cell:
            :param email:
            :param is_admin:
            :param is_support:
        :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "User ID is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()

        if not isinstance(user_instance, UserModel) and bool(user_instance):
            message: str = 'user not found cannot update user details'
            return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

        user_instance.names = names
        user_instance.surname = surname
        user_instance.cell = cell
        user_instance.email = email
        user_instance.is_admin = is_admin
        user_instance.is_support = is_support
        key = user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not isinstance(key, ndb.Key):
            message: str = "Unable to save user database"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        _kwargs: dict = dict(user_view=UserView, organization_id=organization_id, uid=uid, email=email, cell=cell)
        app_cache._schedule_cache_deletion(func=app_cache._delete_user_cache, kwargs=_kwargs)

        message: str = "Successfully updated user details"
        return jsonify(dict(status=True,
                            payload=user_instance.to_dict(),
                            message=message)), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    async def update_user_async(self, organization_id: Optional[str], uid: Optional[str],
                                names: Optional[str], surname: Optional[str],
                                cell: Optional[str], email: Optional[str],
                                is_admin: bool, is_support: bool) -> tuple:
        """
            update user details asynchronously
        :param organization_id:
        :param uid:
        :param names:
        :param surname:
        :param cell:
        :param email:
        :param is_admin:
        :param is_support:
        :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "User ID is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get_async().get_result()
        if not (isinstance(user_instance, UserModel) and bool(user_instance)):
            message: str = "User not found: Unable to update user details"
            return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

        user_instance.names = names
        user_instance.surname = surname
        user_instance.cell = cell
        user_instance.email = email
        user_instance.is_admin = is_admin
        user_instance.is_support = is_support
        key = user_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
        if not isinstance(key, ndb.Key):
            message: str = "Unable to save user database"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        _kwargs: dict = dict(user_view=UserView, organization_id=organization_id, uid=uid, email=email, cell=cell)
        app_cache._schedule_cache_deletion(func=app_cache._delete_user_cache, kwargs=_kwargs)

        message: str = "Successfully updated user details"
        return jsonify(dict(status=True,
                            payload=user_instance.to_dict(),
                            message=message)), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def update_user_names(self, organization_id: Optional[str], uid: Optional[str],
                          names: Optional[str], surname: Optional[str]) -> tuple:
        """
            given organization_id and uid update names
        :param organization_id: required
        :param uid: required
        :param names: optional
        :param surname: optional
        :return:
        """
        # checks if organization_id and uid are available if not throws input Error
        self.check_org_and_uid(organization_id=organization_id, uid=uid)

        if not isinstance(names, str) or not bool(names.strip()):
            message: str = "names is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(surname, str) or not bool(surname.strip()):
            message: str = "surname is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()
        if not isinstance(user_instance, UserModel) and bool(user_instance):
            message: str = "User not found: Unable to update names"
            return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

        user_instance.names = names
        user_instance.surname = surname
        key = user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not isinstance(key, ndb.Key):
            message: str = "Database Error: unable to update names"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        self.__delete_user_cache(organization_id, uid, user_instance)

        message: str = "Successfully updated user names"
        return jsonify(dict(status=True,
                            payload=user_instance.to_dict(),
                            message=message)), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def update_cell(self, organization_id: Optional[str], uid: Optional[str],
                    cell: Optional[str]) -> tuple:
        """
                given organization_id and uid update cell number
            :param organization_id:
            :param uid:
            :param cell:
            :return:
        """
        self.check_org_and_uid(organization_id=organization_id, uid=uid)
        if not isinstance(cell, str) or not bool(cell.strip()):
            message: str = "cell is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()
        if not isinstance(user_instance, UserModel) and bool(user_instance):
            message: str = "User Record not found: Unable to update cell number"
            return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

        old_cell: str = user_instance.cell
        user_instance.cell = cell
        # TODO - run a function to send verification sms if available_funds
        key = user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not isinstance(key, ndb.Key):
            message: str = "Database Error: unable to save updated user record"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        # Note that the old cache needs to be removed as it has now an entry relating to the old cell
        cell: str = old_cell
        email: str = user_instance.email
        _kwargs: dict = dict(user_view=UserView, organization_id=organization_id, uid=uid, email=email, cell=cell)
        app_cache._schedule_cache_deletion(func=app_cache._delete_user_cache, kwargs=_kwargs)

        message: str = "Successfully Updated Cell Number"
        return jsonify(dict(status=True,
                            payload=user_instance.to_dict(),
                            message=message)), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def update_email(self, organization_id: Optional[str], uid: Optional[str],
                     email: Optional[str]) -> tuple:
        """
         update user email given organization_id and uid
        :param organization_id:
        :param uid:
        :param email:
        :return:
        """
        self.check_org_and_uid(organization_id=organization_id, uid=uid)
        if not isinstance(email, str) or not bool(email.strip()):
            message: str = "Email is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()
        if not isinstance(user_instance, UserModel) and bool(user_instance):
            message: str = "Unable to find User record: Email not updated"
            return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

        if user_instance.email == email:
            message: str = "Email is already upto-date"
            return jsonify({'status': True, 'payload': user_instance.to_dict(),
                            'message': message}), status_codes.status_ok_code

        old_email: str = user_instance.emai
        user_instance.email = email
        # TODO send verification email and mark email as not verified
        key = user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not isinstance(key, ndb.Key):
            message: str = "Database Error: Unable to update user record"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        cell: str = user_instance.cell
        email: str = old_email
        _kwargs: dict = dict(user_view=UserView, organization_id=organization_id, uid=uid, email=email,
                             cell=cell)
        app_cache._schedule_cache_deletion(func=app_cache._delete_user_cache, kwargs=_kwargs)

        message: str = "Successfully Updated Email Record please check your email inbox for verification email"
        return jsonify(dict(status=True,
                            payload=user_instance.to_dict(),
                            message=message)), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def update_password(self, organization_id: Optional[str], uid: Optional[str],
                        password: Optional[str], new_password: Optional[str]) -> tuple:
        """
            update password given  organization_id and uid update password
            check if old password matches the present password if that's the case then
            update the password
        :param organization_id:
        :param uid:
        :param password:
        :param new_password:
        :return:
        """
        self.check_org_and_uid(organization_id=organization_id, uid=uid)

        if not isinstance(password, str) or not bool(password.strip()):
            message: str = "password is required"
            raise InputError(status=error_codes.input_error_code, description=message)
        if not isinstance(new_password, str) or not bool(new_password.strip()):
            message: str = "new Password is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()

        if not isinstance(user_instance, UserModel) and bool(user_instance):
            message: str = "User Record not found: Unable to update password"
            return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

        # Note: checking if old password is equal to the password on file
        if not check_password_hash(password=password, pwhash=user_instance.password):
            message: str = "Passwords do not match - please try again"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        user_instance.password = new_password
        key = user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not isinstance(key, ndb.Key):
            message: str = "Database Error: unable to update password"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        self.__delete_user_cache(organization_id, uid, user_instance)

        # TODO - logoff the user
        message: str = "Successfully Updated Password - please login again"
        return jsonify({'status': True,
                        'payload': user_instance.to_dict(),
                        'message': message}), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def set_is_admin(self, organization_id: Optional[str], uid: Optional[str],
                     is_admin: Optional[bool] = False) -> tuple:
        """
            given organization_id and uid update is_admin
        :param organization_id:
        :param uid:
        :param is_admin:
        :return:
        """
        self.check_org_and_uid(organization_id=organization_id, uid=uid)
        if not isinstance(is_admin, bool):
            message: str = "is_admin is required and can only be a boolean"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()
        if not isinstance(user_instance, UserModel) and bool(user_instance):
            message: str = "User Record not found: Unable to update admin"
            return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

        user_instance.is_admin = is_admin
        key = user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not isinstance(key, ndb.Key):
            message: str = "Database Error: Unable to update user admin status"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        if is_admin:
            self.send_welcome_to_admins_email(organization_id=organization_id, uid=uid)
        else:
            self.send_goodbye_admin_email(organization_id=organization_id, uid=uid)

        self.__delete_user_cache(organization_id, uid, user_instance)

        message: str = "Successfully Update admin status"
        return jsonify(dict(status=True,
                            payload=user_instance.to_dict(),
                            message=message)), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def set_is_support(self, organization_id: Optional[str], uid: Optional[str],
                       is_support: Optional[bool]) -> tuple:
        """
            given organization_id and uid set support role
        :param organization_id:
        :param uid:
        :param is_support:
        :return:
        """
        self.check_org_and_uid(organization_id=organization_id, uid=uid)
        if not isinstance(is_support, bool):
            message: str = "is_support is required and can only be a boolean"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()
        if not isinstance(user_instance, UserModel) and bool(user_instance):
            message: str = "User Record not found: Unable to update support"
            return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

        user_instance.is_support = is_support
        key = user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not isinstance(key, ndb.Key):
            message: str = "Database Error: Unable to update user support status"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        if is_support:
            self.send_welcome_to_support_email(organization_id=organization_id, uid=uid)
        else:
            self.send_goodbye_support_email(organization_id=organization_id, uid=uid)

        self.__delete_user_cache(organization_id, uid, user_instance)

        message: str = "Successfully Update support status"
        return jsonify(dict(status=True,
                            payload=user_instance.to_dict(),
                            message=message)), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def set_address(self, organization_id: Optional[str], uid: Optional[str],
                    address_dict: Optional[dict]) -> tuple:
        """
            given organization_id and uid with address_dict update address
        :param organization_id:
        :param uid:
        :param address_dict:
        :return:
        """

        self.check_org_and_uid(organization_id=organization_id, uid=uid)

        line_1: Optional[str] = address_dict.get('line_1')
        if not isinstance(line_1, str) or not bool(line_1.strip()):
            message: str = "line_1 is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        city: Optional[str] = address_dict.get('city')
        if not isinstance(city, str) or not bool(city.strip()):
            message: str = "city is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        zip_code: Optional[str] = address_dict.get('zip_code')
        if not isinstance(zip_code, str) or not bool(zip_code.strip()):
            message: str = "zip_code is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        province: Optional[str] = address_dict.get('province')
        state: Optional[str] = address_dict.get('state')

        if not isinstance(province, str) and not isinstance(state, str):
            message: str = "choose either state or province for your country not both"
            raise InputError(status=error_codes.input_error_code, description=message)

        country: Optional[str] = address_dict.get('country')
        if not isinstance(country, str) or not bool(country.strip()):
            message: str = "country is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()
        if not isinstance(user_instance, UserModel) and bool(user_instance):
            message: str = "User Not Found: Unable to update address"
            return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

        address_instance = AddressMixin(organization_id=organization_id, uid=uid, line_1=line_1, city=city,
                                        zip_code=zip_code, province=province, state=state, country=country)
        address_instance.put()
        user_instance.address = address_instance
        user_key = user_instance.put()
        if not isinstance(user_key, ndb.Key):
            message: str = "Database Error: unable to update user"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        self.__delete_user_cache(organization_id, uid, user_instance)
        message: str = "Successfully updated user address"
        return jsonify(dict(status=True,
                            payload=user_instance.to_dict(),
                            message=message)), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def delete_user(self, organization_id: Optional[str], uid: Optional[str] = None,
                    email: Optional[str] = None, cell: Optional[str] = None) -> tuple:
        """
            given either, uid, email or cell delete user
            :param organization_id:
            :param uid:
            :param email:
            :param cell:
            :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if isinstance(uid, str) and bool(uid.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.uid == uid).get()
            if isinstance(user_instance, UserModel) and bool(user_instance):
                return self.__delete_user(organization_id, uid, user_instance)

        elif isinstance(email, str) and bool(email.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.email == email).get()
            if isinstance(user_instance, UserModel) and bool(user_instance):
                return self.__delete_user(organization_id, uid, user_instance)

        elif isinstance(cell, str) and bool(cell.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.cell == cell).get()
            if isinstance(user_instance, UserModel) and bool(user_instance):
                return self.__delete_user(organization_id, uid, user_instance)

        return jsonify(dict(status=False, message='User not found')), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    async def delete_user_async(self, organization_id: Optional[str], uid: Optional[str] = None,
                                email: Optional[str] = None, cell: Optional[str] = None) -> tuple:
        """
            given either, uid, email or cell delete user
            :param organization_id:
            :param uid:
            :param email:
            :param cell:
            :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if isinstance(uid, str) and bool(uid.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.uid == uid).get_async().get_result()
            if isinstance(user_instance, UserModel) and bool(user_instance):
                return self.__delete_user(organization_id, uid, user_instance)

        elif isinstance(email, str) and bool(email.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.email == email).get_async().get_result()
            if isinstance(user_instance, UserModel) and bool(user_instance):
                return self.__delete_user(organization_id, uid, user_instance)

        elif isinstance(cell, str) and bool(cell.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.cell == cell).get_async().get_result()
            if isinstance(user_instance, UserModel) and bool(user_instance):
                # TODO- rather mark user as deleted
                return self.__delete_user(organization_id, uid, user_instance)

        return jsonify(dict(status=False, message='User not found')), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def get_active_users(self, organization_id: Optional[str]) -> tuple:
        """
            return a list of all users
        :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        users_list: List[dict] = [user.to_dict() for user in UserModel.query(
            UserModel.organization_id == organization_id, UserModel.is_active == True).fetch()]

        if users_list:
            message: str = 'successfully retrieved active users'
            return jsonify(dict(status=True,
                                payload=users_list,
                                message=message)), status_codes.status_ok_code
        message: str = "Unable to find users"
        return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    async def get_active_users_async(self, organization_id: Optional[str]) -> tuple:
        """
            get active users list

            :param organization_id:
            :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        users_list: List[dict] = [user.to_dict() for user in UserModel.query(
            UserModel.organization_id == organization_id, UserModel.is_active == True).fetch_async().get_result()]

        if users_list:
            message: str = 'successfully retrieved active users'
            return jsonify(dict(status=True,
                                payload=users_list,
                                message=message)), status_codes.status_ok_code

        message: str = "Unable to find users list"
        return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def get_in_active_users(self, organization_id: Optional[str]) -> tuple:
        """
            get in-active  list
        :param organization_id:
        :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        users_list: List[dict] = [user.to_dict() for user in UserModel.query(
            UserModel.organization_id == organization_id, UserModel.is_active == False).fetch()]

        if users_list:
            message: str = 'successfully retrieved in-active users'
            return jsonify(dict(status=True,
                                payload=users_list,
                                message=message)), status_codes.status_ok_code

        message: str = "Unable to find active users"
        return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    async def get_in_active_users_async(self, organization_id: Optional[str]) -> tuple:
        """
            return a list of non active users
        :param organization_id:
        :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        users_list: List[dict] = [user.to_dict() for user in UserModel.query(
            UserModel.organization_id == organization_id, UserModel.is_active == False).fetch_async().get_result()]

        if isinstance(users_list, list) and users_list:
            message: str = 'successfully retrieved in-active users'
            return jsonify(dict(status=True,
                                payload=users_list,
                                message=message)), status_codes.status_ok_code

        message: str = "Unable to find active users"
        return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def get_all_users(self, organization_id: Optional[str]) -> tuple:
        """
            get a list of all users
        :param organization_id:
        :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        users_list: List[dict] = [user.to_dict() for user in UserModel.query(
            UserModel.organization_id == organization_id).fetch()]

        if users_list:
            message: str = 'successfully retrieved active users'
            return jsonify(dict(status=True,
                                payload=users_list,
                                message=message)), status_codes.status_ok_code

        message: str = "Unable to retrieve active users"
        return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    async def get_all_users_async(self, organization_id: Optional[str]) -> tuple:
        """
            get a list of all users
        :param organization_id:
        :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        users_list: List[dict] = [user.to_dict() for user in UserModel.query(
            UserModel.organization_id == organization_id).fetch_async().get_result()]

        if users_list:
            message: str = 'successfully retrieved active users'
            return jsonify(dict(status=True,
                                payload=users_list,
                                message=message)), status_codes.status_ok_code

        message: str = "Unable to retrieve all users"
        return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def get_user(self, organization_id: Optional[str], uid: Optional[str] = None, cell: Optional[str] = None,
                 email: Optional[str] = None) -> tuple:
        """
            return a user either by uid, cell or email
            :param organization_id:
            :param uid:
            :param cell:
            :param email:
            :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if isinstance(uid, str) and bool(uid.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.uid == uid).get()
            if isinstance(user_instance, UserModel) and bool(user_instance):
                message: str = 'successfully retrieved user by uid'
                return jsonify(dict(status=True,
                                    payload=user_instance.to_dict(),
                                    message=message)), status_codes.status_ok_code
            message: str = "Unable to find user with that uid"
            return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

        if isinstance(cell, str) and bool(cell.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.cell == cell).get()
            if isinstance(user_instance, UserModel) and bool(user_instance):
                message: str = 'successfully retrieved user by cell'
                return jsonify(dict(status=True,
                                    payload=user_instance.to_dict(),
                                    message=message)), status_codes.status_ok_code

            message: str = "Unable to find user with that cell number"
            return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

        if not isinstance(email, str) or not bool(email.strip()):
            message: str = 'to retrieve a user either submit an email, cell or user id'
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.email == email).get()
        if isinstance(user_instance, UserModel) and bool(user_instance):
            message: str = 'successfully retrieved user by email'
            return jsonify(dict(status=True,
                                payload=user_instance.to_dict(),
                                message=message)), status_codes.status_ok_code

        message: str = "Unable to find user with that email address"
        return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    async def get_user_async(self, organization_id: Optional[str], uid: Optional[str] = None,
                             cell: Optional[str] = None, email: Optional[str] = None) -> tuple:
        """
            return a user either by uid, cell or email
            :param organization_id:
            :param uid:
            :param cell:
            :param email:
            :return:
        """
        if isinstance(uid, str) and bool(uid.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.uid == uid).get_async().get_result()
            if isinstance(user_instance, UserModel) and bool(user_instance):
                message: str = 'successfully retrieved user by uid'
                return jsonify(dict(status=True,
                                    payload=user_instance.to_dict(),
                                    message=message)), status_codes.status_ok_code
            message: str = "Unable to find user with that uid"
            return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

        if isinstance(cell, str) and bool(cell.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.cell == cell).get_async().get_result()
            if isinstance(user_instance, UserModel) and bool(user_instance):
                message: str = 'successfully retrieved user by cell'
                return jsonify(dict(status=True,
                                    payload=user_instance.to_dict(),
                                    message=message)), status_codes.status_ok_code
            message: str = "Unable to find user with that cell number"
            return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

        if isinstance(email, str) and bool(email.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.email == email).get_async().get_result()
            if isinstance(user_instance, UserModel) and bool(user_instance):
                message: str = 'successfully retrieved user by email'
                return jsonify(dict(status=True,
                                    payload=user_instance.to_dict(),
                                    message=message)), status_codes.status_ok_code

            message: str = "Unable to find user with that email address"
            return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

        message: str = 'to retrieve a user either submit an email, cell or user id'
        raise InputError(status=error_codes.input_error_code, description=message)

    @use_context
    @handle_view_errors
    def check_password(self, organization_id: Optional[str], uid: Optional[str],
                       password: Optional[str]) -> tuple:
        """
            check password
        :param organization_id:
        :param uid:
        :param password:
        :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "user Id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(password, str) or not bool(password.strip()):
            message: str = "password is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()
        if not (isinstance(user_instance, UserModel) and bool(user_instance)):
            return jsonify(dict(status=False, message='User not found')), status_codes.data_not_found_code

        if check_password_hash(password=password, pwhash=user_instance.password):
            return jsonify(dict(status=True, message='Passwords match')), status_codes.status_ok_code

        message: str = 'Passwords do not match'
        return jsonify(dict(status=False,
                            message=message)), error_codes.authentication_required_error_code

    @use_context
    @handle_view_errors
    async def check_password_async(self, organization_id: Optional[str],
                                   uid: Optional[str], password: Optional[str]) -> tuple:
        """
            check password asynchronously
        :param organization_id:
        :param uid:
        :param password:
        :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(password, str) or not bool(password.strip()):
            message: str = "password is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get_async().get_result()
        if not (isinstance(user_instance, UserModel) and bool(user_instance)):
            return jsonify(dict(status=False, message='User not found')), status_codes.data_not_found_code

        if check_password_hash(password=password, pwhash=user_instance.password):
            return jsonify(dict(status=True, message='Passwords match')), status_codes.status_ok_code

        message: str = 'Passwords do not match'
        return jsonify(dict(status=False,
                            message=message)), error_codes.authentication_required_error_code

    @use_context
    @handle_view_errors
    def deactivate_user(self, organization_id: Optional[str], uid: Optional[str]) -> tuple:
        """
            de-activate user
        :param organization_id:
        :param uid:
        :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "UserID is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()
        if not (isinstance(user_instance, UserModel) and bool(user_instance)):
            message: str = "User Not found"
            return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

        user_instance.is_active = False
        user_instance.put()

        self.__delete_user_cache(organization_id, uid, user_instance)
        return jsonify(dict(status=True, message='User Deactivated')), status_codes.status_ok_code

    @use_context
    @handle_view_errors
    async def deactivate_user_async(self, organization_id: Optional[str],
                                    uid: Optional[str]) -> tuple:
        """
            deactivate_user_async given uid and organization_id
        :param organization_id:
        :param uid:
        :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get_async().get_result()
        if not isinstance(user_instance, UserModel) or not bool(user_instance):
            message: str = "User Not found"
            return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code
        user_instance.is_active = False
        user_instance.put_async().get_result()
        self.__delete_user_cache(organization_id, uid, user_instance)

        return jsonify(dict(status=True,
                            payload=user_instance.to_dict(),
                            message='User Successfully Deactivated')), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def login(self, organization_id: Optional[str], email: Optional[str],
              password: Optional[str]) -> tuple:
        """
            this login utility may support client app , not necessary for admin and service to service calls
            Options:
            firebase login, JWT Token

        :param organization_id:
        :param email:
        :param password:
        :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(email, str) or not bool(email.strip()):
            message: str = "email is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(password, str) or not bool(password.strip()):
            message: str = "password is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_model: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                UserModel.email == email).get()

        if not isinstance(user_model, UserModel) and user_model.email == email:
            message: str = "user not found"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not user_model.is_active:
            message: str = 'User is de-activated please contact admin'
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        if check_password_hash(user_model.password, password):
            token = encode_auth_token(uid=user_model.uid)
            payload: dict = dict(token=token, user=user_model.to_dict())
            return jsonify(dict(status=True,
                                payload=payload,
                                message='you are successfully logged in')), status_codes.status_ok_code

        message: str = f'login was not successful please check your email: {email} or password'
        return jsonify(dict(message=message)), error_codes.un_auth_error_code

    @use_context
    @handle_view_errors
    def send_recovery_email(self, organization_id: Optional[str],
                            email: Optional[str]) -> tuple:
        """
            **send_recovery_email**
                sends a recovery email on behalf of users
        :param organization_id:
        :param email:
        :return:
        """

        user_model: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                UserModel.email == email).get()
        if isinstance(user_model, UserModel) and bool(user_model):
            # NOTE cannot send failure messages as it will give attackers more information than necessary
            user_model.recovery_code = create_id()
            key: Optional[ndb.Key] = user_model.put(retries=self._max_retries, timeout=self._max_timeout)
            if not isinstance(key, ndb.Key):
                message: str = "Database Error: Unable to create recovery code please try again later"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            uid: str = user_model.uid
            cell: str = user_model.cell
            _kwargs: dict = dict(user_view=UserView, organization_id=organization_id, uid=uid, email=email, cell=cell)
            app_cache._schedule_cache_deletion(func=app_cache._delete_user_cache, kwargs=_kwargs)
            # Using super method to send recovery email
            kwargs: dict = dict(organization_id=organization_id, uid=user_model.uid,
                                recovery_code=user_model.recovery_code)
            self._base_email_scheduler(func=super().send_recovery_email, kwargs=kwargs)

        # NOTE cannot send failure messages as it will give attackers more information than necessary
        message: str = "A password recovery email has been sent to your email inbox"
        return jsonify(dict(status=True, message=message)), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def _system_user_exist(self, email: Optional[str] = None, uid: Optional[str] = None) -> tuple:
        """
            **_system_user_exist**

        :param email:
        :return:
        """
        if isinstance(email, str) and bool(email.strip()):
            users_instance: UserModel = UserModel.query(UserModel.email == email).get()
            message: str = "user exist"
            return jsonify(dict(status=True,
                                payload=users_instance.to_dict(),
                                message=message)), status_codes.status_ok_code

        elif isinstance(uid, str) and bool(uid.strip()):
            users_instance: UserModel = UserModel.query(UserModel.uid == uid).get()
            message: str = "user exist"
            return jsonify(dict(status=True,
                                payload=users_instance.to_dict(),
                                message=message)), status_codes.status_ok_code

        message: str = "user not found"
        return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

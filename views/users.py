import typing
from flask import jsonify, current_app
from werkzeug.security import check_password_hash
from config.exceptions import error_codes, status_codes, InputError, UnAuthenticatedError, DataServiceError
from database.organization import OrgValidators
from main import app_cache
from database.users import UserModel, UserValidators
from security.users_authenticator import encode_auth_token
from utils.utils import create_id, return_ttl, can_cache
from config.exception_handlers import handle_view_errors
from config.use_context import use_context

users_type = typing.List[UserModel]


class UserEmails:
    ***REMOVED***
        used to send emails and notifications to users
    ***REMOVED***
    def __init__(self):
        self.admin_email: str = current_app.config.get('ADMIN_EMAIL')
        self.no_response_email: str = current_app.config.get('NO_RESPONSE_EMAIL')
        self.smtp_server_uri: str = current_app.config.get('SMTP_SERVER_URI')
        self.smtp_server_password: str = current_app.config.get('SMTP_SERVER_PASSWORD')
        self.smtp_server_username: str = current_app.config.get('SMTP_SERVER_USERNAME')

    def _do_send_mail(self, to_address: str, subject: str, body_text: str, body_html: str) -> bool:
        ***REMOVED***
            actually send email here
        :param to_address:
        :param subject:
        :param body_text:
        :param body_html:
        :return:
        ***REMOVED***
        pass

    def send_welcome_to_admins_email(self, email) -> None:
        ***REMOVED***
            send an email to admin welcoming him to the admins club
        :param email:
        :return:
        ***REMOVED***
        pass

    def send_goodbye_admin_email(self, email) -> None:
        ***REMOVED***
            send an email informing the user he or she is no longer admin
        :param email:
        :return:
        ***REMOVED***
        pass

    def send_welcome_to_support_email(self, email) -> None:
        ***REMOVED***
            send welcome to support email
        :param email:
        :return:
        ***REMOVED***
        pass

    def send_goodbye_support_email(self, email) -> None:
        ***REMOVED***

        :param email:
        :return:
        ***REMOVED***
        pass

    def send_recovery_email(self, email) -> None:
        ***REMOVED***
            send recovery email
        :param email:
        :return:
        ***REMOVED***


class Validators(UserValidators, OrgValidators, UserEmails):
    ***REMOVED***
        User Validators
    ***REMOVED***
    def __init__(self):
        super(Validators, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @staticmethod
    def check_required(organization_id: typing.Union[str, None], email: typing.Union[str, None], cell: typing.Union[str, None]) -> None:

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
    def check_org_and_uid(organization_id: typing.Union[str, None], uid: typing.Union[str, None]) -> None:
        ***REMOVED***
            check if organization_id or uid are available if not throw input_error_code and exit
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        pass

    def can_add_user(self, organization_id: typing.Union[str, None], email: typing.Union[str, None],
                     cell: typing.Union[str, None]) -> bool:
        ***REMOVED***
            if this returns true the user can be added

            :param email: required - check if email is available to be used on this organization
            :param cell: required - check if the cell number related to this user is not already registered for another user
            :param organization_id: required - check if user has logged into this organization
            :return: boolean indicate if the user can be added or not
        ***REMOVED***
        is_organization_exist: typing.Union[bool, None] = self.is_organization_exist(organization_id=organization_id)
        # is_user_valid: typing.Union[bool, None] = self.is_user_valid(organization_id=organization_id, uid=uid)
        is_email_valid: typing.Union[bool, None] = self.is_email_available(organization_id=organization_id, email=email)
        is_cell_available: typing.Union[bool, None] = self.is_cell_available(organization_id=organization_id, cell=cell)

        if isinstance(is_organization_exist, bool) and isinstance(is_email_valid, bool) and \
                isinstance(is_cell_available, bool):
            return is_organization_exist and is_email_valid and is_cell_available

        message: str = "Database Error: unable to check the validity of your input due to database errors try again later"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)


# TODO create test cases for User View and Documentations
# noinspection DuplicatedCode
class UserView(Validators):
    def __init__(self):
        super(UserView, self).__init__()

    def _create_unique_uid(self) -> str:
        _uid = create_id()
        user_instance: UserModel = UserModel.query(UserModel.uid == _uid).get()
        return self._create_unique_uid() if isinstance(user_instance, UserModel) else _uid

    @use_context
    @handle_view_errors
    def add_user(self,   organization_id: typing.Union[str, None], names:  typing.Union[str, None],
                 surname:  typing.Union[str, None], cell:  typing.Union[str, None], email:  typing.Union[str, None],
                 password:  typing.Union[str, None], uid:  typing.Union[str, None] = None) -> tuple:
        ***REMOVED***
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
        ***REMOVED***
        # Check if all required values are present if not throw inputError and exit
        self.check_required(organization_id=organization_id, email=email, cell=cell)

        if not self.can_add_user(organization_id=organization_id, email=email, cell=cell):
            message: str = "You are not authorized to create a user record in this organization"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            # This is a new user who has not created a uid from another login service - create a unique uid
            uid = self._create_unique_uid()

        user_instance: UserModel = UserModel(organization_id=organization_id, uid=uid, names=names,
                                             surname=surname, cell=cell, email=email, password=password, is_active=True)

        key = user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not bool(key):
            message: str = "Unable to save database"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)
        print("User Instance: {}".format(user_instance))
        return jsonify({'status': True,
                        "message": "Successfully created new user",
                        "payload": user_instance.to_dict()
                        }), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    async def add_user_async(self, organization_id: typing.Union[str, None],  names:  typing.Union[str, None], surname:  typing.Union[str, None],
                             cell:  typing.Union[str, None], email:  typing.Union[str, None],
                             password:  typing.Union[str, None], uid:  typing.Union[str, None] = None) -> tuple:
        ***REMOVED***
            creates a new user asynchronously - all parameters are required
        :param organization_id:
        :param names:
        :param surname:
        :param cell:
        :param email:
        :param password:
        :param uid:
        :return:
        ***REMOVED***
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
        if not bool(key):
            message: str = "Unable to save user database"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        return jsonify({'status': True,
                        "message": "Successfully created new user",
                        "payload": user_instance.to_dict()
                        }), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def update_user(self, organization_id: typing.Union[str, None], uid:  typing.Union[str, None],
                    names:  typing.Union[str, None], surname:  typing.Union[str, None],
                    cell:  typing.Union[str, None], email:  typing.Union[str, None], is_admin: bool,
                    is_support: bool) -> tuple:
        ***REMOVED***
                update user details all fields are required
        :param organization_id:
        :param uid:
        :param names:
        :param surname:
        :param cell:
        :param email:
        :param is_admin:
        :param is_support:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "User ID is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()

        if isinstance(user_instance, UserModel):
            user_instance.names = names
            user_instance.surname = surname
            user_instance.cell = cell
            user_instance.email = email
            user_instance.is_admin = is_admin
            user_instance.is_support = is_support
            key = user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "Unable to save user database"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            return jsonify({'status': True, 'message': 'successfully updated user details',
                            'payload': user_instance.to_dict()}), status_codes.successfully_updated_code

        return jsonify({'status': False,
                        'message': 'user not found cannot update user details'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    async def update_user_async(self, organization_id: typing.Union[str, None], uid:  typing.Union[str, None],
                                names:  typing.Union[str, None], surname:  typing.Union[str, None],
                                cell:  typing.Union[str, None], email:  typing.Union[str, None],
                                is_admin: bool, is_support: bool) -> tuple:
        ***REMOVED***
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
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "User ID is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get_async().get_result()
        if isinstance(user_instance, UserModel):
            user_instance.names = names
            user_instance.surname = surname
            user_instance.cell = cell
            user_instance.email = email
            user_instance.is_admin = is_admin
            user_instance.is_support = is_support
            key = user_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
            if not bool(key):
                message: str = "Unable to save user database"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            return jsonify({'status': True, 'message': 'successfully updated user details',
                            'payload': user_instance.to_dict()}), status_codes.successfully_updated_code
        else:
            return jsonify({'status': False,
                            'message': 'user not found cannot update user details'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def update_user_names(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                          names:  typing.Union[str, None], surname: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            given organization_id and uid update names
        :param organization_id: required
        :param uid: required
        :param names: optional
        :param surname: optional
        :return:
        ***REMOVED***
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
        if isinstance(user_instance, UserModel):
            user_instance.names = names
            user_instance.surname = surname
            key = user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "Database Error: unable to update names"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
            message: str = "Successfully updated user names"
            return jsonify({'status': True, 'payload': user_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = "User not found: Unable to update names"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def update_cell(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                    cell: typing.Union[str, None]) -> tuple:
        ***REMOVED***
                given organization_id and uid update cell number
            :param organization_id:
            :param uid:
            :param cell:
            :return:
        ***REMOVED***
        self.check_org_and_uid(organization_id=organization_id, uid=uid)
        if not isinstance(cell, str) or not bool(cell.strip()):
            message: str = "cell is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()
        if isinstance(user_instance, UserModel):
            user_instance.cell = cell
            # TODO - run a function to send verification sms if available_funds
            key = user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "Database Error: unable to save updated user record"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
            message: str = "Successfully Updated Cell Number"
            return jsonify({'status': True, 'payload': user_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code
        message: str = "User Record not found: Unable to update cell number"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def update_email(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                     email: typing.Union[str, None]) -> tuple:
        ***REMOVED***
         update user email given organization_id and uid
        :param organization_id:
        :param uid:
        :param email:
        :return:
        ***REMOVED***
        self.check_org_and_uid(organization_id=organization_id, uid=uid)
        if not isinstance(email, str) or not bool(email.strip()):
            message: str = "Email is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()
        if isinstance(user_instance, UserModel):
            if user_instance.email != email:
                user_instance.email = email
                # TODO send verification email and mark email as not verified
                key = user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
                if not bool(key):
                    message: str = "Database Error: Unable to update user record"
                    raise DataServiceError(status=error_codes.data_service_error_code, description=message)

                message: str = "Successfully Updated Email Record please check your email inbox for verification email"
                return jsonify({'status': True, 'payload': user_instance.to_dict(),
                                'message': message}), status_codes.successfully_updated_code

            message: str = "Email is already upto-date"
            return jsonify({'status': True, 'payload': user_instance.to_dict(),
                            'message': message}), status_codes.status_ok_code

        message: str = "Unable to find User record: Email not updated"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def update_password(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                        password:  typing.Union[str, None], new_password: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            update password given  organization_id and uid update password
            check if old password matches the present password if that's the case then
            update the password
        :param organization_id:
        :param uid:
        :param password:
        :param new_password:
        :return:
        ***REMOVED***
        self.check_org_and_uid(organization_id=organization_id, uid=uid)

        if not isinstance(password, str) or not bool(password.strip()):
            message: str = "password is required"
            raise InputError(status=error_codes.input_error_code, description=message)
        if not isinstance(new_password, str) or not bool(new_password.strip()):
            message: str = "new Password is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()

        if isinstance(user_instance, UserModel):
            # Note: checking if old password is equal to the password on file
            if not check_password_hash(password=password, pwhash=user_instance.password):
                message: str = "Passwords do not match - please try again"
                raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

            user_instance.password = new_password
            key = user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "Database Error: unable to update password"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            # TODO - logoff the user
            message: str = "Successfully Updated Password - please login again"
            return jsonify({'status': True,
                            'payload': user_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = "User Record not found: Unable to update password"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def set_is_admin(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                     is_admin: typing.Union[bool, None] = False) -> tuple:
        ***REMOVED***
            given organization_id and uid update is_admin
        :param organization_id:
        :param uid:
        :param is_admin:
        :return:
        ***REMOVED***
        self.check_org_and_uid(organization_id=organization_id, uid=uid)
        if not isinstance(is_admin, bool):
            message: str = "is_admin is required and can only be a boolean"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()
        if isinstance(user_instance, UserModel):
            user_instance.is_admin = is_admin
            key = user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "Database Error: Unable to update user admin status"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            if is_admin:
                self.send_welcome_to_admins_email(email=user_instance.email)
            else:
                self.send_goodbye_admin_email(email=user_instance.email)

            message: str = "Successfully Update admin status"
            return jsonify({'status': True, 'payload': user_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def set_is_support(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                       is_support:  typing.Union[bool, None]) -> tuple:
        ***REMOVED***
            given organization_id and uid set support role
        :param organization_id:
        :param uid:
        :param is_support:
        :return:
        ***REMOVED***
        self.check_org_and_uid(organization_id=organization_id, uid=uid)
        if not isinstance(is_support, bool):
            message: str = "is_support is required and can only be a boolean"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()
        if isinstance(user_instance, UserModel):
            user_instance.is_support = is_support
            key = user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "Database Error: Unable to update user support status"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            if is_support:
                self.send_welcome_to_support_email(email=user_instance.email)
            else:
                self.send_goodbye_support_email(email=user_instance.email)

            message: str = "Successfully Update support status"
            return jsonify({'status': True, 'payload': user_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def set_address(self, organization_id: typing.Union[str, None],
                    uid: typing.Union[str, None], address_dict: typing.Union[dict, None]) -> tuple:
        ***REMOVED***
            given organization_id and uid with address_dict update address
        :param organization_id:
        :param uid:
        :param address_dict:
        :return:
        ***REMOVED***
        pass

    @use_context
    @handle_view_errors
    def delete_user(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None] = None,
                    email: typing.Union[str, None] = None, cell:  typing.Union[str, None] = None) -> tuple:
        ***REMOVED***
            given either, uid, email or cell delete user
            :param organization_id:
            :param uid:
            :param email:
            :param cell:
            :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if isinstance(uid, str) and bool(uid.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.uid == uid).get()
            if isinstance(user_instance, UserModel):
                user_instance.key.delete()
                return jsonify({'status': True,
                                'message': 'successfully deleted user'}), status_codes.successfully_updated_code

        elif isinstance(email, str) and bool(email.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.email == email).get()
            if isinstance(user_instance, UserModel):
                user_instance.key.delete()
                return jsonify({'status': True,
                                'message': 'successfully deleted user'}), status_codes.successfully_updated_code

        elif isinstance(cell, str) and bool(cell.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.cell == cell).get()
            if isinstance(user_instance, UserModel):
                # TODO- rather mark user as deleted
                user_instance.key.delete()
                return jsonify({'status': True,
                                'message': 'successfully deleted user'}), status_codes.successfully_updated_code

        return jsonify({'status': False, 'message': 'user not found'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    async def delete_user_async(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None] = None,
                                email: typing.Union[str, None] = None, cell:  typing.Union[str, None] = None) -> tuple:
        ***REMOVED***
            given either, uid, email or cell delete user
            :param organization_id:
            :param uid:
            :param email:
            :param cell:
            :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if isinstance(uid, str) and bool(uid.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.uid == uid).get_async().get_result()
            if isinstance(user_instance, UserModel):
                user_instance.key.delete()
                return jsonify({'status': True,
                                'message': 'successfully deleted user'}), status_codes.data_not_found_code

        elif isinstance(email, str) and bool(email.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.email == email).get_async().get_result()
            if isinstance(user_instance, UserModel):
                user_instance.key.delete()
                return jsonify({'status': True,
                                'message': 'successfully deleted user'}), status_codes.data_not_found_code

        elif isinstance(cell, str) and bool(cell.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.cell == cell).get_async().get_result()
            if isinstance(user_instance, UserModel):
                # TODO- rather mark user as deleted
                user_instance.key.delete()
                return jsonify({'status': True,
                                'message': 'successfully deleted user'}), status_codes.data_not_found_code

        return jsonify({'status': False, 'message': 'user not found'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_active_users(self, organization_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            return a list of all users
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        users_list: typing.List[dict] = [user.to_dict() for user in UserModel.query(
            UserModel.organization_id == organization_id, UserModel.is_active == True).fetch()]

        if len(users_list) > 0:
            return jsonify({'status': True, 'payload': users_list,
                            'message': 'successfully retrieved active users'}), status_codes.status_ok_code
        message: str = "Unable to find users"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def get_active_users_async(self, organization_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            get active users list

            :param organization_id:
            :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        users_list: typing.List[dict] = [user.to_dict() for user in UserModel.query(
            UserModel.organization_id == organization_id, UserModel.is_active == True).fetch_async().get_result()]

        if len(users_list) > 0:
            return jsonify({'status': True,
                            'payload': users_list,
                            'message': 'successfully retrieved active users'}), status_codes.status_ok_code

        message: str = "Unable to find users list"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_in_active_users(self, organization_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            get in-active  list
        :param organization_id:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        users_list: typing.List[dict] = [user.to_dict() for user in UserModel.query(
            UserModel.organization_id == organization_id, UserModel.is_active == False).fetch()]

        if len(users_list) > 0:
            message: str = 'successfully retrieved active users'
            return jsonify({'status': True, 'payload': users_list,
                            'message': message}), status_codes.status_ok_code

        message: str = "Unable to find active users"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def get_in_active_users_async(self, organization_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            return a list of non active users
        :param organization_id:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        users_list: typing.List[dict] = [user.to_dict() for user in UserModel.query(
            UserModel.organization_id == organization_id, UserModel.is_active == False).fetch_async().get_result()]

        if len(users_list) > 0:
            return jsonify({'status': True,
                            'payload': users_list,
                            'message': 'successfully retrieved active users'}), status_codes.status_ok_code

        message: str = "Unable to find active users"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_all_users(self, organization_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            get a list of all users
        :param organization_id:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        users_list: typing.List[dict] = [user.to_dict() for user in UserModel.query(
            UserModel.organization_id == organization_id).fetch()]

        if len(users_list) > 0:
            message: str = 'successfully retrieved active users'
            return jsonify({'status': True,
                            'payload': users_list, 'message': message}), status_codes.status_ok_code

        message: str = "Unable to retrieve active users"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def get_all_users_async(self, organization_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            get a list of all users
        :param organization_id:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        users_list: typing.List[dict] = [user.to_dict() for user in UserModel.query(
            UserModel.organization_id == organization_id).fetch_async().get_result()]

        if len(users_list) > 0:
            message: str = 'successfully retrieved active users'
            return jsonify({'status': True, 'payload': users_list, 'message': message}), 200

        message: str = "Unable to retrieve all users"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_user(self, organization_id: typing.Union[str, None], uid:  typing.Union[str, None] = None, cell:  typing.Union[str, None] = None,
                 email:  typing.Union[str, None] = None) -> tuple:
        ***REMOVED***
            return a user either by uid, cell or email
            :param organization_id:
            :param uid:
            :param cell:
            :param email:
            :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if isinstance(uid, str) and bool(uid.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.uid == uid).get()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by uid'
                return jsonify({'status': True,
                                'payload': user_instance.to_dict(),
                                'message': message}), status_codes.status_ok_code
            message: str = "Unable to find user with that uid"
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

        if isinstance(cell, str) and bool(cell.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.cell == cell).get()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by cell'
                return jsonify({'status': True,
                                'payload': user_instance.to_dict(),
                                'message': message}), status_codes.status_ok_code
            message: str = "Unable to find user with that cell number"
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

        if isinstance(email, str) and bool(email.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.email == email).get()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by email'
                return jsonify({'status': True,
                                'payload': user_instance.to_dict(),
                                'message': message}), status_codes.status_ok_code
            message: str = "Unable to find user with that email address"
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

        message: str = 'to retrieve a user either submit an email, cell or user id'
        raise InputError(status=error_codes.input_error_code, description=message)

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def get_user_async(self, organization_id: typing.Union[str, None], uid:  typing.Union[str, None] = None,
                             cell:  typing.Union[str, None] = None, email:  typing.Union[str, None] = None) -> tuple:
        ***REMOVED***
            return a user either by uid, cell or email
            :param organization_id:
            :param uid:
            :param cell:
            :param email:
            :return:
        ***REMOVED***
        if isinstance(uid, str) and bool(uid.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.uid == uid).get_async().get_result()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by uid'
                return jsonify({'status': True,
                                'payload': user_instance.to_dict(),
                                'message': message}), status_codes.status_ok_code
            message: str = "Unable to find user with that uid"
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

        if isinstance(cell, str) and bool(cell.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.cell == cell).get_async().get_result()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by cell'
                return jsonify({'status': True,
                                'payload': user_instance.to_dict(),
                                'message': message}), status_codes.status_ok_code
            message: str = "Unable to find user with that cell number"
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

        if isinstance(email, str) and bool(email.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.email == email).get_async().get_result()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by email'
                return jsonify({'status': True,
                                'payload': user_instance.to_dict(),
                                'message': message}), status_codes.status_ok_code
            message: str = "Unable to find user with that email address"
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

        message: str = 'to retrieve a user either submit an email, cell or user id'
        raise InputError(status=error_codes.input_error_code, description=message)

    @use_context
    @handle_view_errors
    def check_password(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                       password:  typing.Union[str, None]) -> tuple:
        ***REMOVED***
            check password
        :param organization_id:
        :param uid:
        :param password:
        :return:
        ***REMOVED***
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
        if isinstance(user_instance, UserModel):
            if check_password_hash(password=password, pwhash=user_instance.password) is True:
                return jsonify({'status': True, 'message': 'passwords match'}), status_codes.status_ok_code

            return jsonify({'status': False,
                            'message': 'passwords do not match'}), error_codes.authentication_required_error_code
        else:
            return jsonify({'status': False, 'message': 'user not found'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    async def check_password_async(self, organization_id: typing.Union[str, None],
                                   uid: typing.Union[str, None], password:  typing.Union[str, None]) -> tuple:
        ***REMOVED***
            check password asynchronously
        :param organization_id:
        :param uid:
        :param password:
        :return:
        ***REMOVED***
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
        if isinstance(user_instance, UserModel):
            if check_password_hash(password=password, pwhash=user_instance.password) is True:
                return jsonify({'status': True, 'message': 'passwords match'}), status_codes.status_ok_code

            return jsonify({'status': False,
                            'message': 'passwords do not match'}), error_codes.authentication_required_error_code
        else:
            return jsonify({'status': False, 'message': 'user not found'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def deactivate_user(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            de-activate user
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "UserID is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()
        if isinstance(user_instance, UserModel):
            user_instance.is_active = False
            user_instance.put()
            return jsonify({'status': True, 'message': 'user deactivated'}), status_codes.status_ok_code

        return jsonify({'status': False, 'message': 'user not found'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    async def deactivate_user_async(self, organization_id: typing.Union[str, None],
                                    uid: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            deactivate_user_async given uid and organization_id
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get_async().get_result()
        if isinstance(user_instance, UserModel):
            user_instance.is_active = False
            user_instance.put_async().get_result()
            return jsonify({'status': True, 'message': 'user deactivated'}), status_codes.status_ok_code

        return jsonify({'status': False, 'message': 'user not found'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def login(self, organization_id: typing.Union[str, None], email:   typing.Union[str, None],
              password: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            this login utility may support client app , not necessary for admin and service to service calls
            Options:
            firebase login, JWT Token

        :param organization_id:
        :param email:
        :param password:
        :return:
        ***REMOVED***
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

        if not isinstance(user_model, UserModel):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not user_model.is_active:
            message: str = 'User is de-activated please contact admin'
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        if check_password_hash(user_model.password, password):
            token = encode_auth_token(uid=user_model.uid)
            return jsonify({'token': token,
                            'message': "you have successfully logged in"}), status_codes.status_ok_code

        message: str = 'login was not successful please check your <strong>email: <code>{}</code> </strong> or ' \
                       '<strong>password: <code>{}</code></strong>'.format(email, password)

        return jsonify({"message": message}), error_codes.un_auth_error_code

    @use_context
    @handle_view_errors
    def send_recovery_email(self, organization_id: typing.Union[str, None],
                            email: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            # Use the email sdk to send recovery email and return
        :param organization_id:
        :param email:
        :return:
        ***REMOVED***
        # TODO: complete this by actually sending recovery email
        return jsonify({'status': False, 'message': 'Unable to send recovery email please try again later'}), 500



import typing
from flask import jsonify, current_app
from werkzeug.security import check_password_hash

from config.exceptions import error_codes, status_codes, InputError, UnAuthenticatedError
from main import app_cache
from database.users import UserModel
from security.users_authenticator import encode_auth_token
from utils.utils import create_id, return_ttl, can_cache
from config.exception_handlers import handle_view_errors
from config.use_context import use_context

users_type = typing.List[UserModel]


# TODO create test cases for User View and Documentations
# noinspection DuplicatedCode
class UserView:
    def __init__(self):
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @use_context
    @handle_view_errors
    def add_user(self,   organization_id: typing.Union[str, None], names:  typing.Union[str, None],
                 surname:  typing.Union[str, None], cell:  typing.Union[str, None], email:  typing.Union[str, None],
                 password:  typing.Union[str, None], uid:  typing.Union[str, None] = None) -> tuple:
        ***REMOVED***
                creates a new user record, the user must already be logged in and have a valid uid
            :param organization_id:
            :param names:
            :param surname:
            :param cell:
            :param email:
            :param password:
            :param uid:
            :return: returns user record
        ***REMOVED***
        # TODO - can_add_user check must be done here
        if not isinstance(uid, str) or not bool(uid.strip()):
            user_instance: UserModel = UserModel.query(UserModel.uid == uid).get()
            if isinstance(user_instance, UserModel):
                return jsonify({'status': False,
                                'message': 'user already exists'}), error_codes.resource_conflict_error_code

        user_instance: UserModel = UserModel.query(UserModel.email == email).get()
        if isinstance(user_instance, UserModel):
            # NOTE: Email already attached to an existing user
            message: str = '''the email you submitted is already attached to an account please 
            login again or reset your password'''
            return jsonify({'status': False, 'message': message}), error_codes.resource_conflict_error_code

        user_instance: UserModel = UserModel.query(UserModel.cell == cell).get()
        if isinstance(user_instance, UserModel):
            message: str = '''the cell you submitted is already attached to an account please login again or 
            reset your password'''
            return jsonify({'status': False, 'message': message}), error_codes.resource_conflict_error_code

        if not isinstance(uid, str) or not bool(uid.strip()):
            uid = create_id()

        user_instance: UserModel = UserModel(organization_id=organization_id, uid=uid, names=names, surname=surname, cell=cell, email=email, password=password,
                                             is_active=True)
        user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        return jsonify({'status': True,
                        "message": "Successfully created new user",
                        "payload": user_instance.to_dict()
                        }), 200

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
        if not isinstance(uid, str) or not bool(uid.strip()):
            user_instance: UserModel = UserModel.query(UserModel.uid == uid).get_async().get_result()
            if isinstance(user_instance, UserModel):
                return jsonify({'status': False,
                                'message': 'user already exists'}), error_codes.resource_conflict_error_code

        user_instance: UserModel = UserModel.query(UserModel.email == email).get_async().get_result()
        if isinstance(user_instance, UserModel):
            message: str = '''the email you submitted is already attached to an account please login again or 
            reset your password'''
            return jsonify({'status': False, 'message': message}), error_codes.resource_conflict_error_code

        user_instance: UserModel = UserModel.query(UserModel.cell == cell).fetch_async().get_result()
        if isinstance(user_instance, UserModel):
            message: str = '''the cell you submitted is already attached to an account please login again 
            or reset your password'''
            return jsonify({'status': False, 'message': message}), error_codes.resource_conflict_error_code

        if (uid is None) or (uid == ""):
            uid = create_id()

        user_instance: UserModel = UserModel(organization_id=organization_id, uid=uid, names=names, surname=surname, cell=cell, email=email, password=password,
                                             is_active=True)
        user_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
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
            user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
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
            user_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
            return jsonify({'status': True, 'message': 'successfully updated user details',
                            'payload': user_instance.to_dict()}), status_codes.successfully_updated_code
        else:
            return jsonify({'status': False,
                            'message': 'user not found cannot update user details'}), status_codes.data_not_found_code

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
            return a list of all users
        :return:
        ***REMOVED***
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
            return a list of non active users
        :return:
        ***REMOVED***
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
        :return:
        ***REMOVED***
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
        :return:
        ***REMOVED***
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
        :return:
        ***REMOVED***
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
        if isinstance(uid, str) and bool(uid.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.uid == uid).get()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by uid'
                return jsonify({'status': True,
                                'payload': user_instance.to_dict(),
                                'message': message}), status_codes.status_ok_code

        if isinstance(cell, str) and bool(cell.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.cell == cell).get()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by cell'
                return jsonify({'status': True,
                                'payload': user_instance.to_dict(),
                                'message': message}), status_codes.status_ok_code

        if isinstance(email, str) and bool(email.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.email == email).get()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by email'
                return jsonify({'status': True,
                                'payload': user_instance.to_dict(),
                                'message': message}), status_codes.status_ok_code

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

        if isinstance(cell, str) and bool(cell.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.cell == cell).get_async().get_result()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by cell'
                return jsonify({'status': True,
                                'payload': user_instance.to_dict(),
                                'message': message}), status_codes.status_ok_code

        if isinstance(email, str) and bool(email.strip()):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.email == email).get_async().get_result()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by email'
                return jsonify({'status': True,
                                'payload': user_instance.to_dict(),
                                'message': message}), status_codes.status_ok_code

        message: str = 'to retrieve a user either submit an email, cell or user id'
        raise InputError(status=error_codes.input_error_code, description=message)

    @use_context
    @handle_view_errors
    def check_password(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                       password:  typing.Union[str, None]) -> tuple:

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
    async def check_password_async(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None], password:  typing.Union[str, None]) -> tuple:
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
        ***REMOVED***
        user_model: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                UserModel.email == email).get()

        if not isinstance(user_model, UserModel):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not user_model.is_active:
            message: str = 'User is de-activated please contact admin'
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        print('checking password hashes: {} password: {}'.format(user_model.password, password))
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
            :return:
        ***REMOVED***
        # TODO: complete this by actually sending recovery email
        return jsonify({'status': False, 'message': 'Unable to send recovery email please try again later'}), 500



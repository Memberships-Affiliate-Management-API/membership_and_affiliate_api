import typing
from flask import jsonify, current_app
from werkzeug.security import check_password_hash
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
            create new user
        ***REMOVED***
        # TODO - refactor this code
        if (uid is not None) and (uid != ""):
            user_instance: UserModel = UserModel.query(UserModel.uid == uid).get()
            if isinstance(user_instance, UserModel):
                return jsonify({'status': False, 'message': 'user already exists'}), 500

        user_instance: UserModel = UserModel.query(UserModel.email == email).get()
        if isinstance(user_instance, UserModel):
            # NOTE: Email already attached to an existing user
            message: str = '''the email you submitted is already attached to an account please 
            login again or reset your password'''
            return jsonify({'status': False, 'message': message}), 500

        user_instance: UserModel = UserModel.query(UserModel.cell == cell).get()
        if isinstance(user_instance, UserModel):
            message: str = '''the cell you submitted is already attached to an account please login again or 
            reset your password'''
            return jsonify({'status': False, 'message': message}), 500

        if (uid is None) or (uid != ""):
            uid = create_id()
        print(uid, names, surname, cell, email, password)
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
            create new user
        ***REMOVED***
        if (uid is not None) and (uid != ""):
            user_instance: UserModel = UserModel.query(UserModel.uid == uid).get_async().get_result()
            if isinstance(user_instance, UserModel):
                return jsonify({'status': False, 'message': 'user already exists'}), 500
        user_instance: UserModel = UserModel.query(UserModel.email == email).get_async().get_result()
        if isinstance(user_instance, UserModel):
            message: str = '''the email you submitted is already attached to an account please login again or 
            reset your password'''
            return jsonify({'status': False, 'message': message}), 500

        user_instance: UserModel = UserModel.query(UserModel.cell == cell).fetch_async().get_result()
        if isinstance(user_instance, UserModel):
            message: str = '''the cell you submitted is already attached to an account please login again 
            or reset your password'''
            return jsonify({'status': False, 'message': message}), 500

        if (uid is None) or (uid == ""):
            uid = create_id()

        user_instance: UserModel = UserModel(organization_id=organization_id, uid=uid, names=names, surname=surname, cell=cell, email=email, password=password,
                                             is_active=True)
        user_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
        return jsonify({'status': True,
                        "message": "Successfully created new user",
                        "payload": user_instance.to_dict()
                        }), 200

    @use_context
    @handle_view_errors
    def update_user(self, organization_id: typing.Union[str, None], uid:  typing.Union[str, None],
                    names:  typing.Union[str, None], surname:  typing.Union[str, None],
                    cell:  typing.Union[str, None], email:  typing.Union[str, None], is_admin: bool,
                    is_support: bool) -> tuple:
        ***REMOVED***
            update user details
        ***REMOVED***
        if (uid is None) or (uid == ""):
            return jsonify({'status': False, 'message': 'User ID is required'}), 500

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
                            'payload': user_instance.to_dict()}), 200
        else:
            return jsonify({'status': False, 'message': 'user not found cannot update user details'}), 500

    @use_context
    @handle_view_errors
    async def update_user_async(self, organization_id: typing.Union[str, None], uid:  typing.Union[str, None],
                                names:  typing.Union[str, None], surname:  typing.Union[str, None],
                                cell:  typing.Union[str, None], email:  typing.Union[str, None],
                                is_admin: bool, is_support: bool) -> tuple:
        ***REMOVED***
            update user details
        ***REMOVED***
        if (uid is None) or (uid == ""):
            return jsonify({'status': False, 'message': 'User ID is required'}), 500

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
                            'payload': user_instance.to_dict()}), 200
        else:
            return jsonify({'status': False, 'message': 'user not found cannot update user details'}), 500

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
        if (uid != "") and (uid is not None):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.uid == uid).get()
            if isinstance(user_instance, UserModel):
                user_instance.key.delete()
                return jsonify({'status': True, 'message': 'successfully deleted user'}), 200
        elif (email != "") and (email is not None):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.email == email).get()
            if isinstance(user_instance, UserModel):
                user_instance.key.delete()
                return jsonify({'status': True, 'message': 'successfully deleted user'}), 200
        elif (cell != "") and (cell is not None):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.cell == cell).get()
            if isinstance(user_instance, UserModel):
                # TODO- rather mark user as deleted
                user_instance.key.delete()
                return jsonify({'status': True, 'message': 'successfully deleted user'}), 200
        return jsonify({'status': False, 'message': 'user not found'}), 500

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
        if (uid != "") and (uid is not None):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.uid == uid).get_async().get_result()
            if isinstance(user_instance, UserModel):
                user_instance.key.delete()
                return jsonify({'status': True, 'message': 'successfully deleted user'}), 200
        elif (email != "") and (email is not None):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.email == email).get_async().get_result()
            if isinstance(user_instance, UserModel):
                user_instance.key.delete()
                return jsonify({'status': True, 'message': 'successfully deleted user'}), 200
        elif (cell != "") and (cell is not None):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.cell == cell).get_async().get_result()
            if isinstance(user_instance, UserModel):
                # TODO- rather mark user as deleted
                user_instance.key.delete()
                return jsonify({'status': True, 'message': 'successfully deleted user'}), 200
        return jsonify({'status': False, 'message': 'user not found'}), 500

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
        return jsonify({'status': True, 'payload': users_list, 'message': 'successfully retrieved active users'}), 200

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

        return jsonify({'status': True, 'payload': users_list, 'message': 'successfully retrieved active users'}), 200

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
        message: str = 'successfully retrieved active users'
        return jsonify({'status': True, 'payload': users_list, 'message': message}), 200

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

        return jsonify({'status': True, 'payload': users_list, 'message': 'successfully retrieved active users'}), 200

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
        message: str = 'successfully retrieved active users'
        return jsonify({'status': True, 'payload': users_list, 'message': message}), 200

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
        message: str = 'successfully retrieved active users'
        return jsonify({'status': True, 'payload': users_list, 'message': message}), 200

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
        if (uid is not None) and (uid != ""):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.uid == uid).get()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by uid'
                return jsonify({'status': True, 'payload': user_instance.to_dict(), 'message': message}), 200

        if (cell is not None) and (cell != ""):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.cell == cell).get()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by cell'
                return jsonify({'status': True, 'payload': user_instance.to_dict(), 'message': message}), 200

        if (email is not None) and (email != ""):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.email == email).get()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by email'
                return jsonify({'status': True, 'payload': user_instance.to_dict(), 'message': message}), 200

        return jsonify({'status': False, 'message': 'to retrieve a user either submit an email, cell or user id'}), 500

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
        if (uid is not None) and (uid != ""):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.uid == uid).get_async().get_result()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by uid'
                return jsonify({'status': True, 'payload': user_instance.to_dict(), 'message': message}), 200

        if (cell is not None) and (cell != ""):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.cell == cell).get_async().get_result()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by cell'
                return jsonify({'status': True, 'payload': user_instance.to_dict(), 'message': message}), 200

        if (email is not None) and (email != ""):
            user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                       UserModel.email == email).get_async().get_result()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by email'
                return jsonify({'status': True, 'payload': user_instance.to_dict(), 'message': message}), 200

        return jsonify({'status': False, 'message': 'to retrieve a user either submit an email, cell or user id'}), 500

    @use_context
    @handle_view_errors
    def check_password(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                       password:  typing.Union[str, None]) -> tuple:

        if (uid is None) or (uid == ""):
            return jsonify({'status': False, 'message': 'please submit user id'}), 500
        if (password is None) or (password == ""):
            return jsonify({'status': False, 'message': 'please submit password'}), 500

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()
        if isinstance(user_instance, UserModel):
            if check_password_hash(password=password, pwhash=user_instance.password) is True:
                return jsonify({'status': True, 'message': 'passwords match'}), 200
            else:
                return jsonify({'status': False, 'message': 'passwords do not match'}), 200
        else:
            return jsonify({'status': False, 'message': 'user not found'}), 200

    @use_context
    @handle_view_errors
    async def check_password_async(self, organization_id: typing.Union[str, None],uid: typing.Union[str, None], password:  typing.Union[str, None]) -> tuple:
        if (uid is None) or (uid == ""):
            return jsonify({'status': False, 'message': 'please submit user id'}), 500
        if (password is None) or (password == ""):
            return jsonify({'status': False, 'message': 'please submit password'}), 500

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get_async().get_result()
        if isinstance(user_instance, UserModel):
            if check_password_hash(password=password, pwhash=user_instance.password) is True:
                return jsonify({'status': True, 'message': 'passwords match'}), 200
            else:
                return jsonify({'status': False, 'message': 'passwords do not match'}), 200
        else:
            return jsonify({'status': False, 'message': 'user not found'}), 200

    @use_context
    @handle_view_errors
    def deactivate_user(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None]) -> tuple:
        if (uid is None) or (uid == ""):
            return jsonify({'status': False, 'message': 'please submit user id'}), 500
        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()
        if isinstance(user_instance, UserModel):
            user_instance.is_active = False
            user_instance.put()
            return jsonify({'status': True, 'message': 'user deactivated'}), 200
        else:
            return jsonify({'status': False, 'message': 'user not found'}), 200

    @use_context
    @handle_view_errors
    async def deactivate_user_async(self, organization_id: typing.Union[str, None],
                                    uid: typing.Union[str, None]) -> tuple:

        if (uid is None) or (uid == ""):
            return jsonify({'status': False, 'message': 'please submit user id'}), 500
        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get_async().get_result()
        if isinstance(user_instance, UserModel):
            user_instance.is_active = False
            user_instance.put_async().get_result()
            return jsonify({'status': True, 'message': 'user deactivated'}), 200
        else:
            return jsonify({'status': False, 'message': 'user not found'}), 200

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
            return jsonify({"message": "User not found"}), 401

        if not user_model.is_active:
            message: str = 'login was not successful user is de-activated please contact admin'
            return jsonify({"message": message}), 403

        print('checking password hashes: {} password: {}'.format(user_model.password, password))
        if check_password_hash(user_model.password, password):
            token = encode_auth_token(uid=user_model.uid)
            return jsonify({'token': token, 'message': "you have successfully logged in"}), 200
        else:
            message: str = 'login was not successful please check your <strong>email: <code>{}</code> </strong> or ' \
                           '<strong>password: <code>{}</code></strong>'.format(email, password)

            return jsonify({"message": message}), 401

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



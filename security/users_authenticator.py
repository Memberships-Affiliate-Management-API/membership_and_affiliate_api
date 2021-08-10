***REMOVED***
    handle users and admin authentication
***REMOVED***
import datetime
from typing import Optional
import jwt
from flask import current_app, request, redirect, url_for, flash
from functools import wraps
from config import config_instance
from database.users import UserModel
from utils import is_development


# noinspection PyUnusedLocal
def check_jwt_token(auth_token: str) -> bool:
    ***REMOVED***
        TODO - handle JWT authentication
    :param auth_token:
    :return:
    ***REMOVED***
    return True


# noinspection PyUnusedLocal
def check_firebase_uid(uid: str) -> bool:
    ***REMOVED***
        TODO - handle firebase authentication
    :param uid:
    :return:
    ***REMOVED***
    return True


def get_admin_user() -> UserModel:
    ***REMOVED***
        return admin_user - uses include on development server
        :return: UserModel
    ***REMOVED***
    uid: str = config_instance.ADMIN_UID
    organization_id: str = config_instance.ORGANIZATION_ID
    admin_email: str = config_instance.ADMIN_EMAIL
    names: str = config_instance.ADMIN_NAMES
    surname: str = config_instance.ADMIN_SURNAME
    password: str = config_instance.ADMIN_PASSWORD
    cell: str = config_instance.ADMIN_CELL

    return UserModel(organization_id=organization_id, uid=uid, email=admin_email, names=names, surname=surname,
                     cell=cell, password=password, is_admin=True)


def is_app_admin(current_user: UserModel) -> bool:
    ***REMOVED***
        checks if user is app admin - meaning admin for main organization for the API
    :param current_user:
    :return:
    ***REMOVED***
    return current_user and current_user.uid and (current_user.organization_id == config_instance.ORGANIZATION_ID)


def encode_auth_token(uid: str) -> str:
    ***REMOVED***
    Generates the Auth Token
    :return: string
    ***REMOVED***
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': uid
        }
        token = jwt.encode(payload=payload, key=str(current_app.config.get('SECRET_KEY')), algorithm='HS256')
        return token.decode()
    except jwt.InvalidAlgorithmError as e:
        return str(e)


def decode_auth_token(auth_token):
    ***REMOVED***
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    ***REMOVED***
    try:
        payload = jwt.decode(jwt=auth_token, key=current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        print("Error Expired Signature")
        return None
    except jwt.InvalidTokenError:
        print("Error : invalid token")
        return None


def handle_users_auth(f):
    # noinspection PyBroadException
    @wraps(f)
    def decorated(*args, **kwargs):
        token: Optional[str] = None
        # print('token headers: {}'.format(request.headers))
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            # print('token found : {}'.format(token))
        # NOTE: if running on development server by-pass authentication and return admin user

        if is_development():
            current_user: Optional[UserModel] = get_admin_user()
            return f(current_user, *args, **kwargs)

        if not token:
            return redirect(url_for('memberships_main.memberships_main_routes', path='login'))
        try:

            uid: Optional[str] = decode_auth_token(auth_token=token)
            if bool(uid):
                current_user: Optional[UserModel] = UserModel.query(uid=uid).get()
                if not isinstance(current_user, UserModel):
                    message = '''Error connecting to database or user does not exist'''
                    flash(message, 'warning')
                    current_user: Optional[UserModel] = None
            else:
                message: str = '''to access restricted areas of this web application please login'''
                flash(message, 'warning')
                current_user: Optional[UserModel] = None
        except jwt.DecodeError:
            flash('Error decoding your token please login again', 'warning')
            return redirect(url_for('memberships_main.memberships_main_routes', path='login'))
        except Exception:
            flash('Unable to locate your account please create a new account', 'warning')
            return redirect(url_for('memberships_main.memberships_main_routes', path='register'))
        return f(current_user, *args, **kwargs)

    return decorated


def logged_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user: Optional[UserModel] = None
        # NOTE: by passes authentication and returns admin user as authenticated
        # user on development
        if is_development():
            current_user: UserModel = get_admin_user()
            return f(current_user, *args, **kwargs)

        if 'x-access-token' in request.headers:
            token: Optional[str] = request.headers['x-access-token']
            if bool(token):
                try:
                    uid: Optional[str] = decode_auth_token(auth_token=token)
                    if bool(uid):
                        user_instance: Optional[UserModel] = UserModel.query(uid=uid).get()
                        if isinstance(user_instance, UserModel):
                            current_user: UserModel = user_instance
                    else:
                        pass
                except jwt.DecodeError:
                    # If user not logged in do nothing
                    pass
            else:
                pass
        return f(current_user, *args, **kwargs)

    return decorated


if __name__ == '__main__':
    ***REMOVED***
        NOTE: fast testing of functions here 
    ***REMOVED***
    pass

"""
    handle users and admin authentication
"""
import datetime
import hmac
import os
from typing import Optional
import jwt
import requests
from flask import current_app, request, redirect, url_for, flash
from functools import wraps
from config import config_instance
from config.exception_handlers import handle_store_errors
from config.use_context import get_client
from database.users import UserModel
from utils import is_development


def get_admin_user() -> UserModel:
    """
        **get_development_user**
            return admin_user - uses include on development server
        :return: dict
    """
    admin_email, cell, names, organization_id, password, surname, uid = get_config_admin_user_details()
    _kwargs: dict = dict(uid=uid, organization_id=organization_id, email=admin_email, names=names, surname=surname,
                         cell=cell, password=password, is_admin=True)
    _user_instance = create_user(_kwargs)
    return _user_instance if isinstance(_user_instance, UserModel) and bool(_user_instance) else UserModel(**_kwargs)


@handle_store_errors
def create_user(_kwargs: dict) -> Optional[UserModel]:
    from google.cloud import ndb
    with get_client().context():
        _user_instance: Optional[UserModel] = UserModel.query(UserModel.uid == _kwargs['uid']).get()
        if not isinstance(_user_instance, UserModel) or not bool(_user_instance):
            _user_instance: UserModel = UserModel(**_kwargs)
            _key: Optional[ndb.Key] = _user_instance.put()
            # NOTE: ignoring key because it does not matter if internet is not on
        return _user_instance


@handle_store_errors
def get_user(uid: str) -> Optional[dict]:
    """
    **send_get_user_request**
        send request for user over api and return user dict

    **PARAMETERS**
        :param uid:
        :return: dict -> user record
    """
    with get_client().context():
        from database.users import UserModel
        user_instance: dict = UserModel.query(UserModel.uid == uid).get()
        return user_instance if isinstance(user_instance, UserModel) and bool(user_instance) else None


def get_config_admin_user_details() -> tuple:
    """
        **get_config_admin_user_details**
            return admin user details from config_instance
    :return:
    """
    uid: str = config_instance.ADMIN_UID
    organization_id: str = config_instance.ORGANIZATION_ID
    admin_email: str = config_instance.ADMIN_EMAIL
    names: str = config_instance.ADMIN_NAMES
    surname: str = config_instance.ADMIN_SURNAME
    password: str = config_instance.ADMIN_PASSWORD
    cell: str = config_instance.ADMIN_CELL
    return admin_email, cell, names, organization_id, password, surname, uid


def is_app_admin(current_user: any) -> bool:
    """
        **is_app_admin**
            checks if user is app admin - meaning admin for main organization for the API

    :param current_user:
    :return: boolean indicating if current user is admin or not
    """
    if isinstance(current_user, dict):
        return current_user and current_user.get('uid') and (
                current_user.get('organization_id') == config_instance.ORGANIZATION_ID)
    _is_system_org: bool = hmac.compare_digest(current_user.organization_id, config_instance.ORGANIZATION_ID)
    return current_user and current_user.uid and _is_system_org


def encode_auth_token(uid: str, expiration_days: int = 0) -> Optional[str]:
    """
    **encode_auth_token**
        Generates the Auth Token for JWT Authentication

    **PARAMETERS**
        :param: uid -> string - unique user id
        :return: string -> auth-token
    """
    try:
        _payload: dict = dict(
            exp=datetime.datetime.utcnow() + datetime.timedelta(days=expiration_days, minutes=30, seconds=5),
            iat=datetime.datetime.utcnow(),
            sub=uid)
        token = jwt.encode(payload=_payload, key=str(current_app.config.get('SECRET_KEY')), algorithm='HS256')
        return token
    except jwt.InvalidAlgorithmError:
        return None


def decode_auth_token(auth_token: str) -> Optional[str]:
    """
    **decode_auth_token**
        Decodes the auth token

    **PARAMETERS**
        :param auth_token:
        :return: string -> uid
    """
    try:
        payload = jwt.decode(jwt=auth_token, key=current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
        return payload.get('sub')

    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def handle_users_auth(func):
    """
        **handle_users_auth**
            handles authentication on html routes for users on client dashboard
            and admin dashboard
        :param func:
    """
    # noinspection PyBroadException
    @wraps(func)
    def decorated(*args, **kwargs):
        """
            decorated
            :param args:
            :param kwargs:
            :return:
        """
        if is_development():
            # TODO also do this on initial setup of application - could be triggered from admin application
            current_user: Optional[UserModel] = get_admin_user()
            return func(current_user, *args, **kwargs)

        token: Optional[str] = request.headers.get('x-access-token')
        # NOTE: if running on development server by-pass authentication and return admin user
        if not bool(token):
            message: str = '''to access restricted areas of this web application please login'''
            flash(message, 'warning')
            return redirect(url_for('memberships_main.memberships_main_routes', path='login'))

        try:
            uid: Optional[str] = decode_auth_token(auth_token=token)
        except jwt.DecodeError:
            flash('Error decoding your token please login again', 'warning')
            return redirect(url_for('memberships_main.memberships_main_routes', path='login'))
        except jwt.InvalidTokenError:
            flash('Your Login Expired please login again', 'warning')
            return redirect(url_for('memberships_main.memberships_main_routes', path='register'))

        if not bool(uid):
            message: str = '''Invalid User'''
            flash(message, 'warning')
            return redirect(url_for('memberships_main.memberships_main_routes', path='login'))

        # NOTE: using client api to access user details
        current_user: Optional[UserModel] = get_user(uid=uid)
        if not isinstance(current_user, dict):
            message: str = '''Error connecting to database or user does not exist'''
            flash(message, 'warning')
            current_user: Optional[dict] = None

        return func(current_user, *args, **kwargs)

    return decorated


def logged_user(func):
    """
        **logged_user**
            only accesses the record of the logged in user without denying access to the route
            if user is not logged in.
    :param func: route to wrap
    :return: wrapped function
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        current_user: Optional[UserModel] = None
        # NOTE: by passes authentication and returns admin user as authenticated
        # user on development
        if is_development():
            current_user: Optional[UserModel] = get_admin_user()
            return func(current_user, *args, **kwargs)

        if 'x-access-token' in request.headers:
            token: Optional[str] = request.headers['x-access-token']
            if bool(token):
                try:
                    uid: Optional[str] = decode_auth_token(auth_token=token)
                    if bool(uid):
                        user_instance: Optional[UserModel] = get_user(uid=uid)
                        if isinstance(user_instance, UserModel):
                            current_user: UserModel = user_instance
                    else:
                        pass
                except jwt.DecodeError:
                    # If user not logged in do nothing
                    pass
            else:
                pass
        return func(current_user, *args, **kwargs)
    return decorated


if __name__ == '__main__':
    """
        NOTE: fast testing of functions here 
    """
    pass

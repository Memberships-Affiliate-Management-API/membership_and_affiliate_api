"""
    handle users and admin authentication
"""
import datetime
import os
from typing import Optional
import jwt
import requests
from flask import current_app, request, redirect, url_for, flash
from functools import wraps
from config import config_instance
from utils import is_development


# noinspection PyUnusedLocal
def check_jwt_token(auth_token: str) -> bool:
    """
        TODO - handle JWT authentication
    :param auth_token:
    :return:
    """
    return True


# noinspection PyUnusedLocal
def check_firebase_uid(uid: str) -> bool:
    """
        TODO - handle firebase authentication
    :param uid:
    :return:
    """
    return True


def get_admin_user() -> dict:
    """
        **get_admin_user**
            return admin_user - uses include on development server

        :return: dict
    """
    if is_development():
        admin_email, cell, names, organization_id, password, surname, uid = get_config_admin_user_details()
    else:
        return get_admin_user_from_admin_api()

    return dict(uid=uid, organization_id=organization_id, email=admin_email, names=names, surname=surname,
                cell=cell, password=password, is_admin=True)


def get_admin_user_from_admin_api() -> Optional[dict]:
    """
        **get_api_admin_user_details**
            fetch api admin user details from back-end

    :return: dict -> as user
    """
    _endpoint: str = '_api/v1/admin/users/get'
    _base_url: str = config_instance.BASE_URL
    _url: str = f'{_base_url}{_endpoint}'
    _secret_key: str = config_instance.SECRET_KEY
    _auth_token: str = encode_auth_token(uid=_secret_key)
    _organization_id: str = config_instance.ORGANIZATION_ID
    _uid: str = config_instance.ADMIN_UID
    user_data: dict = dict(SECRET_KEY=_secret_key, auth_token=_auth_token,
                           organization_id=_organization_id, uid=_uid)

    _headers = dict(content_type='application/json', domain=config_instance.ADMIN_APP_BASEURL)
    response = requests.post(url=_url, json=user_data, headers=_headers)

    response_data: dict = response.json()

    if response_data.get('status') is True:
        return response_data.get('payload')
    return None


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
        return current_user and current_user.get('uid') and (current_user.get('organization_id') == config_instance.ORGANIZATION_ID)

    return current_user and current_user.uid and (current_user.organization_id == config_instance.ORGANIZATION_ID)


def encode_auth_token(uid: str, expiration_days: int = 0) -> Optional[str]:
    """
    **encode_auth_token**
        Generates the Auth Token for JWT Authentication

    **PARAMETERS**
        :param: uid -> string - unique user id
        :return: string -> auth-token
    """
    try:
        _payload: dict = dict(exp=datetime.datetime.utcnow() + datetime.timedelta(days=expiration_days, minutes=30, seconds=5),
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


def send_get_user_request(uid: str) -> Optional[dict]:
    """
    **send_get_user_request**
        send request for user over api and return user dict

    **PARAMETERS**
        :param uid:
        :return: dict -> user record
    """
    _base_url: str = os.environ.get("BASE_URL")
    _user_endpoint: str = "_api/v1/client/users/get-user"
    response = requests.post(url=f"{_base_url}{_user_endpoint}", json=dict(uid=uid))
    response_data: dict = response.json()
    if response_data['status']:
        return response_data['payload']
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
            current_user: Optional[dict] = get_admin_user()
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
        current_user: Optional[dict] = send_get_user_request(uid=uid)
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
        current_user: Optional[dict] = None
        # NOTE: by passes authentication and returns admin user as authenticated
        # user on development
        if is_development():
            # TODO use api here instead of user model

            current_user: Optional[dict] = get_admin_user()
            return func(current_user, *args, **kwargs)

        if 'x-access-token' in request.headers:
            token: Optional[str] = request.headers['x-access-token']
            if bool(token):
                try:
                    uid: Optional[str] = decode_auth_token(auth_token=token)
                    if bool(uid):
                        user_instance: Optional[dict] = send_get_user_request(uid=uid)
                        if isinstance(user_instance, dict):
                            current_user: dict = user_instance
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

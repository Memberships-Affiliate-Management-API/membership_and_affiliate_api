***REMOVED***
    handle users and admin authentication
***REMOVED***
from flask import request
from config.exception_handlers import handle_view_errors
from config.exceptions import UnAuthenticatedError
from config.use_context import use_context
import functools


def check_jwt_token(auth_token: str) -> bool:
    ***REMOVED***
        TODO - handle JWT authentication
    :param auth_token:
    :return:
    ***REMOVED***
    return True


def check_firebase_uid(uid: str) -> bool:
    ***REMOVED***
        TODO - handle firebase authentication
    :param uid:
    :return:
    ***REMOVED***
    return True


def handle_users_auth(func):
    @functools.wraps(func)
    def auth_wrapper(*args, **kwargs):

        auth_token: str = request.headers.get('auth-token')
        uid: str = request.headers.get('uid')

        if check_jwt_token(auth_token=auth_token):
            return func(*args, **kwargs)

        if check_firebase_uid(uid=uid):
            return func(*args, **kwargs)

        message: str = "request not authorized"
        raise UnAuthenticatedError(status=401, description=message)

    return auth_wrapper

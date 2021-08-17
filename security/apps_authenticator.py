***REMOVED***
    **apps_authenticator**
        will handle internal application api cals

***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
from typing import Optional
import requests
from flask import request
from config import config_instance
from config.exceptions import UnAuthenticatedError, error_codes
import functools
from main import app_cache


@app_cache.memoize(timeout=16*60)
def is_app_authenticated(domain: str, secret_key: str, auth_token: str) -> bool:
    ***REMOVED***
        **apps_authenticator**
            authenticate application to api calls
    :param domain:
    :param secret_key:
    :param auth_token:
    :return:
    ***REMOVED***
    pass


def handle_apps_authentication(func):
    @functools.wraps(func)
    def auth_wrapper(*args, **kwargs):
        domain: Optional[str] = request.headers.get('domain')
        secret_key: Optional[str] = kwargs.get('SECRET_KEY')
        auth_token: Optional[str] = kwargs.get('auth_token')

        if is_app_authenticated(domain=domain, secret_key=secret_key, auth_token=auth_token):
            return func(*args, **kwargs)
        message: str = "request not authorized"
        raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)
    return auth_wrapper

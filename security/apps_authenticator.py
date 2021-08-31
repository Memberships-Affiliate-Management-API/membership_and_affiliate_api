***REMOVED***
    **apps_authenticator**
        will handle internal application api calls

    **NOTE:**
        this authenticator runs on the api side will have access to all the data classes

***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import hmac
from typing import Optional
import requests
from flask import request
from config import config_instance
from config.exceptions import UnAuthenticatedError, error_codes
import functools
from config.use_context import use_context
from main import app_cache
from database.app_authenticator import MicroAuthDetails
from utils import is_development, return_ttl


@use_context
@app_cache.memoize(timeout=return_ttl('short'))
def is_app_authenticated(domain: str, secret_key: str, auth_token: str) -> bool:
    ***REMOVED***
        **apps_authenticator**
            authenticate application to api calls
    :param domain:
    :param secret_key:
    :param auth_token:
    :return: True
    ***REMOVED***
    # TODO use system database to get details for authenticated applications
    if not is_development():
        compare_auth_token: bool = False
        app_auth_details: MicroAuthDetails = MicroAuthDetails.query(MicroAuthDetails.domain == domain).get()
        if isinstance(app_auth_details, MicroAuthDetails) and app_auth_details.domain == domain:
            compare_auth_token: bool = hmac.compare_digest(auth_token, app_auth_details.auth_token)

        compare_admin_domain: bool = hmac.compare_digest(domain, config_instance.ADMIN_APP_BASEURL)
        compare_client_domain: bool = hmac.compare_digest(domain, config_instance.CLIENT_APP_BASEURL)
        compare_secret_key: bool = hmac.compare_digest(secret_key, config_instance.SECRET_KEY)

        return compare_secret_key and compare_client_domain and compare_admin_domain and compare_auth_token
    return True


def handle_apps_authentication(func):
    @functools.wraps(func)
    def auth_wrapper(*args, **kwargs):
        domain: Optional[str] = request.headers.get('Referrer')
        secret_key: Optional[str] = kwargs.get('SECRET_KEY')
        auth_token: Optional[str] = kwargs.get('auth_token')
        print(f"domain: {domain}, secret_key: {secret_key}, auth_token: {auth_token}")

        if not is_development() and ("localhost" in domain or "127.0.0.1" in domain):
            message: str = "request not authorized"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        if is_app_authenticated(domain=domain, secret_key=secret_key, auth_token=auth_token):
            return func(*args, **kwargs)
        message: str = "request not authorized"
        raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

    return auth_wrapper

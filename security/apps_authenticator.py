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


def verify_app_id(app_id: str, domain: str) -> bool:
    ***REMOVED***
    **verify_app_id**
        given a micro-services domain name check if the app_id is the same as the app_id
        created
    :param app_id:
    :param domain:
    :return:
    ***REMOVED***
    _endpoint: str = '_ipn/micro-services/verify-app-id'
    _url: str = f"{domain}{_endpoint}"
    _secret_key: str = config_instance.SECRET_KEY
    _kwargs: dict = dict(domain=domain, app_id=app_id, secret_key=_secret_key)
    _result = requests.post(url=_url, json=_kwargs)
    json_data: dict = _result.json()
    compare_secret_key: bool = hmac.compare_digest(_secret_key,json_data.get('secret_key'))
    compare_app_id: bool = hmac.compare_digest(app_id, json_data.get('app_id'))
    return json_data.get('status') and compare_secret_key and compare_app_id


@use_context
@app_cache.memoize(timeout=return_ttl('short'))
def is_app_authenticated(domain: Optional[str], secret_key: Optional[str],
                         auth_token: Optional[str]) -> bool:
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

        # NOTE: this is an applications Authentication Token not users Authentication Token
        compare_auth_token: bool = False
        # NOTE: ON launching the application to be live create MicroAuthDetails on main database
        # NOTE:  after every authentication save auth token on live database
        app_auth_details: MicroAuthDetails = MicroAuthDetails.query(MicroAuthDetails.domain == domain).get()
        compare_domain: bool = hmac.compare_digest(domain, app_auth_details.domain)

        if isinstance(app_auth_details, MicroAuthDetails) and compare_domain:
            compare_auth_token: bool = hmac.compare_digest(auth_token, app_auth_details.auth_token)

        compare_admin_domain: bool = hmac.compare_digest(domain, config_instance.ADMIN_APP_BASEURL)
        compare_client_domain: bool = hmac.compare_digest(domain, config_instance.CLIENT_APP_BASEURL)
        compare_secret_key: bool = hmac.compare_digest(secret_key, config_instance.SECRET_KEY)

        # NOTE if either admin domain or client domain is the same as is known then proceed
        return compare_secret_key and (compare_client_domain or compare_admin_domain) and compare_auth_token

    return True


def handle_apps_authentication(func):
    @functools.wraps(func)
    def auth_wrapper(*args, **kwargs):
        domain: Optional[str] = kwargs.get('domain')
        secret_key: Optional[str] = request.headers.get('SECRET_KEY')
        auth_token: Optional[str] = kwargs.get('token')
        print(f"domain: {domain}, secret_key: {secret_key}, auth_token: {auth_token}")

        if not is_development() and ("localhost" in domain or "127.0.0.1" in domain):
            message: str = "request not authorized"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        if is_app_authenticated(domain=domain, secret_key=secret_key, auth_token=auth_token):
            return func(*args, **kwargs)
        message: str = "request not authorized"
        raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

    return auth_wrapper

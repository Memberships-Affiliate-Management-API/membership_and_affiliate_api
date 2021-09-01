***REMOVED***
    **apps_authenticator**
        will handle internal application api calls

    **NOTE:**
        this authenticator runs on the api side will have access to all the data classes

***REMOVED***
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

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
from security.users_authenticator import decode_auth_token
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

    if not json_data.get('status'):
        # TODO if app not authenticated adding the ip address to a black list may be a good idea
        message: str = "application un-authenticated"
        raise UnAuthenticatedError(description=message)

    _payload: dict = json_data.get('payload')

    # Note: comparing a known secret_key with the returned secret_key
    compare_secret_key: bool = hmac.compare_digest(_secret_key, _payload.get('secret_key'))

    compare_app_id: bool = hmac.compare_digest(app_id, _payload.get('app_id'))
    return json_data.get('status') and compare_secret_key and compare_app_id


@use_context
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
    decoded_token = decode_auth_token(auth_token=auth_token)
    if not bool(decoded_token):
        return False
    _domain, _secret_key, _app_id = decoded_token.split('#')
    print(f"DOMAIN: {domain} SECRET_KEY: {secret_key}, app_id: {_app_id}")
    domain = f"{domain}/" if not domain.endswith("/") else domain

    compare_secret_key: bool = hmac.compare_digest(_secret_key, secret_key)
    compare_domain: bool = hmac.compare_digest(_domain, domain)
    print(f"domain : {domain}, _domain: {_domain}")

    return compare_secret_key and compare_domain and verify_app_id(app_id=_app_id, domain=_domain)


def handle_apps_authentication(func):
    @functools.wraps(func)
    def auth_wrapper(*args, **kwargs):
        json_data: dict = request.get_json()
        domain: Optional[str] = json_data.get('domain')
        secret_key: Optional[str] = json_data.get('SECRET_KEY')
        auth_token: Optional[str] = json_data.get('app_token')
        print(f"Domain: {domain}, Secret_key: {secret_key}, Auth_token: {auth_token}")

        if not is_development() and ("localhost" in domain or "127.0.0.1" in domain):
            message: str = "request not authorized"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        if is_app_authenticated(domain=domain, secret_key=secret_key, auth_token=auth_token):
            return func(*args, **kwargs)
        message: str = "request not authorized"
        raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

    return auth_wrapper


def is_domain_authorised(domain) -> bool:
    pass

"""
    **apps_authenticator**
        will handle internal application api calls

    **NOTE:**
        this authenticator runs on the api side will have access to all the data classes

"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

import functools
import hmac
from typing import Optional, Callable, List

import requests
from flask import request

from config import config_instance
from config.exceptions import UnAuthenticatedError, error_codes, status_codes
from config.use_context import use_context
from security.users_authenticator import decode_auth_token
from utils import is_development


def verify_secret_key(secret_key: str) -> None:
    if not hmac.compare_digest(secret_key, config_instance.SECRET_KEY):
        message: str = "User not Authorized: you are not authorized to call this API"
        raise UnAuthenticatedError(
            status=error_codes.un_auth_error_code, description=message)


def debug_verify_app_id(_result, domain):
    pass


def verify_app_id(app_id: str, domain: str) -> bool:
    """
    **verify_app_id**
        given a micro-services domain name check if the app_id is the same as the app_id
        created
    :param app_id:
    :param domain:
    :return:
    """
    _endpoint: str = '_ipn/micro-services/verify-app-id'
    _url: str = f"{domain}{_endpoint}"

    _secret_key: str = config_instance.SECRET_KEY
    _kwargs: dict = dict(domain=domain, app_id=app_id, SECRET_KEY=_secret_key)

    _result: requests.Response = requests.post(url=_url, json=_kwargs)
    _ok_codes: List[int] = [
        status_codes.successfully_updated_code, status_codes.status_ok_code]
    if _result.status_code in _ok_codes and _result.headers['content-type'] == 'application/json':
        json_data: dict = _result.json()
    else:
        debug_verify_app_id(_result, domain)
        message: str = 'Application not authenticated'
        raise UnAuthenticatedError(description=message)

    if not json_data.get('status'):
        # TODO if app not authenticated adding the ip address to a black list may be a good idea
        message: str = "application un-authenticated"
        raise UnAuthenticatedError(description=message)

    _payload: dict = json_data.get('payload')

    # Note: comparing a known secret_key with the returned secret_key
    compare_secret_key: bool = hmac.compare_digest(
        _secret_key, _payload.get('SECRET_KEY'))

    compare_app_id: bool = hmac.compare_digest(app_id, _payload.get('app_id'))
    return json_data.get('status') and compare_secret_key and compare_app_id


@use_context
def is_app_authenticated(domain: Optional[str], secret_key: Optional[str],
                         auth_token: Optional[str]) -> bool:
    """
        **apps_authenticator**
            authenticate application to api calls
    :param domain:
    :param secret_key:
    :param auth_token:
    :return: True
    """
    decoded_token = decode_auth_token(auth_token=auth_token)
    if not bool(decoded_token):

        return False

    _domain, _secret_key, _app_id = decoded_token.split('#')

    domain = f"{domain}/" if not domain.endswith("/") else domain
    if is_development() and domain == 'http://localhost:8082/':
        domain = 'http://127.0.0.1:8082/'

    compare_secret_key: bool = hmac.compare_digest(_secret_key, secret_key)
    compare_domain: bool = hmac.compare_digest(_domain, domain)

    return compare_secret_key and compare_domain and verify_app_id(app_id=_app_id, domain=_domain)


def handle_apps_authentication(func: Callable) -> Callable:
    # noinspection DuplicatedCode
    @functools.wraps(func)
    def auth_wrapper(*args, **kwargs) -> Callable:
        json_data: dict = request.get_json()
        domain: Optional[str] = json_data.get('domain')
        secret_key: Optional[str] = json_data.get('SECRET_KEY')
        auth_token: Optional[str] = json_data.get('app_token')
        # print(f"Domain: {domain}, Secret_key: {secret_key}, Auth_token: {auth_token}")
        if domain is None:
            # print(f'domain is Null: {domain}')
            message: str = "request not authorized"
            raise UnAuthenticatedError(
                status=error_codes.un_auth_error_code, description=message)
        if secret_key is None:
            # print(f'secret_key is Null: {secret_key}')
            message: str = "request not authorized"
            raise UnAuthenticatedError(
                status=error_codes.un_auth_error_code, description=message)

        if auth_token is None:
            # print(f'auth_token is Null: {auth_token}')
            message: str = "request not authorized"
            raise UnAuthenticatedError(
                status=error_codes.un_auth_error_code, description=message)

        if not is_development() and ("localhost" in domain or "127.0.0.1" in domain):
            message: str = "request not authorized: local-development"
            raise UnAuthenticatedError(
                status=error_codes.un_auth_error_code, description=message)

        if is_app_authenticated(domain=domain, secret_key=secret_key, auth_token=auth_token):
            return func(*args, **kwargs)
        message: str = "request not authorized- app not authenticated"
        raise UnAuthenticatedError(
            status=error_codes.un_auth_error_code, description=message)

    return auth_wrapper


def handle_internal_auth(func: Callable) -> Callable:
    """
    **handle_internal_auth**
        handles authentication of internal api calls

    :param func:
    :return:
    """

    @functools.wraps(func)
    def auth_wrapper(*args, **kwargs) -> Callable:
        # TODO - finish up internal authentication
        return func(*args, **kwargs)

    return auth_wrapper


def verify_cron_job(cron_domain: str, secret_key: str) -> bool:
    """verify if the executor of the cron job is authorized"""
    is_domain: bool = hmac.compare_digest(
        cron_domain, config_instance.CRON_DOMAIN)
    is_secret: bool = hmac.compare_digest(
        secret_key, config_instance.CRON_SECRET)
    return is_domain and is_secret


def handle_cron_auth(func: Callable) -> Callable:
    """authenticate cron job execution routes"""

    @functools.wraps(func)
    def auth_wrapper(*args, **kwargs) -> Callable:
        json_data: dict = request.get_json()
        _cron_domain: Optional[str] = json_data.get('domain')
        _secret_key: Optional[str] = json_data.get('SECRET_KEY')

        if _cron_domain is None:
            # print(f'cron domain is Null: {_cron_domain}')
            message: str = "request not authorized"
            raise UnAuthenticatedError(
                status=error_codes.un_auth_error_code, description=message)

        if _secret_key is None:
            # print(f'secret key is Null: {_secret_key}')
            message: str = "request not authorized"
            raise UnAuthenticatedError(
                status=error_codes.un_auth_error_code, description=message)

        if verify_cron_job(cron_domain=_cron_domain, secret_key=_secret_key):
            return func(*args, **kwargs)
        message: str = "request not authorized"
        raise UnAuthenticatedError(
            status=error_codes.un_auth_error_code, description=message)

    return auth_wrapper


def is_domain_authorised(domain) -> bool:
    """
    :param domain:
    :return:
    """
    pass

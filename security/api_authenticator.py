"""
    **API Authenticator Module**
        authorize client api calls
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from typing import Optional
from flask import request
import functools
import hmac
from config import config_instance
from config.exceptions import UnAuthenticatedError, error_codes, RemoteDataError
from cache.cache_manager import app_cache
from views import api_keys_view


@app_cache.cache.memoize(timeout=15 * 60, cache_none=False)  # timeout equals fifteen minutes // 900 seconds
def is_request_valid(api_key: str, secret: str, domain: str) -> bool:
    """
    **is_api_key_valid**
        validates api keys on behalf of client api calls

    :param api_key: str -> api_key to check
    :param secret: str -> secret token
    :param domain: str -> domain registered for the api_key and secret_token
    :return: bool -> True if api_key is valid
    """

    organization_id: str = config_instance.ORGANIZATION_ID
    response = api_keys_view.get_api_key(api_key=api_key, organization_id=organization_id)

    response_data, status_code = response
    response_dict = response_data.get_json()

    if not response_dict.get('status'):
        return False

    api_instance: dict = response_dict.get('payload')
    if not isinstance(api_instance, dict):
        return False

    domain: str = domain.lower().strip()
    # NOTE accessing the keys this way will throw ValueError if keys are not available which is what we want
    is_secret_valid: bool = hmac.compare_digest(api_instance['secret_token'], secret)
    is_domain_valid: bool = hmac.compare_digest(api_instance['domain'], domain)
    _request_valid: bool = is_secret_valid and is_domain_valid

    return not not api_instance.get('is_active') if _request_valid else False


def handle_api_auth(func):
    """
    **handle_api_auth**
        wrapper to handle public api calls authentications

    :param func: a function to be wrapped
    :return: wrapped function
    """

    # noinspection DuplicatedCode
    @functools.wraps(func)
    def auth_wrapper(*args, **kwargs):
        api_key: Optional[str] = request.headers.get('x-api-key')
        secret_token: Optional[str] = request.headers.get('x-secret-token')
        domain: Optional[str] = request.base_url

        if api_key is None:
            print(f'api_key is Null: {api_key}')
            message: str = "request not authorized"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        if secret_token is None:
            print(f'secret_token is Null: {secret_token}')
            message: str = "request not authorized"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        if domain is None:
            print(f'domain is Null: {domain}')
            message: str = "request not authorized"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        if is_request_valid(api_key=api_key, secret=secret_token, domain=domain):
            return func(*args, **kwargs)
        message: str = "request not authorized"
        raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

    return auth_wrapper


if __name__ == '__main__':
    """
        NOTE: fast testing of functions here 
    """
    pass

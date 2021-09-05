***REMOVED***
    **API Authenticator Module**
        authorize client api calls
***REMOVED***
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from typing import Optional
import requests
from flask import request
from config import config_instance
from config.exceptions import UnAuthenticatedError, error_codes, RemoteDataError
import functools
from cache.cache_manager import app_cache


@app_cache.cache.memoize(timeout=15 * 60)  # timeout equals fifteen minutes // 900 seconds
def is_request_valid(api_key: str, secret: str, domain: str) -> bool:
    ***REMOVED***
    **is_api_key_valid**
        validates api keys on behalf of client api calls

    :param api_key: str -> api_key to check
    :param secret: str -> secret token
    :param domain: str -> domain registered for the api_key and secret_token
    :return: bool -> True if api_key is valid
    ***REMOVED***

    organization_id: str = config_instance.ORGANIZATION_ID
    _endpoint = f'_api/admin/api-keys/{api_key}/org/{organization_id}'
    _url: str = f'{config_instance.BASE_URL}{_endpoint}'

    try:
        response = requests.post(url=_url, json=dict(SECRET_KEY=config_instance.SECRET_KEY))
    except requests.ConnectionError:
        message: str = 'Remote Error: Failed to verify app id- Could not communicate to app server'
        raise RemoteDataError(description=message, url=_url)
    except requests.Timeout:
        message: str = 'Remote Error: Failed to verify app id- Could not communicate to app server'
        raise RemoteDataError(description=message, url=_url)

    response_dict: dict = response.json()

    if not response_dict.get('status'):
        return False

    api_instance: dict = response_dict.get('payload')
    if not isinstance(api_instance, dict):
        return False

    domain: str = domain.lower().strip()
    _request_valid: bool = (api_instance['secret_token'] == secret) and (api_instance['domain'] == domain)

    return api_instance['is_active'] if _request_valid else False


def handle_api_auth(func):
    ***REMOVED***
    **handle_api_auth**
        wrapper to handle public api calls authentications

    :param func: a function to be wrapped
    :return: wrapped function
    ***REMOVED***

    @functools.wraps(func)
    def auth_wrapper(*args, **kwargs):
        api_key: Optional[str] = request.headers.get('api-key')
        secret_token: Optional[str] = request.headers.get('secret-token')
        domain: Optional[str] = request.base_url
        # TODO check which domain is making the request - this may not be True

        if is_request_valid(api_key=api_key, secret=secret_token, domain=domain):
            return func(*args, **kwargs)
        message: str = "request not authorized"
        raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

    return auth_wrapper


if __name__ == '__main__':
    ***REMOVED***
        NOTE: fast testing of functions here 
    ***REMOVED***
    pass

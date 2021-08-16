***REMOVED***
    **API Authenticator Module**
        authorize client api calls
***REMOVED***
import json

import requests
from flask import request
from config import config_instance
from config.exceptions import UnAuthenticatedError
import functools
from main import app_cache
from utils.utils import return_ttl


@app_cache.memoize(timeout=return_ttl('short'))
def is_api_key_valid(api_key: str, secret: str, domain: str) -> bool:
    ***REMOVED***
        **is_api_key_valid**
            validates api keys on behalf of client api calls

    :param api_key:
    :param secret:
    :param domain:
    :return:
    ***REMOVED***
    # TODO: Use api call to api keys
    organization_id: str = config_instance.ORGANIZATION_ID
    _endpoint = '_api/admin/api-keys/{}/org/{}'.format(api_key, organization_id)
    _url: str = "{}{}".format(config_instance.BASE_URL, _endpoint)

    response = requests.post(url=_url, json=dict(SECRET_KEY=config_instance.SECRET_KEY))
    response_dict: dict = response.json()

    if response_dict['status']:
        api_instance: dict = response_dict['payload']
        if isinstance(api_instance, dict):
            if (api_instance['secret_token'] == secret) and (api_instance['domain'] == domain):
                return api_instance['is_active']
        return False


def handle_api_auth(func):
    @functools.wraps(func)
    def auth_wrapper(*args, **kwargs):
        api_key: str = request.headers.get('api-key')
        secret_token: str = request.headers.get('secret-token')
        domain: str = request.base_url

        if is_api_key_valid(api_key=api_key, secret=secret_token, domain=domain):
            return func(*args, **kwargs)
        message: str = "request not authorized"
        raise UnAuthenticatedError(status=401, description=message)

    return auth_wrapper


# NOTE: this is irrelevant
@handle_api_auth
def main():
    pass


if __name__ == '__main__':
    ***REMOVED***
        NOTE: fast testing of functions here 
    ***REMOVED***
    main()

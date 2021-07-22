***REMOVED***
    authorize api calls
***REMOVED***
from flask import request
from config.exceptions import UnAuthenticatedError
from config.use_context import use_context
import functools
from database.apikeys import APIKeys


@use_context
@functools.cache
def is_api_key_valid(api_key: str, secret: str) -> bool:
    api_instance: APIKeys = APIKeys.query(APIKeys.api_key == api_key).get()
    if isinstance(api_instance, APIKeys):
        if api_instance.secret_token == secret:
            return api_instance.is_active
    return False


@functools.lru_cache(maxsize=1024)
def handle_auth(func):
    @functools.wraps(func)
    def auth_wrapper(*args, **kwargs):
        api_key = request.headers.get('api-key')
        secret = request.headers.get('secret')
        # TODO verify request domain
        api_key_valid: bool = is_api_key_valid(api_key=api_key, secret=secret)
        if api_key_valid:
            return func(*args, **kwargs)
        message: str = "request not authorized"
        raise UnAuthenticatedError(status=401, description=message)

    return auth_wrapper

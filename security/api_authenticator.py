***REMOVED***
    authorize api calls
***REMOVED***
from flask import request
from config.exception_handlers import handle_view_errors
from config.exceptions import UnAuthenticatedError
from config.use_context import use_context
import functools
from database.apikeys import APIKeys


@use_context
@functools.lru_cache(maxsize=1024)
@handle_view_errors
def is_api_key_valid(api_key: str, secret: str, domain: str) -> bool:
    api_instance: APIKeys = APIKeys.query(APIKeys.api_key == api_key).get()
    if isinstance(api_instance, APIKeys):
        if (api_instance.secret_token == secret) and (api_instance.domain == domain):
            return api_instance.is_active
    return False


def handle_api_auth(func):
    @functools.wraps(func)
    def auth_wrapper(*args, **kwargs):
        api_key: str = request.headers.get('api-key')
        secret: str = request.headers.get('secret')
        domain: str = request.base_url
        print(f"domain: {domain} secret: {secret} api key: {api_key}")
        if is_api_key_valid(api_key=api_key, secret=secret, domain=domain):
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

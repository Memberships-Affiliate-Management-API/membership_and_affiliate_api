"""
    **Wrappers for common application exceptions**
    Used on views to handle common method errors when accessing ndb databases

"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import functools
from typing import Callable, Optional

from google.api_core.exceptions import Aborted, RetryError
from google.cloud.ndb.exceptions import BadRequestError, BadQueryError
from config.exceptions import InputError, RequestError, DataServiceError, error_codes
from flask import current_app


def handle_view_errors(func):
    """
        view error handler wrapper
    #     TODO - raise user related errors here
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        debug: bool = current_app.config.get('DEBUG')
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            message: str = str(e)
            if debug:
                print(message)
            raise InputError(
                status=error_codes.input_error_code, description=message)
        except TypeError as e:
            message: str = str(e)
            if debug:
                print(e)
            raise InputError(
                status=error_codes.input_error_code, description=message)
        except BadRequestError as e:
            if debug:
                print(e)
            message: str = '''Bad Request: while connecting to database'''
            raise RequestError(
                status=error_codes.bad_request_error_code, description=message)
        except BadQueryError as e:
            if debug:
                print(e)
            message: str = '''Database Query Error: Error while querying database please inform admin'''
            raise DataServiceError(
                status=error_codes.data_service_error_code, description=message)
        except ConnectionRefusedError as e:
            if debug:
                print(e)
            message: str = '''Connection Refused: Unable to connect to database please try again later'''
            raise RequestError(
                status=error_codes.remote_data_error, description=message)
        except RetryError as e:
            if debug:
                print(e)
            message: str = '''Retries Exceeded: Unable to connect to database please try again later 
            or inform the administrator'''
            raise RequestError(
                status=error_codes.remote_data_error, description=message)
        except Aborted as e:
            if debug:
                print(e)
            message: str = '''Abort Error: connection refused by remote server'''
            raise RequestError(
                status=error_codes.remote_data_error, description=message)

    return wrapper


def handle_store_errors(func: Callable) -> Callable:
    """
        handle errors related to GCP datastore
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Optional[Callable]:
        debug: bool = current_app.config.get('DEBUG')
        try:
            return func(*args, **kwargs)
        except ConnectionRefusedError as e:
            if debug:
                print(str(e))
            return None
        except RetryError as e:
            if debug:
                print(str(e))
            return None
        except Aborted as e:
            if debug:
                print(str(e))
            return None
        except BadQueryError as e:
            if debug:
                print(str(e))
            return None
        except BadRequestError as e:
            if debug:
                print(str(e))
            return None

    return wrapper


def handle_requests_errors(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Callable:
        return func(*args, **kwargs)

    return wrapper


if __name__ == '__main__':
    """
        NOTE: fast testing of functions here 
    """
    pass

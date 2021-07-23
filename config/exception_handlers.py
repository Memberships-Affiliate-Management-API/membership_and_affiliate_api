import functools
from flask import jsonify
from google.api_core.exceptions import Aborted, RetryError
from google.cloud.ndb.exceptions import BadRequestError, BadQueryError
from config.exceptions import InputError, RequestError, DataServiceError


def handle_view_errors(func):
    ***REMOVED***
        view error handler wrapper
    #     TODO - raise user related errors here
    ***REMOVED***
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            message: str = str(e)
            # IF debug please print debug messages
            # raise InputError(description='Bad input values, please check your input')
            return({'status': False, 'message': message}), 500
        except TypeError as e:
            message: str = str(e)
            raise InputError(status=500, description='InputError: Bad input values, please check your input')
        except BadRequestError as e:
            message: str = str(e)
            raise RequestError(status=500, description='Bad Request: while connecting to database')
        except BadQueryError as e:
            message: str = str(e)
            raise DataServiceError(status=500, description="Database Error: Error while querying database please inform admin")
        except ConnectionRefusedError as e:
            message: str = str(e)
            raise RequestError(status=500, description="Request Error: Unable to connect to database please try again later")
        except RetryError as e:
            message: str = str(e)
            raise RequestError(status=500, description="Request error: Unable to connect to database please try again later")
        except Aborted as e:
            message: str = str(e.message or e)
            raise RequestError(status=500, description="Abort Error: due to some error on our servers your connection was aborted try again later")

    return wrapper


def handle_store_errors(func):
    ***REMOVED***
        handle errors related to GCP datastore
    ***REMOVED***
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        except Aborted:
            return None
        except BadQueryError:
            return None
        except BadRequestError:
            return None

    return wrapper

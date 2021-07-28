import functools
from google.api_core.exceptions import Aborted, RetryError
from google.cloud.ndb.exceptions import BadRequestError, BadQueryError
from config.exceptions import InputError, RequestError, DataServiceError
from flask import current_app


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
            raise InputError(status=500, description=message)
        except TypeError as e:
            message: str = str(e)
            if current_app.config.get('DEBUG'):
                print(e)
            raise InputError(status=500, description=message)
        except BadRequestError as e:
            if current_app.config.get('DEBUG'):
                print(e)
            message: str = '''<code>Bad Request:</code> while connecting to database'''
            raise RequestError(status=500, description=message)
        except BadQueryError as e:
            if current_app.config.get('DEBUG'):
                print(e)
            message: str = '''<code>Database Query Error:</code> Error while querying database please inform admin'''
            raise DataServiceError(status=500, description=message)
        except ConnectionRefusedError as e:
            if current_app.config.get('DEBUG'):
                print(e)
            message: str = '''<code>Connection Refused:</code> Unable to connect to database please try again later'''
            raise RequestError(status=500, description=message)
        except RetryError as e:
            if current_app.config.get('DEBUG'):
                print(e)
            message: str = '''<code>Retries Exceeded:</code> Unable to connect to database please try again later 
            or inform the administrator'''
            raise RequestError(status=500, description=message)
        except Aborted as e:
            if current_app.config.get('DEBUG'):
                print(e)
            message: str = '''<code>Abort Error:</code> due to some error on our servers your connection 
            was aborted try again later'''
            raise RequestError(status=500, description=message)

    return wrapper


def handle_store_errors(func):
    ***REMOVED***
        handle errors related to GCP datastore
    ***REMOVED***
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionRefusedError as e:
            if current_app.config.get('DEBUG'):
                print(e)
            return None
        except RetryError as e:
            if current_app.config.get('DEBUG'):
                print(e)
            return None
        except Aborted as e:
            if current_app.config.get('DEBUG'):
                print(e)
            return None
        except BadQueryError as e:
            if current_app.config.get('DEBUG'):
                print(e)
            return None
        except BadRequestError as e:
            if current_app.config.get('DEBUG'):
                print(e)
            return None

    return wrapper


if __name__ == '__main__':
    ***REMOVED***
        NOTE: fast testing of functions here 
    ***REMOVED***
    pass

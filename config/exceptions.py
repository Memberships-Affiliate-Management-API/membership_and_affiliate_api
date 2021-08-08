***REMOVED***
    **Custom Exception Definitions, Error Codes and Status Codes **

***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import typing
from werkzeug.exceptions import HTTPException, BadRequest


class ErrorCodes:
    ***REMOVED***
        definitions of error codes, for errors that can be raised in Memberships & Affiliates Management API
        this is in-case requests are not completed successfully
    ***REMOVED***

    def __init__(self) -> None:
        self.input_error_code: int = 422
        self.data_service_error_code: int = 512
        self.un_auth_error_code: int = 401
        # 404 means our server never found the resource associated with the requested
        self.request_not_found_error_code: int = 404
        self.remote_data_error: int = 406
        self.environment_error_code: int = 506
        self.bad_request_error_code: int = 400
        self.payment_required_error_code: int = 402
        self.access_forbidden_error_code: int = 403
        self.not_acceptable_response_error_code: int = 406
        self.teapot_error_code: int = 418
        self.too_many_requests_error_code: int = 429
        self.resource_conflict_error_code: int = 429
        self.server_error_code: int = 500
        self.not_implemented_error_code: int = 501
        self.server_overload_error_code: int = 503
        self.server_timed_out_error_code: int = 504
        self.resource_limit_reached_error_code: int = 508
        self.authentication_required_error_code: int = 511
        self.server_is_down_error_code: int = 521


class StatusCodes:
    ***REMOVED***
        a list of status codes to be returned when request was successfully completed
    ***REMOVED***

    def __init__(self):
        self.data_not_found_code: int = 204
        self.successfully_updated_code: int = 201
        self.status_ok_code: int = 200


error_codes: ErrorCodes = ErrorCodes()
status_codes: StatusCodes = StatusCodes()


class DataServiceError(HTTPException):
    ***REMOVED****401*
        raised when user has been performing an update or edit operation on their resource and the application
        is unable to complete such an operation.

    ***REMOVED***
    code: int = error_codes.data_service_error_code
    description: str = 'We have a problem connection to the Database'

    def __init__(self, status: typing.Union[int, None], description: typing.Union[str, None] = None):
        if bool(description):
            self.description = description
        if bool(status):
            self.code = status

        super(DataServiceError, self).__init__()

    def __str__(self) -> str:
        return "<DataServiceError {} Code: {}".format(self.description, str(self.code))

    def __repr__(self) -> str:
        return self.__str__()


class InputError(Exception):
    ***REMOVED****422*
        raised when a user has supplied bad data or invalid arguments, for example supplying a None / Null value instead
        of a string will result in this error being thrown
    ***REMOVED***
    code: int = error_codes.input_error_code
    description: str = "Unable to process input"

    def __init__(self, status: typing.Union[int, None] = None, description: typing.Union[None, str] = None):
        if bool(description):
            self.description = description
        if bool(status):
            self.code = status
        super(InputError, self).__init__()

    def __str__(self) -> str:
        return "<InputError {} Code: {}".format(self.description, str(self.code))

    def __repr__(self) -> str:
        return self.__str__()


class UnAuthenticatedError(HTTPException):
    ***REMOVED***
        in-case of an authentication error throw this error
    ***REMOVED***
    code: int = error_codes.un_auth_error_code
    description: str = "You are not authorized to use this resource"

    def __init__(self, status: typing.Union[int, None] = None,
                 description: typing.Union[None, str] = None):
        if bool(description):
            self.description = description

        if bool(status):
            self.code = status

        super(UnAuthenticatedError, self).__init__()

    def __str__(self) -> str:
        return "<UnAuthenticated {} Code: {}".format(self.description, str(self.code))

    def __repr__(self) -> str:
        return self.__str__()


class RequestError(HTTPException):
    ***REMOVED****404*
       raised when the server has created a request which succeeded but the response
       isn't what is expected or the remote server returns an error.
    ***REMOVED***
    code: int = error_codes.request_not_found_error_code
    description: str = "Request unsuccessful"

    def __init__(self, status: typing.Union[int, None] = None, description: typing.Union[str, None] = None,
                 url: typing.Union[str, None] = None):

        super(RequestError, self).__init__()

        if bool(description):
            self.description = description

        if bool(url):
            self.description = "{} on url: {}".format(description, url)

        if bool(status):
            self.code = status

    def __str__(self) -> str:
        return "<RequestError {} Code: {}".format(self.description, str(self.code))

    def __repr__(self) -> str:
        return self.__str__()


# Errors

class RemoteDataError(IOError):
    ***REMOVED*** *406*
        raised when the server is trying to access a remote server or service in order
        to complete the users transaction but is unable to . the proper response
        would be to retry the action that lead to this error.
    ***REMOVED***
    code: int = error_codes.remote_data_error
    description: str = 'Error connecting to remote server'
    url: str = ""

    def __init__(self, status: typing.Union[int, None] = 406,
                 description: typing.Union[str, None] = None, url: str = None):

        super(RemoteDataError, self).__init__()

        if bool(description):
            self.description = "{} {}".format(description, url)

        if bool(status):
            self.code = status

        if bool(url):
            self.url = url

    def __str__(self) -> str:
        return "<RemoteDataError {} Code: {}, URL: {}".format(self.description, str(self.code),
                                                              self.url)

    def __repr__(self) -> str:
        return self.__str__()


class EnvironNotSet(Exception):
    ***REMOVED***
        raised when environment variables are not set
    ***REMOVED***
    code: int = error_codes.environment_error_code
    description: str = "environment variables not set please inform admin"
    url: str = ""

    def __init__(self, status: typing.Union[int, None] = 406,
                 description: typing.Union[str, None] = None, url: str = None):

        super(EnvironNotSet, self).__init__()

        if bool(description) and bool(url):
            self.description = "{} {}".format(description, url)

        if bool(status):
            self.code = status

        if bool(url):
            self.url = url

    def __str__(self) -> str:
        return "<EnvironNotSet {} Code: {} Url: {}".format(self.description, str(self.code),
                                                           self.url)

    def __repr__(self) -> str:
        return self.__str__()


def if_bad_request_raise(request) -> None:
    content_type: str = request.headers.get('content-type')
    if not content_type.lower() == 'application/json':
        raise BadRequest(description="parameters for this end-point may only be in json format")

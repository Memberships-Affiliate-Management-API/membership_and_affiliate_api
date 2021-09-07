"""
    **Custom Exception Definitions**
        for handling application flow and enable the application to throw errors
    **Error Codes and Status Codes **
        named error codes and status codes to use on the application
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from typing import Optional
from werkzeug.exceptions import HTTPException, BadRequest


class ErrorCodes:
    """
        **Class ErrorCodes**
            definitions of error codes, for errors that can be raised in Memberships & Affiliates Management API
            this is in-case requests are not completed successfully
    """

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
    """
        **Class StatusCodes**
            a list of status codes to be returned when request was successfully completed
    """

    def __init__(self):
        self.data_not_found_code: int = 204
        self.successfully_updated_code: int = 201
        self.status_ok_code: int = 200


error_codes: ErrorCodes = ErrorCodes()
status_codes: StatusCodes = StatusCodes()


class DataServiceError(HTTPException):
    """
    **DataServiceError**
        raised when user has been performing an update or edit operation on their resource and the application
        is unable to complete such an operation. due to database errors

    **CODE: 512**
    """
    code: int = error_codes.data_service_error_code
    description: str = 'We have a problem connection to the Database'

    def __init__(self, status: Optional[int] = None, description: Optional[str] = None):
        super(DataServiceError, self).__init__(description=description)
        if bool(description):
            self.description = description
        if bool(status):
            self.code = status

    def __str__(self) -> str:
        return f"<DataServiceError Description: {self.description} Code: {self.code}"

    def __repr__(self) -> str:
        return self.__str__()


class InputError(Exception):
    """
    **InputError**
        raised when a user has supplied bad data or invalid arguments, for example supplying a None / Null value instead
        of a string will result in this error being thrown

    **CODE 422**
    """
    code: int = error_codes.input_error_code
    description: str = "Unable to process input"

    def __init__(self, status: Optional[int] = None, description: Optional[str] = None):
        super(InputError, self).__init__()
        if bool(description):
            self.description = description
        if bool(status):
            self.code = status

    def __str__(self) -> str:
        return f"<InputError Description: {self.description} Code: {self.code}"

    def __repr__(self) -> str:
        return self.__str__()


class UnAuthenticatedError(HTTPException):
    """
        **UnAuthenticatedError**
            in-case of an authentication error throw this error
        **CODE 401**
    """
    code: int = error_codes.un_auth_error_code
    description: str = "You are not authorized to use this resource"

    def __init__(self, status: Optional[int] = None, description: Optional[str] = None):
        super(UnAuthenticatedError, self).__init__(description=description)
        if bool(description):
            self.description = description

        if bool(status):
            self.code = status

    def __str__(self) -> str:
        return f"<UnAuthenticated Description: {self.description} Code: {self.code}"

    def __repr__(self) -> str:
        return self.__str__()


class RequestError(HTTPException):
    """
    **RequestError**
        when raised it simply means there was an error with the request
        and client/ user may need to verify their request
    **CODE: 400**
    """
    code: int = error_codes.bad_request_error_code
    description: str = "Bad Request Error: cannot proceed"

    def __init__(self, status: Optional[int] = None, description: Optional[str] = None,
                 url: Optional[str] = None):
        super(RequestError, self).__init__(description=description)
        if bool(description):
            self.description = description

        if bool(url):
            self.description = "{} on url: {}".format(description, url)

        if bool(status):
            self.code = status

    def __str__(self) -> str:
        return f"<RequestError  Description: {self.description} Code: {self.code}"

    def __repr__(self) -> str:
        return self.__str__()


# Errors

class RemoteDataError(IOError):
    """
        **RemoteDataError**
            raised when the server is trying to access a remote server or service in order
            to complete the users transaction but is unable to . the proper response
            would be to retry the action that lead to this error.
        ** CODE 406**
    """
    code: int = error_codes.remote_data_error
    description: str = 'Error connecting to remote server'
    url: str = ""

    def __init__(self, status: Optional[int] = None, description: Optional[str] = None,
                 url: Optional[str] = None):
        super(RemoteDataError, self).__init__()

        if bool(description):
            self.description = "{} {}".format(description, url)

        if bool(status):
            self.code = status

        if bool(url):
            self.url = url

    def __str__(self) -> str:
        return f"<RemoteDataError Description: {self.description} Code: {self.code} URL: {self.url}"

    def __repr__(self) -> str:
        return self.__str__()


class EnvironNotSet(Exception):
    """
        raised when environment variables are not set
    """
    code: int = error_codes.environment_error_code
    description: str = "environment variables not set please inform admin"
    url: str = ""

    def __init__(self, status: Optional[int] = None, description: Optional[str] = None,
                 url: Optional[str] = None):
        super(EnvironNotSet, self).__init__()

        if bool(description) and bool(url):
            self.description = "{} {}".format(description, url)

        if bool(status):
            self.code = status

        if bool(url):
            self.url = url

    def __str__(self) -> str:
        return f"<EnvironNotSet Description: {self.description} Code: {self.code} URL: {self.url}"

    def __repr__(self) -> str:
        return self.__str__()


def if_bad_request_raise(request) -> None:
    """
        **if_bad_request_raise**
            checks if request headers contains application/json
            if not raises request Error

    :param request: client request
    :return: None
    """
    content_type: str = request.headers.get('content-type')
    if not content_type.lower() == 'application/json':
        raise RequestError(description="parameters for this end-point may only be in json format")

import typing
from werkzeug.exceptions import HTTPException


class ErrorCodes:
    ***REMOVED***
        definitions of error codes, for errors that can be raised in Memberships & Affiliates Management API
    ***REMOVED***
    def __init__(self) -> None:
        self.input_error_code = 422
        self.data_service_error_code = 512
        self.un_auth_error_code = 401
        self.request_error_code = 404
        self.remote_data_error = 406
        self.environment_error_code = 506


class StatusCodes:
    def __init__(self):
        self.data_not_found_code = 204
        self.successfully_updated_code = 201
        self.status_ok_code = 200


error_codes: ErrorCodes = ErrorCodes()
status_codes: StatusCodes = StatusCodes()


class DataServiceError(HTTPException):
    ***REMOVED***
        use this error to throw a custom error explaining something is wrong with the datastore
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
    code: int = error_codes.request_error_code
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
    ***REMOVED***
        Remote data exception
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



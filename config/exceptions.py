import typing
from werkzeug.exceptions import HTTPException


class DataServiceError(HTTPException):
    ***REMOVED***
        use this error to throw a custom error explaining something is wrong with the datastore
    ***REMOVED***
    code: int = 512
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
    code: int = 422
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
    code: int = 401
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
    code: int = 404
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
    code: int = 406
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
    code: int = 506
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

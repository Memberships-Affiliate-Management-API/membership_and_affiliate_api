***REMOVED***
    **Module For Common Error Handlers for the application**
    *Routes Definitions for handling common application errors*
***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from flask import Blueprint, jsonify
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, MethodNotAllowed, Unauthorized
from config import config_instance
from config.exceptions import DataServiceError, InputError, RemoteDataError
from config.exceptions import UnAuthenticatedError, RequestError

default_handlers_bp = Blueprint('handlers', __name__)


@default_handlers_bp.route('/_ah/warmup')
def warmup() -> tuple:
    ***REMOVED***
        Use Context will create a database connection
        APP-Engine Warm UP Handler
        # TODO - send a message that another instance has started up
    ***REMOVED***
    return "OK", 200


# TODO - send an sms notification or email message with the error message for each error

def return_error(e) -> tuple:
    ***REMOVED***Actually replying with the error and description of the error here***REMOVED***
    if config_instance.DEBUG:
        print(f"Description: {e.description} Error_Code: {e.code}")
    return jsonify({'status': False, 'message': e.description}), e.code


@default_handlers_bp.app_errorhandler(BadRequest)
def handle_bad_request(e: BadRequest) -> tuple:
    ***REMOVED***
    Error_Code: 400
        Raise if the browser sends something to the application the application
        or server cannot handle.
    :param e: error instance
    :return:
    ***REMOVED***
    return return_error(e)


@default_handlers_bp.app_errorhandler(Forbidden)
def handle_forbidden_error(e: Forbidden) -> tuple:
    ***REMOVED****403* Forbidden

    Raise if the user doesn't have the permission for the requested resource
    but was authenticated.
    param e: error instance
    return: error response
    ***REMOVED***
    return return_error(e)


@default_handlers_bp.app_errorhandler(NotFound)
def handle_not_found_error(e: NotFound) -> tuple:
    ***REMOVED***
        *404* `Not Found`
        Raise if a resource does not exist and never existed.
    :param e: error instance
    :return: tuple of error response and status code
    ***REMOVED***
    return return_error(e)


@default_handlers_bp.app_errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e: MethodNotAllowed) -> tuple:
    ***REMOVED***
    *405* `Method Not Allowed`

    Raise if the server used a method the resource does not handle.  For
    example `POST` if the resource is view only.  Especially useful for REST.

    The first argument for this exception should be a list of allowed methods.
    Strictly speaking the response would be invalid if you don't provide valid
    methods in the header which you can do with that list.
    :param e: error instance
    :return: tuple of error response and status code
    ***REMOVED***
    return return_error(e)


@default_handlers_bp.app_errorhandler(Unauthorized)
def handle_un_authorized_requests(e: Unauthorized) -> tuple:
    ***REMOVED***
*401* ``Unauthorized``

    Raise if the user is not authorized to access a resource.

    The ``www_authenticate`` argument should be used to set the
    ``WWW-Authenticate`` header. This is used for HTTP basic auth and
    other schemes. Use :class:`~werkzeug.datastructures.WWWAuthenticate`
    to create correctly formatted values. Strictly speaking a 401
    response is invalid if it doesn't provide at least one value for
    this header, although real clients typically don't care.


    :param e: error instance
    :return:
    ***REMOVED***
    return return_error(e)


@default_handlers_bp.app_errorhandler(UnAuthenticatedError)
def handle_un_authorized_requests(e: UnAuthenticatedError) -> tuple:
    ***REMOVED****401*
    raised when a user is trying to access a resource without supplying the proper credentials for the resource.

    example: trying to access users from one organization without being registered to do so...meaning no organization_id was provided
    for such an organization or your uid is not suppose to access resources or manipulate those resources in the organization even
    though you are registered to the organization.


    :param e: error_instance
    :return: tuple representing the error
    ***REMOVED***
    return return_error(e)

#
# @default_handlers_bp.app_errorhandler(HTTPException)
# def handle_http_exception(e: HTTPException) -> tuple:
#     ***REMOVED***
#
#     :param e:
#     :return:
#     ***REMOVED***
#     return return_error(e)
#


# Custom Errors
@default_handlers_bp.app_errorhandler(DataServiceError)
def handle_data_service_error(e: DataServiceError):
    ***REMOVED***
    *401*
        raised when user has been performing an update or edit operation on their resource and the application
        is unable to complete such an operation.

    :param e: error instance
    :return: tuple representing the error
    ***REMOVED***
    return return_error(e)


@default_handlers_bp.app_errorhandler(InputError)
def handle_input_error(e: InputError) -> tuple:
    ***REMOVED****422*
        raised when a user has supplied bad data or invalid arguments, for example supplying a None / Null value instead
        of a string will result in this error being thrown
    :param e: error_instance
    :return: tuple representing the error and status
    ***REMOVED***
    return return_error(e)


@default_handlers_bp.app_errorhandler(RemoteDataError)
def handle_remote_error(e: RemoteDataError) -> tuple:
    ***REMOVED****406*
        raised when the server is trying to access a remote server or service in order
        to complete the users transaction but is unable to . the proper response
        would be to retry the action that lead to this error.
        :param  e: error_instance
        :return : tuple representing the error and status code
    ***REMOVED***
    return return_error(e)


@default_handlers_bp.app_errorhandler(RequestError)
def handle_remote_error(e: RequestError) -> tuple:
    ***REMOVED****404*
       raised when the server has created a request which succeeded but the response
       isn't what is expected or the remote server returns an error.

    :param e: error_instance
    :return: tuple representing the error and status
    ***REMOVED***
    return return_error(e)

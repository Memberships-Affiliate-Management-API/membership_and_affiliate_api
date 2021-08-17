***REMOVED***
    **Module For Common Error Handlers for the application**
    *Routes Definitions for handling common application errors*
***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from authlib.integrations.base_client import OAuthError
from flask import Blueprint, jsonify
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, MethodNotAllowed, Unauthorized
from config import config_instance
from config.exceptions import DataServiceError, InputError, RemoteDataError, error_codes
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


# TODO - send an sms notification or email message to app admin with the error message for each error

def return_error(e) -> tuple:
    ***REMOVED***
        **return_error**
            Actually replying with the error and description of the error here

        :param e: -> thrown exception
        :return tuple response, status_code
            -> message: exception description
    ***REMOVED***

    if config_instance.DEBUG:
        print(f"Description: {e.description} Error_Code: {e.code}")
    return jsonify({'status': False, 'message': e.description}), e.code


@default_handlers_bp.app_errorhandler(BadRequest)
def handle_bad_request(e: BadRequest) -> tuple:
    ***REMOVED***
    **handle_bad_request**
        Raise if the browser sends something to the application the application
        or server cannot handle.

    :param e: error instance
    :return: tuple -> response, status_code
    ***REMOVED***
    return return_error(e)


@default_handlers_bp.app_errorhandler(Forbidden)
def handle_forbidden_error(e: Forbidden) -> tuple:
    ***REMOVED***
    **handle_forbidden_error**
        Raise if the user doesn't have the permission for the requested resource
        but was authenticated.

    *403* Forbidden

    :param e: error instance
    :return: error response
    ***REMOVED***
    return return_error(e)


@default_handlers_bp.app_errorhandler(NotFound)
def handle_not_found_error(e: NotFound) -> tuple:
    ***REMOVED***
        **handle_not_found_error**
            Raise if a resource does not exist and never existed.

        *404* `Not Found`
    :param e: error instance
    :return: tuple -> error response and status code
    ***REMOVED***
    return return_error(e)


@default_handlers_bp.app_errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e: MethodNotAllowed) -> tuple:
    ***REMOVED***
    **handle_method_not_allowed**
        Raise if the server used a method the resource does not handle.  For
        example `POST` if the resource is view only.  Especially useful for REST.

        The first argument for this exception should be a list of allowed methods.
        Strictly speaking the response would be invalid if you don't provide valid
        methods in the header which you can do with that list.

        *405* `Method Not Allowed`

    :param e: error instance
    :return: tuple of error response and status code
    ***REMOVED***
    return return_error(e)


@default_handlers_bp.app_errorhandler(Unauthorized)
def handle_un_authorized_requests(e: Unauthorized) -> tuple:
    ***REMOVED***
    **handle_un_authorized_requests**
        Raise if the user is not authorized to access a resource.

        The ``www_authenticate`` argument should be used to set the
        ``WWW-Authenticate`` header. This is used for HTTP basic auth and
        other schemes. Use :class:`~werkzeug.datastructures.WWWAuthenticate`
        to create correctly formatted values. Strictly speaking a 401
        response is invalid if it doesn't provide at least one value for
        this header, although real clients typically don't care.

        *401* ``Unauthorized``
    :param e: error instance
    :return:
    ***REMOVED***
    return return_error(e)


@default_handlers_bp.app_errorhandler(UnAuthenticatedError)
def handle_un_authorized_requests(e: UnAuthenticatedError) -> tuple:
    ***REMOVED***
    **handle_un_authorized_requests**
        raised when a user is trying to access a resource without supplying the proper credentials for the resource.

        example: trying to access users from one organization without being registered to do so...meaning no organization_id was provided
        for such an organization or your uid is not suppose to access resources or manipulate those resources in the organization even
        though you are registered to the organization.

    **CODE: 401**

    :param e: exception -> error instance
    :return: tuple representing the error
    ***REMOVED***
    return return_error(e)


# Custom Errors
@default_handlers_bp.app_errorhandler(DataServiceError)
def handle_data_service_error(e: DataServiceError):
    ***REMOVED***
    **handle_data_service_error**
        raised when user has been performing an update or edit operation on their resource and the application
        is unable to complete such an operation.

    **CODE: 512**

    :param e: exception instance
    :return: tuple representing the error
    ***REMOVED***
    return return_error(e)


@default_handlers_bp.app_errorhandler(InputError)
def handle_input_error(e: InputError) -> tuple:
    ***REMOVED***
        **handle_input_error**

            raised when a user has supplied bad data or invalid arguments, for example supplying a None / Null value instead
            of a string will result in this error being thrown

        **CODE: 422**

    :param e: error_instance
    :return: tuple -> response, status_code
    ***REMOVED***
    return return_error(e)


@default_handlers_bp.app_errorhandler(RemoteDataError)
def handle_remote_error(e: RemoteDataError) -> tuple:
    ***REMOVED***
        **handle_remote_error**
            raised when the server is trying to access a remote server or service in order
            to complete the users transaction but is unable to . the proper response
            would be to retry the action that lead to this error.

        **CODE: 406**

        :param  e: error_instance
        :return : tuple -> response, status_code
    ***REMOVED***
    return return_error(e)


@default_handlers_bp.app_errorhandler(RequestError)
def handle_remote_error(e: RequestError) -> tuple:
    ***REMOVED***
    **handle_remote_error**
       raised when the server has created a request which succeeded but the response
       isn't what is expected or the remote server returns an error.

    **CODE: 404**

    :param e: error_instance
    :return: tuple response, status_code
    ***REMOVED***
    return return_error(e)


@default_handlers_bp.app_errorhandler(OAuthError)
def handle_auth_error(e:  OAuthError) -> tuple:
    ***REMOVED***
        **handle_auth_error**
            1. handles github authentication error**
            2. raised when something wrong happens during github authentication flow

        **CODE: 422 **
    :param e: exception instance
    :return: tuple -> response, status_code
    ***REMOVED***
    # Note OAuthError is not compatible with my custom errors
    message: str = e.description
    return return_error(e=UnAuthenticatedError(status=error_codes.input_error_code, description=message))


from flask import Blueprint, jsonify
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, MethodNotAllowed, Unauthorized, HTTPException
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
# noinspection PyUnusedLocal
@default_handlers_bp.app_errorhandler(BadRequest)
def handle_bad_request(e: BadRequest) -> tuple:
    return jsonify({'status': False, 'message': 'Bad Request'}), 400


# noinspection PyUnusedLocal
@default_handlers_bp.app_errorhandler(Forbidden)
def handle_forbidden_error(e: Forbidden) -> tuple:
    return jsonify({'status': False, 'message': 'Forbidden Request'}), 403


# noinspection PyUnusedLocal
@default_handlers_bp.app_errorhandler(NotFound)
def handle_not_found_error(e: NotFound) -> tuple:
    return jsonify({'status': False, 'message': 'Resource Not Found'}), 404


# noinspection PyUnusedLocal
@default_handlers_bp.app_errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e: MethodNotAllowed) -> tuple:
    return jsonify({'status': False, 'message': 'Request Method not Allowed'}), 405


# noinspection PyUnusedLocal
@default_handlers_bp.app_errorhandler(Unauthorized)
def handle_un_authorized_requests(e: Unauthorized) -> tuple:
    return jsonify({'status': False, 'message': 'Request Not Authorized'}), 401


@default_handlers_bp.app_errorhandler(UnAuthenticatedError)
def handle_un_authorized_requests(e: UnAuthenticatedError) -> tuple:
    return jsonify({'status': False, 'message': e.description}), e.code


# noinspection PyUnusedLocal
@default_handlers_bp.app_errorhandler(HTTPException)
def handle_http_exception(e: HTTPException) -> tuple:
    return jsonify({'status': False, 'message': 'HTTP Error'}), 503


# Custom Errors
@default_handlers_bp.app_errorhandler(DataServiceError)
def handle_data_service_error(e: DataServiceError):
    return jsonify({'status': False, 'message': e.description}), e.code


@default_handlers_bp.app_errorhandler(InputError)
def handle_input_error(e: InputError) -> tuple:
    return jsonify({'status': False, 'message': e.description}), e.code


@default_handlers_bp.app_errorhandler(RemoteDataError)
def handle_remote_error(e: RemoteDataError) -> tuple:
    return jsonify({'status': False, 'message': e.description}), e.code


@default_handlers_bp.app_errorhandler(RequestError)
def handle_remote_error(e: RequestError) -> tuple:
    return jsonify({'status': False, 'message': e.description}), e.code

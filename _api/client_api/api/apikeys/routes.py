***REMOVED***
    **api keys module**
        will be used by clients and application to get access to api keys
        for authentication purposes
***REMOVED***
from typing import Optional
from flask import Blueprint, request, current_app
from config.exceptions import UnAuthenticatedError, error_codes, if_bad_request_raise
from views.apikeys import APIKeysView

client_api_keys_bp = Blueprint('api-keys', __name__)


@client_api_keys_bp.route('/_api/v1/admin/api-keys/<string:key>/org/<string:organization_id>', methods=["POST"])
def return_api_key(key: str, organization_id) -> tuple:
    ***REMOVED***
        **return api_key**
            this module cannot be called from the outside
    :param key: api key to verify
    :param organization_id: the organization_id of the organization the api key belongs to
    :return:
    ***REMOVED***
    if_bad_request_raise(request)
    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get('SECRET_KEY')
    if isinstance(secret_key, str) and secret_key == current_app.config.get('SECRET_KEY'):
        api_view_instance: APIKeysView = APIKeysView()
        return api_view_instance.get_api_key(api_key=key, organization_id=organization_id)

    message: str = "User not Authorized: you are not authorized to call this API"
    raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)


@client_api_keys_bp.route('/_api/v1/client/api-keys/create', methods=['POST'])
def create_client_api_key() -> tuple:
    ***REMOVED***
        **create_client_api_key**
            used on behalf of clients to register new api keys
    :return:
    ***REMOVED***
    json_data: dict = request.get_json()
    domain: Optional[str] = json_data.get('domain')
    uid: Optional[str] = json_data.get('uid')
    organization_id: Optional[str] = json_data.get('organization_id')
    secret_key: Optional[str] = json_data.get('SECRET_KEY')
    if isinstance(secret_key, str) and secret_key == current_app.config.get('SECRET_KEY'):
        api_view_instance: APIKeysView = APIKeysView()
        return api_view_instance.create_keys(domain=domain, uid=uid, organization_id=organization_id)

    message: str = "User not Authorized: you are not authorized to call this API"
    raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)


@client_api_keys_bp.route('/_api/v1/client/api-keys/deactivate', methods=['POST'])
def deactivate_key() -> tuple:
    ***REMOVED***
        **deactivate_key**
            used on behalf of clients to de-activate their api keys
    :return:
    ***REMOVED***
    json_data: dict = request.get_json()
    api_key: Optional[str] = json_data.get('api-key')
    secret_key: Optional[str] = json_data.get('SECRET_KEY')
    if isinstance(secret_key, str) and secret_key == current_app.config.get('SECRET_KEY'):
        api_view_instance: APIKeysView = APIKeysView()
        return api_view_instance.deactivate_key(key=api_key)

    message: str = "User not Authorized: you are not authorized to call this API"
    raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)


@client_api_keys_bp.route('/_api/v1/client/api-keys/activate-key', methods=['POST'])
def activate_key() -> tuple:
    ***REMOVED***
        **activate_key**
            used on behalf of clients to de-activate their api keys
    :return:
    ***REMOVED***
    json_data: dict = request.get_json()
    api_key: Optional[str] = json_data.get('api-key')
    organization_id: Optional[str] = json_data.get('organization_id')
    secret_key: Optional[str] = json_data.get('SECRET_KEY')
    if isinstance(secret_key, str) and secret_key == current_app.config.get('SECRET_KEY'):
        api_view_instance: APIKeysView = APIKeysView()
        return api_view_instance.activate_key(key=api_key, organization_id=organization_id)

    message: str = "User not Authorized: you are not authorized to call this API"
    raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)


"""
    **api keys module**
        will be used by clients and application to get access to api keys
        for authentication purposes
"""

__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

import hmac
from typing import Optional
from flask import Blueprint, request, current_app
from config.exceptions import UnAuthenticatedError, error_codes, if_bad_request_raise
from security.apps_authenticator import handle_apps_authentication, verify_secret_key
from views import api_keys_view

client_api_keys_bp = Blueprint('api-keys', __name__)


# NOTE do not change to client route
@client_api_keys_bp.route('/_api/v1/admin/api-keys/<string:key>/org/<string:organization_id>', methods=["POST"])
@handle_apps_authentication
def return_api_key(key: str, organization_id) -> tuple:
    """
        **return api_key**
            this module cannot be called from the outside
    :param key: api key to verify
    :param organization_id: the organization_id of the organization the api key belongs to
    :return:
    """
    if_bad_request_raise(request)
    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get('SECRET_KEY')
    _secret_keys_match: bool = hmac.compare_digest(secret_key, current_app.config.get('SECRET_KEY'))
    if _secret_keys_match:
        return api_keys_view.get_api_key(api_key=key, organization_id=organization_id)

    message: str = "User not Authorized: you are not authorized to call this API"
    raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)


@client_api_keys_bp.route('/_api/v1/client/api-keys/create', methods=['POST'])
@handle_apps_authentication
def create_client_api_key() -> tuple:
    """
        **create_client_api_key**
            used on behalf of clients to register new api keys
    :return:
    """
    json_data: dict = request.get_json()
    domain: Optional[str] = json_data.get('domain')
    uid: Optional[str] = json_data.get('uid')
    organization_id: Optional[str] = json_data.get('organization_id')
    secret_key: Optional[str] = json_data.get('SECRET_KEY')
    _secret_keys_match: bool = hmac.compare_digest(secret_key, current_app.config.get('SECRET_KEY'))

    if not _secret_keys_match:
        message: str = "User not Authorized: you are not authorized to call this API"
        raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

    return api_keys_view.create_keys(domain=domain, uid=uid, organization_id=organization_id)


@client_api_keys_bp.route('/_api/v1/client/api-keys/deactivate', methods=['POST'])
@handle_apps_authentication
def deactivate_key() -> tuple:
    """
        **deactivate_key**
            used on behalf of clients to de-activate their api keys
    :return:
    """
    json_data: dict = request.get_json()
    api_key: Optional[str] = json_data.get('api-key')
    secret_key: Optional[str] = json_data.get('SECRET_KEY')
    verify_secret_key(secret_key)

    return api_keys_view.deactivate_key(key=api_key)


@client_api_keys_bp.route('/_api/v1/client/api-keys/activate-key', methods=['POST'])
@handle_apps_authentication
def activate_key() -> tuple:
    """
        **activate_key**
            used on behalf of clients to de-activate their api keys
    :return:
    """
    json_data: dict = request.get_json()
    api_key: Optional[str] = json_data.get('api-key')
    organization_id: Optional[str] = json_data.get('organization_id')
    secret_key: Optional[str] = json_data.get('SECRET_KEY')
    _secret_keys_match: bool = hmac.compare_digest(secret_key, current_app.config.get('SECRET_KEY'))

    if _secret_keys_match:
        return api_keys_view.activate_key(key=api_key, organization_id=organization_id)

    message: str = "User not Authorized: you are not authorized to call this API"
    raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

"""
    **Microservices Authentication Endpoint**
        this module insures the identity of each micro-service while calling the admin api
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import hmac

from flask import Blueprint, jsonify, request

from config import config_instance
from config.exceptions import status_codes, UnAuthenticatedError, error_codes
from security.apps_authenticator import verify_app_id
from security.users_authenticator import encode_auth_token
from utils import is_development

microservices_ipn_bp = Blueprint("microservices_ipn", __name__)


@microservices_ipn_bp.route('/_ipn/micro-services/auth', methods=["POST"])
def micro_services_auth() -> tuple:
    """

    :return:
    """
    json_data: dict = request.get_json()
    domain: str = json_data.get('domain')
    app_id: str = json_data.get('app_id')
    secret_key: str = json_data.get('SECRET_KEY')
    if domain is None:
        message: str = "Application not authorized: domain is Null"
        raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)
    if app_id is None:
        message: str = "Application not authorized: app_id is Null"
        raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)
    if secret_key is None:
        message: str = "Application not authorized: Secret_key is Null"
        raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

    # TODO consider checking if the domain which makes the call is the same as the domain which was passed

    # Note: adding forward slash to the domain name to match internal domain formatting
    _domain = f"{domain}/" if not domain.endswith("/") else domain
    # NOTE: the following statement will only run if api is running
    # in development server or on staging sever
    _domain = _domain.replace('localhost', '127.0.0.1') if is_development() else _domain

    # Note: checking if domain matches a known client domain
    _client_domain: str = config_instance.CLIENT_APP_BASEURL
    client_domain_compare: bool = hmac.compare_digest(_domain, _client_domain)

    # Note checking if domain matches a known admin domain
    _admin_domain: str = config_instance.ADMIN_APP_BASEURL
    admin_domain_compare: bool = hmac.compare_digest(_domain, _admin_domain)

    # Note: checking if secret key matches
    _secret_key: str = config_instance.SECRET_KEY
    compare_secret_key: bool = hmac.compare_digest(secret_key, _secret_key)

    # Note: checking if app_id is really the same as the app_id created by the app itself
    if client_domain_compare:
        is_id_valid: bool = verify_app_id(app_id=app_id, domain=_client_domain)
    elif admin_domain_compare:
        is_id_valid: bool = verify_app_id(app_id=app_id, domain=_admin_domain)
    else:
        message: str = "Application not authorized"
        raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

    # If auth details are found and app id is valid and secret_key matches default key proceed to
    # authenticate
    if not is_id_valid or not compare_secret_key:
        message: str = "Application not authorized"
        raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

    _token_id: str = f"{domain}#{secret_key}#{app_id}"
    _auth_token = encode_auth_token(uid=_token_id, expiration_days=30)
    if not _auth_token:
        message: str = "Application not authorized"
        raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

    _payload: dict = dict(app_id=app_id, domain=domain, secret_key=secret_key, auth_token=_auth_token)
    _message: str = 'application successfully authenticated'

    return jsonify(dict(result=True, payload=_payload, message=_message)), status_codes.successfully_updated_code


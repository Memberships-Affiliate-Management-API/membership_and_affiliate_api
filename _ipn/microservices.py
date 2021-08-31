***REMOVED***
    **Microservices Auth Endpoint**
***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import hmac
from typing import Optional

import requests
from flask import Blueprint, jsonify, request
from google.cloud import ndb

from config import config_instance
from config.exceptions import status_codes, UnAuthenticatedError, error_codes, DataServiceError
from database.app_authenticator import MicroAuthDetails
from security.apps_authenticator import verify_app_id
from security.users_authenticator import encode_auth_token

microservices_ipn_bp = Blueprint("microservices_ipn", __name__)


@microservices_ipn_bp.route('/_ipn/micro-services/auth', methods=["POST"])
def micro_services_auth() -> tuple:
    ***REMOVED***

    :return:
    ***REMOVED***
    json_data: dict = request.get_json()
    domain: str = json_data.get('domain')
    app_id: str = json_data.get('app_id')
    secret_key: str = json_data.get('secret_key')

    _secret_key: str = config_instance.SECRET_KEY
    _client_domain: str = config_instance.CLIENT_APP_BASEURL
    client_domain_compare: bool = hmac.compare_digest(domain, _client_domain)
    _admin_domain: str = config_instance.ADMIN_APP_BASEURL
    admin_domain_compare: bool = hmac.compare_digest(domain, _admin_domain)
    compare_secret_key: bool = hmac.compare_digest(secret_key, _secret_key)

    if client_domain_compare:
        is_id_valid: bool = verify_app_id(app_id=app_id, domain=_client_domain)
    elif admin_domain_compare:
        is_id_valid: bool = verify_app_id(app_id=app_id, domain=_admin_domain)
    else:
        message: str = "Application not authorized"
        raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

    app_auth_details: MicroAuthDetails = MicroAuthDetails.query(MicroAuthDetails.domain == domain).get()

    if isinstance(app_auth_details, MicroAuthDetails):
        compare_domain: bool = hmac.compare_digest(domain, app_auth_details.domain)
        if compare_domain:
            app_auth_details.app_id = app_id
            token_id: str = f"{secret_key}.{app_id}"
            app_auth_details.auth_token = encode_auth_token(uid=token_id)
            _retries: int = config_instance.DATASTORE_RETRIES
            _timeout: int = config_instance.DATASTORE_TIMEOUT
            key: Optional[ndb.Key] = app_auth_details.put(retries=_retries, timeout=_timeout)
            if not isinstance(key, ndb.Key):
                message: str = "Database Error: Unable to authenticate"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            _result: dict = {'status': True, 'payload': app_auth_details.to_dict(),
                             'message': 'successfully authenticated'}

            return jsonify(_result), status_codes.successfully_updated_code

    message: str = "Application not authorized"
    raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)







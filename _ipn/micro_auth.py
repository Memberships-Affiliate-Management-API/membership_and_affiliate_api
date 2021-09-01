***REMOVED***
    **Microservices Authentication Endpoint**
        this module insures the identity of each micro-service while calling the admin api
***REMOVED***
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import hmac
from typing import Optional

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

    # Note: adding forward slash to the domain name to match internal domain formatting
    _domain = f"{domain}/" if not domain.endswith("/") else domain

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

    app_auth_details: MicroAuthDetails = MicroAuthDetails.query(MicroAuthDetails.domain == domain).get()

    # If auth details are found and app id is valid and secret_key matches default key proceed to
    # authenticate
    if bool(app_auth_details) and is_id_valid and compare_secret_key:
        # comparing domain name with auth details domain name
        compare_domain: bool = hmac.compare_digest(domain, app_auth_details.domain)
        if compare_domain:
            # Updating app_id and auth token
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

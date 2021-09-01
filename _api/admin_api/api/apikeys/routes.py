***REMOVED***
    **api keys system admin module**
        controls access to api keys for system admin application
***REMOVED***

__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

import hmac
from typing import Optional

from flask import Blueprint, request, current_app

from config import config_instance
from config.exceptions import UnAuthenticatedError, error_codes
from security.apps_authenticator import handle_apps_authentication
from views.apikeys import APIKeysView

admin_api_keys_api_bp = Blueprint("admin_api_keys_api", __name__)


@admin_api_keys_api_bp.route('/_api/v1/admin/api-keys/<string:path>', methods=["POST"])
@handle_apps_authentication
def api_keys(path: str) -> tuple:
    ***REMOVED***
    **api_keys**
        system admin api keys endpoint
    :param path:
    :return: results depending on path
    ***REMOVED***

    api_keys_instance: APIKeysView = APIKeysView()
    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get('SECRET_KEY')

    compare_secret_key: bool = hmac.compare_digest(secret_key, current_app.config.get('SECRET_KEY'))
    if not compare_secret_key:
        message: str = 'User Not Authorized: you cannot perform this action'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    if path == "get-all":
        organization_id: str = json_data.get('organization_id')
        uid: str = json_data.get('uid')
        compare_uid: bool = hmac.compare_digest(uid, config_instance.ADMIN_UID)
        compare_org: bool = hmac.compare_digest(organization_id, config_instance.ORGANIZATION_ID)
        if compare_org and compare_uid:
            return api_keys_instance.return_all_organization_keys(organization_id=organization_id)
        message: str = 'User Not Authorized: you cannot perform this action'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)


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
from views import affiliates_view

admin_affiliates_api_bp = Blueprint("admin_affiliates_api", __name__)


@admin_affiliates_api_bp.route('/_api/v1/admin/affiliates/<string:path>', methods=["POST"])
@handle_apps_authentication
def admin_affiliates(path: str) -> tuple:
    ***REMOVED***

    :param path:
    :return:
    ***REMOVED***
    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get('SECRET_KEY')

    compare_secret_key: bool = hmac.compare_digest(secret_key, current_app.config.get('SECRET_KEY'))
    if not compare_secret_key:
        message: str = 'User Not Authorized: you cannot perform this action'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    if path == "get-all":
        organization_id: str = json_data.get('organization_id')
        uid: str = json_data.get('uid')
        compare_organization: bool = hmac.compare_digest(organization_id, config_instance.ORGANIZATION_ID)
        compare_uid: bool = hmac.compare_digest(uid, config_instance.ADMIN_UID)

        if compare_organization and compare_uid:
            # NOTE: this returns the affiliates to the main application
            return affiliates_view.get_all_affiliates(organization_id=organization_id)
        message: str = "You are not authorized to access this resource"
        raise UnAuthenticatedError(description=message)


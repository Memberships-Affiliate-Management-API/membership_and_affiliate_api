"""
    **api keys system admin module**
        controls access to api keys for system admin application
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

from config import config_instance
from config.exceptions import UnAuthenticatedError, error_codes
from security.apps_authenticator import handle_apps_authentication, verify_secret_key
from views import api_keys_view

admin_api_keys_api_bp = Blueprint("admin_api_keys_api", __name__)


@admin_api_keys_api_bp.route('/_api/v1/admin/api-keys/<string:path>', methods=["POST"])
@handle_apps_authentication
def api_keys(path: str) -> tuple:
    """
    **api_keys**
        system admin api keys endpoint

    :param path:
    :return: results depending on path
    """
    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get('SECRET_KEY')
    verify_secret_key(secret_key)

    if path == "get-all":
        organization_id = is_admin_user(json_data)
        return api_keys_view.return_all_organization_keys(organization_id=organization_id)
    elif path == "return-active-org-keys":
        organization_id = is_admin_user(json_data)
        return api_keys_view.return_active_organization_keys(organization_id=organization_id)
    elif path == "get-api-key":
        organization_id = is_admin_user(json_data)
        api_key: str = json_data.get('api_key')
        return api_keys_view.get_api_key(api_key=api_key, organization_id=organization_id)


def is_admin_user(json_data):
    organization_id: str = json_data.get('organization_id')
    uid: str = json_data.get('uid')
    compare_uid: bool = hmac.compare_digest(uid, config_instance.ADMIN_UID)
    compare_org: bool = hmac.compare_digest(organization_id, config_instance.ORGANIZATION_ID)
    if not (compare_org and compare_uid):
        message: str = 'User Not Authorized: you cannot perform this action'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)
    return organization_id

"""
    **recruits admin api module**
        an admin api for recruits management
"""

__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

import hmac
from typing import Optional

from flask import Blueprint, request

from config import config_instance
from config.exceptions import UnAuthenticatedError
from security.apps_authenticator import handle_apps_authentication, verify_secret_key
from views import recruits_view

admin_recruits_api_bp = Blueprint("admin_recruits_api", __name__)

admin_recruits_api_bp.route('/_api/v1/admin/recruits/<string:path', methods=['POST'])


@handle_apps_authentication
def recruits_admin(path: str) -> tuple:
    """
        **recruits_admin**
            system admin management api
    :param path:
    :return:
    """
    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get('SECRET_KEY')
    verify_secret_key(secret_key)
    if path == 'get-all':
        organization_id: str = json_data.get('organization_id')
        uid: str = json_data.get('uid')
        compare_organization: bool = hmac.compare_digest(organization_id, config_instance.ORGANIZATION_ID)
        compare_uid: bool = hmac.compare_digest(uid, config_instance.ADMIN_UID)
        if not (compare_organization and compare_uid):
            raise UnAuthenticatedError(description=message)
        return recruits_view.get_recruit


"""
    **memberships system admin api**
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"


import hmac
from typing import Union, Optional
from flask import Blueprint, request, current_app

from config.exceptions import UnAuthenticatedError, error_codes
from security.apps_authenticator import handle_apps_authentication
from views import membership_plans_view, memberships_view

membership_admin_api_bp = Blueprint('memberships_admin_api', __name__)


@membership_admin_api_bp.route('/_api/v1/admin/membership-plans/<string:path>', methods=['GET', 'POST'])
@handle_apps_authentication
def memberships_plan_admin_api(path: str) -> tuple:
    """
    **memberships_plan_admin_api**
        this endpoint is for purposes of user administration only not for admin purposes

    :param path:
    :return:
    """
    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get('SECRET_KEY')

    compare_secret_key: bool = hmac.compare_digest(secret_key, current_app.config.get('SECRET_KEY'))
    if not compare_secret_key:
        message: str = 'User Not Authorized: you cannot perform this action'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    if path == "get":
        organization_id: Union[str, None] = json_data.get('organization_id')
        uid: Union[str, None] = json_data.get('uid')

        return membership_plans_view.return_plan_by_uid(organization_id=organization_id, uid=uid)

    elif path == "get-all":
        organization_id: Union[str, None] = json_data.get('organization_id')
        return membership_plans_view.return_all_plans(organization_id=organization_id)


@membership_admin_api_bp.route('/_api/v1/admin/memberships/<string:path>', methods=['GET', 'POST'])
def memberships_admin(path: str) -> tuple:
    """

    :param path:
    :return:
    """
    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get('SECRET_KEY')

    compare_secret_key: bool = hmac.compare_digest(secret_key, current_app.config.get('SECRET_KEY'))
    if not compare_secret_key:
        message: str = 'User Not Authorized: you cannot perform this action'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    if path == "get-all":
        # get all subscriptions for a specific organization
        organization_id: Union[str, None] = json_data.get('organization_id')
        uid: Union[str, None] = json_data.get('uid')

        return memberships_view.return_members(organization_id=organization_id)

    elif path == "get-subscription":
        organization_id: Union[str, None] = json_data.get('organization_id')
        uid: Union[str, None] = json_data.get('uid')

        return memberships_view.is_member_off(organization_id=organization_id, uid=uid)






***REMOVED***
    **memberships system admin api**
***REMOVED***
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"


import hmac

from flask import Blueprint, request, current_app

from config.exceptions import UnAuthenticatedError, error_codes
from security.apps_authenticator import handle_apps_authentication
from views.memberships import MembershipPlansView, MembershipsView
from security.users_authenticator import logged_user, is_app_admin, handle_users_auth
from typing import Union, Optional

membership_plans_admin_api_bp = Blueprint('memberships_admin_api', __name__)


@membership_plans_admin_api_bp.route('/_api/v1/admin/membership-plans/<string:path>', methods=['GET', 'POST'])
@handle_apps_authentication
def memberships_admin_api(path: str) -> tuple:
    ***REMOVED***
        this endpoint is for purposes of user administration only not for admin purposes
    :param path:
    :return:
    ***REMOVED***
    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get('SECRET_KEY')

    compare_secret_key: bool = hmac.compare_digest(secret_key, current_app.config.get('SECRET_KEY'))
    if not compare_secret_key:
        message: str = 'User Not Authorized: you cannot perform this action'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    if path == "get":
        organization_id: Union[str, None] = json_data.get('organization_id')
        uid: Union[str, None] = json_data.get('uid')
        membership_plan_view_instance: MembershipPlansView = MembershipPlansView()
        return membership_plan_view_instance.return_plan_by_uid(organization_id=organization_id, uid=uid)

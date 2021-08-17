from flask import Blueprint, request, current_app

from config.exceptions import UnAuthenticatedError, error_codes
from views.memberships import MembershipPlansView, MembershipsView
from security.users_authenticator import logged_user, is_app_admin, handle_users_auth
from typing import Union, Optional

membership_plans_admin_api_bp = Blueprint('memberships_admin_api', __name__)


@membership_plans_admin_api_bp.route('/_api/v1/admin/membership-plans/<string:path>', methods=['GET', 'POST'])
def memberships_admin_api(path: str) -> tuple:
    ***REMOVED***
        this endpoint is for purposes of user administration only not for admin purposes
    :param path:
    :return:
    ***REMOVED***
    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get('SECRET_KEY')
    if not isinstance(secret_key, str) or secret_key != current_app.config.get('SECRET_KEY'):
        message: str = 'User Not Authorized: you cannot perform this action'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    if path == "get":
        organization_id: Union[str, None] = json_data.get('organization_id')
        uid: Union[str, None] = json_data.get('uid')
        membership_plan_view_instance: MembershipPlansView = MembershipPlansView()
        return membership_plan_view_instance.return_plan_by_uid(organization_id=organization_id, uid=uid)

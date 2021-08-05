from flask import Blueprint, request
from views.memberships import MembershipPlansView, MembershipsView
from security.users_authenticator import logged_user, is_app_admin
from typing import Union


membership_plans_admin_api_bp = Blueprint('memberships_admin_api', __name__)


@membership_plans_admin_api_bp.route('_api/admin/membership-plans/<string:path>', methods=['GET', 'POST'])
def memberships_admin_api(path: str) -> tuple:

    if path == "get":
        json_data: dict = request.get_json()
        organization_id: Union[str, None] = json_data.get('organization_id')
        uid: Union[str, None] = json_data.get('uid')
        membership_plan_view_instance: MembershipPlansView = MembershipPlansView()
        return membership_plan_view_instance.return_plan_by_uid(organization_id=organization_id, uid=uid)
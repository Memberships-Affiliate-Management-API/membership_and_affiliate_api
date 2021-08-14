from flask import Blueprint, request, current_app

from config.exceptions import UnAuthenticatedError, error_codes
from views.organization import OrganizationView
from typing import Union, Optional

admin_organization_api_bp = Blueprint("admin_organization_api", __name__)


@admin_organization_api_bp.route('/_api/v1/admin/organizations/<string:path>', methods=['GET', 'POST'])
def organization_admin_api(path: str) -> tuple:
    ***REMOVED***
        **organization_admin_api**
            organizations admin routes are only related to administration functions of
            organizations

        **NOTE**
            for client routes see client admin api

    :param path:
    :return:
    ***REMOVED***
    # TODO - verify this uid against system admin user id
    org_view_instance: OrganizationView = OrganizationView()

    # NOTE: here the system admin is actually requesting client or developers organizations
    if path == "get":
        json_data: dict = request.get_json()
        organization_id: Optional[str] = json_data.get("organization_id")
        uid: Optional[str] = json_data.get("uid")
        secret_key: Optional[str] = json_data.get('SECRET_KEY')
        if isinstance(secret_key, str) and secret_key == current_app.config.get('SECRET_KEY'):
            return org_view_instance._get_organizations(organization_id=organization_id)

        message: str = 'User Not Authorized: cannot fetch organization'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    # NOTE: here the system is requesting records of all clients organizations
    elif path == "get-all":
        json_data: dict = request.get_json()
        secret_key: Optional[str] = json_data.get('SECRET_KEY')
        if isinstance(secret_key, str) and secret_key == current_app.config.get('SECRET_KEY'):
            return org_view_instance._return_all_organizations()

        message: str = 'User Not Authorized: cannot fetch organizations'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)




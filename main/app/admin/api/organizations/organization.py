from flask import Blueprint, request
from views.organization import OrganizationView
from typing import Union

admin_organization_api_bp = Blueprint("admin_organization_api", __name__)


@admin_organization_api_bp.route('/_api/admin/organizations/<string:path>', methods=['GET', 'POST'])
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

    if path == "get":
        json_data: dict = request.get_json()
        organization_id: Union[str, None] = json_data.get("organization_id")
        uid: Union[str, None] = json_data.get("uid")
        org_view_instance: OrganizationView = OrganizationView()
        return org_view_instance.get_organization(uid=uid, organization_id=organization_id)


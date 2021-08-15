***REMOVED***
    **Organization Routes Module**
        Handles API Requests for Organizations

***REMOVED***
from typing import Optional
from flask import request, Blueprint, current_app

from config.exceptions import UnAuthenticatedError, error_codes, if_bad_request_raise
from views.organization import OrganizationView

client_organizations_api_bp = Blueprint('client_organizations_api', __name__)


@client_organizations_api_bp.route('/_api/v1/client-admin/organization/<string:path>', methods=['POST'])
def client_organization_main(path: str) -> tuple:
    ***REMOVED***
        **client_organization_main**
            handles requests related to organizations creations and manipulation
            will be used only when clients/ developers registers an api in order
            to start using it

        **NOTE**
            this api will only be called from the main application -
            that means no users for clients will make requests to this endpoint
    :return:
    ***REMOVED***
    if_bad_request_raise(request)
    org_view_instance: OrganizationView = OrganizationView()
    # NOTE: client admin request to create organization
    if path == "create":
        json_data: dict = request.get_json()
        secret_key: str = current_app.config.get('SECRET_KEY')
        uid: Optional[str] = json_data.get('uid')
        organization_name: Optional[str] = json_data.get('organization_name')
        description: Optional[str] = json_data.get('description')
        currency: Optional[str] = json_data.get('currency')
        paypal_address: Optional[str] = json_data.get('paypal_address')
        if isinstance(secret_key, str) and secret_key == current_app.config.get('SECRET_KEY'):
            return org_view_instance.create_organization(uid=uid, organization_name=organization_name,
                                                         description=description, currency=currency,
                                                         paypal_address=paypal_address)

        message: str = 'User Not Authorized: cannot create new organization'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)
    elif path == "update":
        json_data: dict = request.get_json()
        secret_key: str = current_app.config.get('SECRET_KEY')
        uid: Optional[str] = json_data.get('uid')
        organization_id: Optional[str] = json_data.get('organization_id')
        organization_name: Optional[str] = json_data.get('organization_name')
        description: Optional[str] = json_data.get('description')
        # NOTE can update organization wallet on the org page wallet tab - meaning separate route or api
        # currency: Optional[str] = json_data.get('currency')
        # paypal_address: Optional[str] = json_data.get('paypal_address')
        if isinstance(secret_key, str) and secret_key == current_app.config.get('SECRET_KEY'):
            return org_view_instance.update_organization(uid=uid, organization_id=organization_id,
                                                         organization_name=organization_name, description=description)

        message: str = 'User Not Authorized: cannot update organization'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    elif path == "get":
        json_data: dict = request.get_json()
        secret_key: str = current_app.config.get('SECRET_KEY')
        organization_id: Optional[str] = json_data.get('organization_id')
        uid: Optional[str] = json_data.get('uid')
        if isinstance(secret_key, str) and secret_key == current_app.config.get('SECRET_KEY'):
            return org_view_instance.get_organization(organization_id=organization_id, uid=uid)

        message: str = 'User Not Authorized: cannot fetch organization'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

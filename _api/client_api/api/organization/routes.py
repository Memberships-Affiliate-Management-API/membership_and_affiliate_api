"""
    **Organization Routes Module**
        Handles API Requests for Organizations

"""
import hmac
from typing import Optional
from flask import request, Blueprint, current_app
from config.exceptions import UnAuthenticatedError, error_codes, if_bad_request_raise
from security.apps_authenticator import handle_apps_authentication
from views import organization_view

client_organizations_api_bp = Blueprint('client_organizations_api', __name__)


@client_organizations_api_bp.route('/_api/v1/client-admin/organization/<string:path>', methods=['POST'])
@handle_apps_authentication
def client_organization_main(path: str) -> tuple:
    """
        **client_organization_main**
            handles requests related to organizations creations and manipulation
            will be used only when clients/ developers registers an api in order
            to start using it

        **NOTE**
            this api will only be called from the main application -
            that means no users for clients will make requests to this endpoint
    :return:
    """
    if_bad_request_raise(request)
    # NOTE: client admin request to create organization
    json_data: dict = request.get_json()
    secret_key: str = current_app.config.get('SECRET_KEY')

    compare_secret_key: bool = hmac.compare_digest(secret_key, current_app.config.get('SECRET_KEY'))
    if not compare_secret_key:
        message: str = 'User Not Authorized: you cannot perform this action'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    if path == "create":
        uid: Optional[str] = json_data.get('uid')
        organization_name: Optional[str] = json_data.get('organization_name')
        description: Optional[str] = json_data.get('description')
        currency: Optional[str] = json_data.get('currency')
        paypal_address: Optional[str] = json_data.get('paypal_address')
        home_url: Optional[str] = json_data.get('home_url')
        login_callback_url: Optional[str] = json_data.get('login_callback_url')
        recovery_callback_url: Optional[str] = json_data.get('recovery_callback_url')
        if isinstance(secret_key, str) and secret_key == current_app.config.get('SECRET_KEY'):
            return organization_view.create_organization(uid=uid, organization_name=organization_name,
                                                         description=description, currency=currency,
                                                         paypal_address=paypal_address, home_url=home_url,
                                                         login_callback_url=login_callback_url,
                                                         recovery_callback_url=recovery_callback_url)

        message: str = 'User Not Authorized: cannot create new organization'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)
    elif path == "update":
        uid: Optional[str] = json_data.get('uid')
        organization_id: Optional[str] = json_data.get('organization_id')
        organization_name: Optional[str] = json_data.get('organization_name')
        description: Optional[str] = json_data.get('description')
        home_url: Optional[str] = json_data.get('home_url')
        login_callback_url: Optional[str] = json_data.get('login_callback_url')
        recovery_callback_url: Optional[str] = json_data.get('recovery_callback_url')

        # NOTE can update organization wallet on the org page wallet tab - meaning separate route or api
        # currency: Optional[str] = json_data.get('currency')
        # paypal_address: Optional[str] = json_data.get('paypal_address')
        if isinstance(secret_key, str) and secret_key == current_app.config.get('SECRET_KEY'):
            return organization_view.update_organization(uid=uid, organization_id=organization_id,
                                                         organization_name=organization_name, description=description,
                                                         home_url=home_url, login_callback_url=login_callback_url,
                                                         recovery_callback_url=recovery_callback_url)

        message: str = 'User Not Authorized: cannot update organization'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    elif path == "get":
        organization_id: Optional[str] = json_data.get('organization_id')
        uid: Optional[str] = json_data.get('uid')
        if isinstance(secret_key, str) and secret_key == current_app.config.get('SECRET_KEY'):
            return organization_view.get_organization(organization_id=organization_id, uid=uid)

        message: str = 'User Not Authorized: cannot fetch organization'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

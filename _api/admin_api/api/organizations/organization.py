***REMOVED***
    handle users and admin authentication
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
from database.mixins import AmountMixin
from security.apps_authenticator import handle_apps_authentication
from views import organization_view
from typing import Optional

admin_organization_api_bp = Blueprint("admin_organization_api", __name__)


@admin_organization_api_bp.route('/_api/v1/admin/organizations/<string:path>', methods=['GET', 'POST'])
@handle_apps_authentication
def organization_admin_api(path: str) -> tuple:
    ***REMOVED***
        **organization_admin_api**
            organizations admin routes are only related to administration functions of
            organizations

        **NOTE**
            for client routes see client admin api
        TODO - complete documentation
    :param path:
    :return:
    ***REMOVED***
    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get('SECRET_KEY')

    compare_secret_key: bool = hmac.compare_digest(secret_key, current_app.config.get('SECRET_KEY'))
    if not compare_secret_key:
        message: str = 'User Not Authorized: you cannot perform this action'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    # NOTE: here the system admin is actually requesting client or developers organizations
    if path == "get":
        organization_id: Optional[str] = json_data.get("organization_id")
        return organization_view._get_organizations(organization_id=organization_id)

    # NOTE: here the system is requesting records of all clients organizations
    elif path == "get-all":
        return organization_view._return_all_organizations()

    # NOTE: this allows the system to update affiliate count
    elif path == "update-affiliate-count":
        organization_id: Optional[str] = json_data.get("organization_id")
        add: int = int(json_data.get("add", 0))
        sub: int = int(json_data.get("int", 0))
        return organization_view._update_affiliate_count(organization_id=organization_id, add=add, subtract=sub)

    # Updates the total amount paid by this organization
    elif path == "update-total-paid":
        organization_id: Optional[str] = json_data.get("organization_id")
        add: int = int(json_data.get("add", 0))
        sub: int = int(json_data.get("int", 0))
        currency: Optional[str] = json_data.get("currency")

        add_amount: AmountMixin = AmountMixin(amount=add, currency=currency)
        sub_amount: AmountMixin = AmountMixin(amount=sub, currency=currency)
        return organization_view._update_total_paid(organization_id=organization_id, add_amount=add_amount,
                                                    subtract_amount=sub_amount)

    elif path == "update-total-members":
        organization_id: Optional[str] = json_data.get("organization_id")
        add: int = int(json_data.get("add", 0))
        sub: int = int(json_data.get("int", 0))

        return organization_view._update_total_members(organization_id=organization_id, add=add, subtract=sub)

    elif path == "update-projected-payments":
        # TODO learn the best way to calculate projected payments - maybe use property on databases
        pass

    elif path == "update-total-membership-payments":
        organization_id: Optional[str] = json_data.get("organization_id")
        add: int = int(json_data.get("add", 0))
        sub: int = int(json_data.get("int", 0))
        currency: Optional[str] = json_data.get("currency")
        add_amount: Optional[AmountMixin] = None
        sub_amount: Optional[AmountMixin] = None
        if add:
            add_amount: AmountMixin = AmountMixin(amount=add, currency=currency)
        if sub:
            sub_amount: AmountMixin = AmountMixin(amount=sub, currency=currency)
        return organization_view._update_total_membership_payments(organization_id=organization_id,
                                                                   subtract_total_membership_payment=sub_amount,
                                                                   add_total_membership_amount=add_amount)

from flask import Blueprint, request, current_app
from config.exceptions import UnAuthenticatedError, error_codes
from database.mixins import AmountMixin
from security.apps_authenticator import handle_apps_authentication
from views.organization import OrganizationView
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

    :param path:
    :return:
    ***REMOVED***
    # TODO - verify this uid against system admin user id
    org_view_instance: OrganizationView = OrganizationView()
    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get('SECRET_KEY')

    if not isinstance(secret_key, str) or secret_key != current_app.config.get('SECRET_KEY'):
        message: str = 'User Not Authorized: you cannot perform this action'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    # NOTE: here the system admin is actually requesting client or developers organizations
    if path == "get":
        organization_id: Optional[str] = json_data.get("organization_id")
        return org_view_instance._get_organizations(organization_id=organization_id)

    # NOTE: here the system is requesting records of all clients organizations
    elif path == "get-all":
        return org_view_instance._return_all_organizations()

    # NOTE: this allows the system to update affiliate count
    elif path == "update-affiliate-count":
        organization_id: Optional[str] = json_data.get("organization_id")
        add: int = int(json_data.get("add", 0))
        sub: int = int(json_data.get("int", 0))
        return org_view_instance._update_affiliate_count(organization_id=organization_id, add=add, subtract=sub)

    # Updates the total amount paid by this organization
    elif path == "update-total-paid":
        organization_id: Optional[str] = json_data.get("organization_id")
        add: int = int(json_data.get("add", 0))
        sub: int = int(json_data.get("int", 0))
        currency: Optional[str] = json_data.get("currency")

        add_amount: AmountMixin = AmountMixin(amount=add, currency=currency)
        sub_amount: AmountMixin = AmountMixin(amount=sub, currency=currency)
        return org_view_instance._update_total_paid(organization_id=organization_id, add_amount=add_amount,
                                                    subtract_amount=sub_amount)

    elif path == "update-total-members":
        organization_id: Optional[str] = json_data.get("organization_id")
        add: int = int(json_data.get("add", 0))
        sub: int = int(json_data.get("int", 0))

        return org_view_instance._update_total_members(organization_id=organization_id, add=add, subtract=sub)

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
        return org_view_instance._update_total_membership_payments(organization_id=organization_id,
                                                                   subtract_total_membership_payment=sub_amount,
                                                                   add_total_membership_amount=add_amount)






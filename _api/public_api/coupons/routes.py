***REMOVED***

***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from typing import Optional

from flask import Blueprint, request
from config.exceptions import if_bad_request_raise
from security.api_authenticator import handle_api_auth
from views.memberships import CouponsView
coupons_bp = Blueprint('coupons', __name__)


@coupons_bp.route('/api/v1/public/coupons/<path:path>', methods=['POST'])
@handle_api_auth
def coupons(path: str) -> tuple:
    ***REMOVED***
        **coupons endpoint**
            Allows developers to integrate coupon codes functionality into
            the payment plans for services on their website.
        **PARAMETERS**
            :param path: str -> path that indicates the resource to access
            :return tuple: response, status_code -> tuple containing response (in json format) and status_code

            path == "get"
                given organization_id and coupon_code return coupon code details

            path == "create":
                given organization_id, code, discount, expiration_time , create a new coupon

            path == "update":
                given organization_id, code, discount, and expiration_time update coupon code

            path == "cancel":
                given organization_id and code cancel coupon code

            path == "get-all":
                given organization_id return all coupon codes relevant to the organization.

            path == "get-valid":
                given organization_id return valid coupon codes

            path == "get-expired":
                given organization_id return expired coupon codes

    ***REMOVED***
    coupons_view_instance: CouponsView = CouponsView()
    # TODO - include organization_id for this routes, and refactor the view functions
    # Raises Bad Request error if request is not in json format
    if_bad_request_raise(request)
    coupon_data: dict = request.get_json()

    if path == "get":
        return coupons_view_instance.get_coupon(coupon_data=coupon_data)
    elif path == "create":
        return coupons_view_instance.add_coupon(coupon_data=coupon_data)
    elif path == "update":
        return coupons_view_instance.update_coupon(coupon_data=coupon_data)
    elif path == "cancel":
        return coupons_view_instance.cancel_coupon(coupon_data=coupon_data)
    elif path == "get-all":
        organization_id: Optional[str] = coupon_data.get('organization_id')
        return coupons_view_instance.get_all_coupons(organization_id=organization_id)
    elif path == "get-valid":
        organization_id: Optional[str] = coupon_data.get('organization_id')
        return coupons_view_instance.get_valid_coupons(organization_id=organization_id)
    elif path == "get-expired":
        organization_id: Optional[str] = coupon_data.get('organization_id')
        return coupons_view_instance.get_expired_coupons(organization_id=organization_id)
    else:
        pass
    # TODO integrate Coupons to admin app and allow for the app to
    # generate and manage them

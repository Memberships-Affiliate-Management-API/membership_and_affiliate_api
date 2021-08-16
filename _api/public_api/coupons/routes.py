***REMOVED***

***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"


from flask import Blueprint, request
from config.exceptions import if_bad_request_raise
from security.api_authenticator import handle_api_auth
from views.memberships import CouponsView
coupons_bp = Blueprint('coupons', __name__)


@coupons_bp.route('/api/v1/coupons/<path:path>', methods=['POST'])
@handle_api_auth
def coupons(path: str) -> tuple:
    coupons_view_instance: CouponsView = CouponsView()
    # TODO - include organization_id for this routes, and refactor the view functions
    # Raises Bad Request error if request is not in json format
    if_bad_request_raise(request)

    if path == "get":
        coupon_data: dict = request.get_json()
        return coupons_view_instance.get_coupon(coupon_data=coupon_data)
    elif path == "create":
        coupon_data: dict = request.get_json()
        return coupons_view_instance.add_coupon(coupon_data=coupon_data)
    elif path == "update":
        coupon_data: dict = request.get_json()
        return coupons_view_instance.update_coupon(coupon_data=coupon_data)
    elif path == "cancel":
        coupon_data: dict = request.get_json()
        return coupons_view_instance.cancel_coupon(coupon_data=coupon_data)
    elif path == "get-all":
        # TODO supply the required organization_id here
        return coupons_view_instance.get_all_coupons()
    elif path == "get-valid":
        return coupons_view_instance.get_valid_coupons()
    elif path == "get-expired":
        return coupons_view_instance.get_expired_coupons()
    else:
        pass
    # TODO integrate Coupons to admin app and allow for the app to
    # generate and manage them

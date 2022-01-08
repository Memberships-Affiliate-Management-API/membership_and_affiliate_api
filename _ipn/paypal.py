"""
    **PayPal Payments Management _IPN Endpoints**
    allows the app to receive notifications when payments to users and deposit from users where made
    successfully or not successfully

    the _ipn for user deposit to certain organization must be given to the owner of the account
    the owner may use the endpoint while setting up paypal payments on their website
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from flask import Blueprint
paypal_ipn_bp = Blueprint("paypal_ipn", __name__)


@paypal_ipn_bp.route('/_ipn/paypal/deposit/success/<path:path>', methods=["GET", "POST"])
def deposit_successful_ipn(path: str) -> tuple:
    """
    **deposit_successful_ipn**
        deposit is successful capture the approve url and redirect the user there after saving the deposit
        details to the store

        :param path: organization_id
        :return: "OK", 200
    """
    # TODO - get authorization link and redirect the user to this link
    return "OK", 200


@paypal_ipn_bp.route('/_ipn/paypal/deposit/failure/<path:path>', methods=["GET", "POST"])
def deposit_failed_ipn(path: str) -> tuple:
    """
        **deposit_failed_ipn**

        :param path: organization_id
        :return: "OK", 200
    """

    return "OK", 200


@paypal_ipn_bp.route('/_ipn/paypal/deposit/cancelled/<path:path>', methods=["GET", "POST"])
def deposit_cancelled_ipn(path: str) -> tuple:
    """
    **deposit_cancelled_ipn**
        paypal deposit is cancelled handle this event
        path: is organization_id

    :return:
    """
    return "OK", 200


@paypal_ipn_bp.route('/_ipn/paypal/withdrawal/failure/<path:path>', methods=["GET", "POST"])
def withdrawal_failed_ipn(path: str) -> tuple:
    """
        **withdrawal_failed_ipn**

        :param path: organization_id
        :return: "OK", 200
    """

    return "OK", 200


@paypal_ipn_bp.route('/_ipn/paypal/withdrawal/success/<path:path>', methods=["GET", "POST"])
def withdrawal_successful_ipn(path: str) -> tuple:
    """
        **withdrawal_successful_ipn**

        :param path: organization_id
        :return: "OK", 200
    """

    return "OK", 200

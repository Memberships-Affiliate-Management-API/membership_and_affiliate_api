***REMOVED***
    allows the app to receive notifications when payments to users and deposit from users where made
    successfully or not successfully

    the _ipn for user deposit to certain organization must be given to the owner of the account
    the owner may use the endpoint while setting up paypal payments on their website
***REMOVED***
from flask import Blueprint, request
paypal_ipn_bp = Blueprint("paypal_ipn", __name__)


@paypal_ipn_bp.route('/_ipn/paypal/deposit/success/<path:path>', methods=["GET", "POST"])
def deposit_successfull_ipn(path: str) -> tuple:
    ***REMOVED***

    :param path: organization_id
    :return: "OK", 200
    ***REMOVED***

    return "OK", 200


@paypal_ipn_bp.route('/_ipn/paypal/deposit/failure/<path:path>', methods=["GET", "POST"])
def deposit_failed_ipn(path: str) -> tuple:
    ***REMOVED***

    :param path: organization_id
    :return: "OK", 200
    ***REMOVED***

    return "OK", 200


@paypal_ipn_bp.route('/_ipn/paypal/withdrawal/failure/<path:path>', methods=["GET", "POST"])
def withdrawal_failed_ipn(path: str) -> tuple:
    ***REMOVED***

    :param path: organization_id
    :return: "OK", 200
    ***REMOVED***

    return "OK", 200


@paypal_ipn_bp.route('/_ipn/paypal/withdrawal/success/<path:path>', methods=["GET", "POST"])
def withdrawal_successfull_ipn(path: str) -> tuple:
    ***REMOVED***

    :param path: organization_id
    :return: "OK", 200
    ***REMOVED***

    return "OK", 200

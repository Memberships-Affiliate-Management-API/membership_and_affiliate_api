"""
    Wallet API Routes for Memberships & Affiliates Management API
    There are two types of APIS in this module one for clients and
    one for organizations, this is because Organizations also
    owns wallets the same as users and clients.

    User Authentication is handled differently depending on the target or
    purpose of the API
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from flask import Blueprint, request, jsonify

from config.exceptions import if_bad_request_raise
from security.api_authenticator import handle_api_auth
from views import wallet_view

wallet_bp = Blueprint("wallet", __name__)


# NOTE: there is no reason to cache API routes as the cache is on the view level


@wallet_bp.route('/api/v1/public/wallet', methods=["GET", "POST", "DELETE", "PUT"])
@handle_api_auth
def wallet() -> tuple:
    """
        Wallet API Endpoint for servicing users and clients.
    :return: tuple containing response and status code
    """
    # Raises Bad Request error if request is not in json format
    if_bad_request_raise(request)
    json_data: dict = request.get_json()

    if request.method == "GET":
        organization_id: str = json_data.get('organization_id')
        uid: str = json_data.get('uid')

        return wallet_view.get_wallet(organization_id=organization_id, uid=uid)

    if request.method == "POST":

        uid: str = json_data.get('uid')
        organization_id: str = json_data.get('organization_id')
        currency: str = json_data.get('currency')
        paypal_address: str = json_data.get('paypal_address')

        return wallet_view.create_wallet(organization_id=organization_id,
                                         uid=uid,
                                         currency=currency,
                                         paypal_address=paypal_address)
    if request.method == "PUT":
        return wallet_view.update_wallet(wallet_data=json_data)

    if request.method == "DELETE":
        return wallet_view.reset_wallet(wallet_data=json_data)
    
    return jsonify({'status': False, 'message': 'Unable to process this request please check your parameters'}), 500


@wallet_bp.route('/api/v1/public/wallet/organization', methods=["GET", "POST", "DELETE", "PUT"])
@handle_api_auth
def org_wallet() -> tuple:
    # NOTE: deprecated remove this endpoint
    """
        API Endpoint for organizational Accounts and Administrative Purposes
    :return: response as tuple
    """
    if_bad_request_raise(request)
    json_data: dict = request.get_json()

    if request.method == "GET":
        # Fetching the organizational Wallet
        organization_id: str = json_data.get('organization_id')
        uid: str = json_data.get('uid')

        return wallet_view.get_wallet(organization_id=organization_id, uid=uid)

    if request.method == "POST":
        # Creating organizational Wallet
        uid: str = json_data.get('uid')
        organization_id: str = json_data.get('organization_id')
        currency: str = json_data.get('currency')
        paypal_address: str = json_data.get('paypal_address')

        return wallet_view.create_wallet(organization_id=organization_id,
                                         uid=uid,
                                         currency=currency,
                                         paypal_address=paypal_address,
                                         is_org_wallet=True)
    if request.method == "PUT":
        # NOTE: Updating organization Wallet
        return wallet_view.update_wallet(wallet_data=json_data)
    
    return jsonify({'status': False, 'message': 'Unable to process this request please check your parameters'}), 500


@wallet_bp.route('/api/v1/public/wallet/organization/<string:organization_id>', methods=["GET"])
@handle_api_auth
def organization_wallets(organization_id: str) -> tuple:
    """
    **organization_wallets**
            returns all wallets relating to a specific organization.
            # TODO try and determine if we really need this functionality

        :param organization_id: the id of the organization from which the wallets will be obtained
        :param path: organization_id for the organization to fetch wallets from
        :return: response as tuple

    """
    return wallet_view.return_all_wallets(organization_id=organization_id)
        
    


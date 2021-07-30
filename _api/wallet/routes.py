***REMOVED***
    Wallet API Routes for Memberships & Affiliates Management API
    There are two types of APIS in this module one for clients and
    one for organizations, this is because Organizations also
    owns wallets the same as users and clients.

    User Authentication is handled differently depending on the target or
    purpose of the API
***REMOVED***
from flask import Blueprint, request, jsonify

from security.api_authenticator import handle_api_auth
from views.wallet import WalletView
wallet_bp = Blueprint("wallet", __name__)

# NOTE: there is no reason to cache API routes as the cache is on the view level


@wallet_bp.route('/api/v1/wallet', methods=["GET", "POST", "DELETE", "PUT"])
@handle_api_auth
def wallet() -> tuple:
    ***REMOVED***
        Wallet API Endpoint for servicing users and clients.
    :return: tuple containing response and status code
    ***REMOVED***
    wallet_instance: WalletView = WalletView()

    if request.method == "GET":
        json_data: dict = request.get_json()

        organization_id: str = json_data.get('organization_id')
        uid: str = json_data.get('uid')

        return wallet_instance.get_wallet(organization_id=organization_id, uid=uid)

    elif request.method == "POST":
        json_data: dict = request.get_json()

        uid: str = json_data.get('uid')
        organization_id: str = json_data.get('organization_id')
        currency: str = json_data.get('currency')
        paypal_address: str = json_data.get('paypal_address')

        return wallet_instance.create_wallet(organization_id=organization_id,
                                             uid=uid,
                                             currency=currency,
                                             paypal_address=paypal_address)
    elif request.method == "PUT":
        json_data: dict = request.get_json()
        return wallet_instance.update_wallet(wallet_data=json_data)

    elif request.method == "DELETE":
        json_data: dict = request.get_json()
        return wallet_instance.reset_wallet(wallet_data=json_data)
    else:
        return jsonify({'status': False, 'message': 'Unable to process this request please check your parameters'}), 500


@wallet_bp.route('/api/v1/wallet/organization', methods=["GET", "POST", "DELETE", "PUT"])
def org_wallet() -> tuple:
    # TODO Finalize of the authentication method to use here
    ***REMOVED***
        API Endpoint for organizational Accounts and Administrative Purposes
    :return: response as tuple
    ***REMOVED***
    wallet_instance: WalletView = WalletView()

    if request.method == "GET":
        # Fetching the organizational Wallet
        json_data: dict = request.get_json()

        organization_id: str = json_data.get('organization_id')
        uid: str = json_data.get('uid')

        return wallet_instance.get_wallet(organization_id=organization_id, uid=uid)

    elif request.method == "POST":
        # Creating organizational Wallet
        json_data: dict = request.get_json()

        uid: str = json_data.get('uid')
        organization_id: str = json_data.get('organization_id')
        currency: str = json_data.get('currency')
        paypal_address: str = json_data.get('paypal_address')

        return wallet_instance.create_wallet(organization_id=organization_id,
                                             uid=uid,
                                             currency=currency,
                                             paypal_address=paypal_address,
                                             is_org_wallet=True)
    elif request.method == "PUT":
        # NOTE: Updating organization Wallet
        json_data: dict = request.get_json()
        return wallet_instance.update_wallet(wallet_data=json_data)

    else:
        return jsonify({'status': False, 'message': 'Unable to process this request please check your parameters'}), 500


@wallet_bp.route('/api/v1/wallet/organization/<path:path>', methods=["GET"])
def organization_wallets(path: str) -> tuple:
    ***REMOVED***
            returns all wallets relating to a specific organization.
            # TODO try and determine if we really need this functionality

        :param path: organization_id for the organization to fetch wallets from
        :return: response as tuple

    ***REMOVED***
    pass

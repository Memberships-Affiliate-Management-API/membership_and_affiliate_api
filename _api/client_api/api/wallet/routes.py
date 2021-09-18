"""
    **Wallet API Endpoint**

"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"


from flask import Blueprint, request, current_app, jsonify
from config.exceptions import error_codes, UnAuthenticatedError, if_bad_request_raise
from security.apps_authenticator import handle_apps_authentication, verify_secret_key
from views import wallet_view
from typing import Optional

# TODO - Could move this to the main api if needed
wallet_client_api_bp = Blueprint("wallet_client_api", __name__)


@wallet_client_api_bp.route('/_api/v1/client/wallet/<string:path>', methods=['POST'])
@handle_apps_authentication
def client_wallets(path: str) -> tuple:
    """
        **client_wallets**
            allows client applications to perform transactions on client wallets

    :param path:
    :return:
    """
    if_bad_request_raise(request)
    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get("SECRET_KEY")
    verify_secret_key(secret_key)

    if path == 'create-wallet':
        uid: str = json_data.get('uid')
        organization_id: str = json_data.get('organization_id')
        currency: str = json_data.get('currency')
        paypal_address: str = json_data.get('paypal_address')
        return wallet_view.create_wallet(organization_id=organization_id, uid=uid, currency=currency,
                                         paypal_address=paypal_address)
    elif path == 'get-wallet':
        organization_id: str = json_data.get('organization_id')
        uid: str = json_data.get('uid')
        return wallet_view.get_wallet(organization_id=organization_id, uid=uid)
    elif path == 'update':
        return wallet_view.update_wallet(wallet_data=json_data)
    elif path == 'delete':
        return wallet_view.reset_wallet(wallet_data=json_data)
    elif path == 'deposit':
        uid: str = json_data.get('uid')
        organization_id: str = json_data.get('organization_id')
        currency: str = json_data.get('currency')
        # Note: Amount is in cents
        amount: int = json_data.get('amount')
        paypal_address: str = json_data.get('paypal_address')
        # TODO: Send deposit request to paypal - once the request has been verified and succeeded
        #  paypal will call the _ipn with the deposit details - after this details have been
        #  verified from the _IPN then deposit amount will be credited
        return jsonify(dict(status=False, message='Under Development')), error_codes.remote_data_error

    elif path == 'withdraw':
        uid: str = json_data.get('uid')
        organization_id: str = json_data.get('organization_id')
        currency: str = json_data.get('currency')
        # Note: Amount is in cents
        amount: int = json_data.get('amount')
        return wallet_view._wallet_withdraw_funds(organization_id=organization_id, uid=uid, amount=amount)

    elif path == 'balance':
        uid: str = json_data.get('uid')
        organization_id: str = json_data.get('organization_id')
        return wallet_view.get_wallet(organization_id=organization_id, uid=uid)

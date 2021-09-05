
from flask import Blueprint, request

from config.exceptions import if_bad_request_raise
from security.apps_authenticator import handle_internal_auth
from views import wallet_view

internal_api_bp = Blueprint('internal_api', __name__)


@internal_api_bp.route('_api/v1/internal/wallet/organization/<string:path>', methods=['POST'])
@handle_internal_auth
def int_organizational_wallets(path: str) -> tuple:
    ***REMOVED***

        :return: tuple
    ***REMOVED***
    if_bad_request_raise(request)
    json_data: dict = request.get_json()

    if path == 'create-wallet':
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

from flask import Blueprint, request, jsonify
from views.wallet import WalletView
wallet_bp = Blueprint("wallet", __name__)


@wallet_bp.route('/api/v1/wallet', methods=["GET", "POST", "DELETE", "PUT"])
def wallet() -> tuple:
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


@wallet_bp.route('/api/v1/organization/wallet', methods=["GET", "POST", "DELETE", "PUT"])
def org_wallet() -> tuple:
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
                                             paypal_address=paypal_address,
                                             is_org_wallet=True)
    elif request.method == "PUT":
        json_data: dict = request.get_json()
        return wallet_instance.update_wallet(wallet_data=json_data)

    elif request.method == "DELETE":
        json_data: dict = request.get_json()
        return wallet_instance.reset_wallet(wallet_data=json_data)
    else:
        return jsonify({'status': False, 'message': 'Unable to process this request please check your parameters'}), 500

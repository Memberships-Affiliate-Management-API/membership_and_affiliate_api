from flask import Blueprint, request, current_app
from config.exceptions import error_codes, UnAuthenticatedError, if_bad_request_raise
from security.apps_authenticator import handle_apps_authentication
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
    user_data: dict = request.get_json()
    secret_key: Optional[str] = user_data.get("SECRET_KEY")

    if path == 'withdraw-funds':
        pass
    elif path == 'deposit-funds':
        pass
    elif path == 'balance':
        pass




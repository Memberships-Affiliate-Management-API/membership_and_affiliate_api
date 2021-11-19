"""
    Swagger Compatible API for wallet
"""
from flask_apispec import doc
from _api._swagger_api import ViewModel
from security.api_authenticator import handle_api_auth
from flask_restful import marshal_with
from views import wallet_view
from _api._swagger_api.schemas.wallet import WalletPayloadSchema, WalletResponseSchema, WalletListResponseSchema


# TODO add request Schema


class WalletView(ViewModel):
    """
        **WalletView**
            get, update, delete Wallet
    """
    methods = ["GET", "PUT", "DELETE"]
    method_decorators = [handle_api_auth]

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    @doc(description=wallet_view.get_wallet.__doc__)
    @marshal_with(WalletResponseSchema)
    def get(organization_id: str, uid: str) -> tuple:
        """
            eval(wallet_view.get_wallet.__doc__)
        :return:
        """
        return wallet_view.get_wallet(organization_id=organization_id, uid=uid)

    @staticmethod
    @doc(description=wallet_view.update_wallet.__doc__)
    @marshal_with(WalletResponseSchema)
    def put(wallet_dict: dict) -> tuple:
        """
            updates an existing wallet by uid
        :return:
        """
        return wallet_view.update_wallet(wallet_data=wallet_dict)

    @staticmethod
    @doc(description=wallet_view.reset_wallet.__doc__)
    @marshal_with(WalletResponseSchema)
    def delete(organization_id: str, uid: str) -> tuple:
        """
            deletes an existing wallet by uid
        :return:
        """
        return wallet_view.reset_wallet(wallet_data=dict(organization_id=organization_id, uid=uid))


class WalletListView(ViewModel):
    """
        **WalletListView**
            returns a list of all wallets for a specific organization
    """
    methods = ["GET"]
    method_decorators = [handle_api_auth]

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    @doc(description=wallet_view.return_all_wallets.__doc__)
    @marshal_with(WalletListResponseSchema)
    def get(organization_id: str) -> tuple:
        """
        **get**
            will return a list of all wallets belonging to a specific organization
        :return:
        """
        return wallet_view.return_all_wallets(organization_id=organization_id)


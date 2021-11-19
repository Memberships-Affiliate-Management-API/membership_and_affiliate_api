"""
    Swagger Compatible API for wallet
"""
from datetime import datetime
from flask_apispec import doc
from _api._swagger_api import ViewModel
from security.api_authenticator import handle_api_auth
from flask_restful import fields, marshal_with
from marshmallow import Schema, fields
from views import wallet_view
from database.wallet import WalletModel


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

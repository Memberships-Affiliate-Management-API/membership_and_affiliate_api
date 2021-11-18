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


class AmountSchema(Schema):
    amount_cents = fields.Integer(default=0)
    currency: str = fields.String()


# Wallet Payload Schema
class WalletPayloadSchema(Schema):
    organization_id: str = fields.String()
    uid: str = fields.String()
    wallet_id: str = fields.String()
    is_org_wallet: bool = fields.Boolean(default=False)
    available_funds = fields.Nested(AmountSchema)
    monthly_withdrawal_allowance = fields.Nested(AmountSchema)
    time_created: datetime = fields.DateTime()
    last_transaction_time: datetime = fields.DateTime()
    paypal_address: str = fields.String()
    is_verified: bool = fields.String()


# Wallet Response Schema
WalletResponseSchema = dict(
    status=fields.Boolean(default=False),
    message=fields.String(),
    payload=fields.Nested(WalletPayloadSchema))

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

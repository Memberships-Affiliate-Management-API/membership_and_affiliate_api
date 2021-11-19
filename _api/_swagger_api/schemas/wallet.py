"""
    **Wallet Schemas**
"""
import required
from marshmallow import Schema, fields
from datetime import datetime
from _api._swagger_api.schemas.amount import AmountSchema


# Wallet Payload Schema
class WalletPayloadSchema(Schema):
    """
        **Class WalletPayloadSchema**
            a schema for payload
    """
    organization_id: str = fields.String(required=True)
    uid: str = fields.String(required=True)
    wallet_id: str = fields.String(required=True)
    is_org_wallet: bool = fields.Boolean(default=False)
    available_funds = fields.Nested(AmountSchema)
    monthly_withdrawal_allowance = fields.Nested(AmountSchema)
    time_created: datetime = fields.DateTime()
    last_transaction_time: datetime = fields.DateTime()
    paypal_address: str = fields.String()
    is_verified: bool = fields.String()


# Wallet Response Schema
class WalletResponseSchema(Schema):
    """
        **WalletResponseSchema**
            a schema for wallet responses
    """
    status = fields.Boolean(default=False)
    message = fields.String()
    payload = fields.Nested(WalletPayloadSchema)


class WalletListResponseSchema(Schema):
    """
        a schema for returning list of wallets
    """
    status = fields.Boolean(default=False)
    message = fields.String()
    payload = fields.List(WalletPayloadSchema)

"""
    **Wallet Schemas**
"""

from flask_restful import fields, marshal_with
from marshmallow import Schema, fields
from datetime import datetime



class AmountSchema(Schema):
    """
        ** Class AmountSchema **

    """
    amount_cents = fields.Integer(default=0)
    currency: str = fields.String()


# Wallet Payload Schema
class WalletPayloadSchema(Schema):
    """
        **Class WalletPayloadSchema**
            a schema for payload
    """
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
class WalletResponseSchema(Schema):
    """
        **WalletResponseSchema**
            a schema for wallet responses
    """
    status = fields.Boolean(default=False)
    message = fields.String()
    payload = fields.Nested(WalletPayloadSchema)



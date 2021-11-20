"""
    **Wallet Schemas**
"""
import required
from lxml.html._diffcommand import description
from marshmallow import Schema, fields
from datetime import datetime
from _swagger_api.schemas.amount import AmountSchema


# Wallet Payload Schema
class WalletPayloadSchema(Schema):
    """
        **Class WalletPayloadSchema**
            a schema for payload
    """
    organization_id: str = fields.String(required=True, description='organization id of the registered organization')
    uid: str = fields.String(required=True, description='user id of the user making the request')
    wallet_id: str = fields.String(required=True, description='wallet_id the id of the wallet')
    is_org_wallet: bool = fields.Boolean(default=False, description='True if this wallet is an organization wallet')
    available_funds = fields.Nested(AmountSchema, description='indicates funds available in the wallet')
    monthly_withdrawal_allowance = fields.Nested(AmountSchema, description='indicates funds available for withdrawal')
    time_created: datetime = fields.DateTime(description='the date and time the wallet was created')
    last_transaction_time: datetime = fields.DateTime(description='the date the last transaction was performed')
    paypal_address: str = fields.String(description='paypal address attached to wallet - withdrawals will be sent to this address')
    is_verified: bool = fields.String(description='True if wallet is verified, only verified wallets can receive withdrawals')


# Wallet Response Schema
class WalletResponseSchema(Schema):
    """
        **WalletResponseSchema**
            a schema for wallet responses
    """
    status = fields.Boolean(default=False)
    message = fields.String()
    payload = fields.Nested(WalletPayloadSchema)


class WalletListResponseSchema(WalletResponseSchema):
    """
        a schema for returning list of wallets
    """
    payload = fields.List(fields.Nested(WalletPayloadSchema), description='List of wallets')

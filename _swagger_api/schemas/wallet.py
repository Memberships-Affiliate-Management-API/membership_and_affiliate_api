"""
    **Wallet Schemas**
"""
from marshmallow import Schema, fields
from datetime import datetime
from _swagger_api.schemas.amount import AmountSchema
# Wallet Payload Schema
from _swagger_api.schemas.response import ResponseSchema


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
class WalletResponseSchema(ResponseSchema):
    """
        **WalletResponseSchema**
            a schema for wallet responses
    """
    payload = fields.Nested(WalletPayloadSchema, description='wallet payload')


class WalletListResponseSchema(ResponseSchema):
    """
        ** Class WalletListResponseSchema **
            a schema for returning list of wallets
    """
    payload = fields.Nested(WalletPayloadSchema(many=True), description='List of wallets')


class WalletRequestSchema(Schema):
    """
        **Class WalletRequestSchema**
            a schema for wallet requests
    """
    payload = fields.Nested(WalletPayloadSchema, description='description of wallet request')

"""
    Amount Mixin Schema
"""
from marshmallow import Schema, fields


class AmountSchema(Schema):
    """
        ** Class AmountSchema **

    """
    amount_cents = fields.Integer(default=0, required=True, description='amount in cents')
    currency: str = fields.String(required=True, description='currency symbol')

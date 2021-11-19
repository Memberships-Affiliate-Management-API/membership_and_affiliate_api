"""
    Amount Mixin Schema
"""
from marshmallow import Schema, fields


class AmountSchema(Schema):
    """
        ** Class AmountSchema **

    """
    amount_cents = fields.Integer(default=0, required=True)
    currency: str = fields.String(required=True)

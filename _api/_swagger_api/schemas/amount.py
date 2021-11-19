"""
    Amount Mixin Schema
"""
from marshmallow import Schema, fields


class AmountSchema(Schema):
    """
        ** Class AmountSchema **

    """
    amount_cents = fields.Integer(default=0)
    currency: str = fields.String()

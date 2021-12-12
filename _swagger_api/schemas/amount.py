"""
    Amount Mixin Schema
"""
from marshmallow import Schema, fields


class AmountSchema(Schema):
    """
        ** Class AmountSchema **

        `PARAMETERS`
            amount_cents: integer
            currency: integer
    """
    amount_cents = fields.Integer(default=0, required=True, description='amount in cents')
    currency: str = fields.String(required=True, description='currency symbol')


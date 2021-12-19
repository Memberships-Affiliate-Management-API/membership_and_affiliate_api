"""
    Coupons schema
"""
from marshmallow import Schema, fields
from _swagger_api.schemas.response import ResponseSchema


class PayloadSchema(Schema):
    """
    ** Class CouponPayloadSchema **
        Coupon schema

    """
    organization_id = fields.Integer(required=True)
    code = fields.String(required=True)
    discount_percent = fields.Float()
    is_valid = fields.Boolean(default=True)
    date_created = fields.DateTime(required=True)
    expiration_time = fields.Integer(required=True)


class CouponResponseSchema(ResponseSchema):
    """
        Coupon schema
    """
    payload = fields.Nested(PayloadSchema)


class CouponResponseListSchema(ResponseSchema):
    """
        Coupon schema
            payload: request payload
    """
    payload = fields.Nested(PayloadSchema, many=True)

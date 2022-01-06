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
    organization_id = fields.Integer(required=True, description='a unique id for the organization')
    code = fields.String(required=True, description='coupon code')
    discount_percent = fields.Float(description='discount amount in percent the coupon code offers')
    is_valid = fields.Boolean(default=True, description='True if coupon code is valid')
    date_created = fields.DateTime(required=True, description='The date the coupon was created, this value will '
                                                              'be auto generated')
    expiration_time = fields.Integer(required=True, description='time of expiration (time stamp) for the coupon code')


class CouponResponseSchema(ResponseSchema):
    """
        ** Class CouponResponseSchema **
            Coupon schema
    """
    payload = fields.Nested(PayloadSchema)


class CouponResponseListSchema(ResponseSchema):
    """
        ** Coupon Response List Schema **
            payload: request payload
    """
    payload = fields.Nested(PayloadSchema, many=True)

from datetime import datetime, date
from marshmallow import Schema, fields, validate, ValidationError
from _swagger_api.schemas.response import ResponseSchema


class MembershipPayloadSchema(Schema):
    """
    ** Class MembershipPayloadSchema **
        Schema for the response of a membership
    """
    organization_id: str = fields.String()
    uid: str = fields.String()
    plan_id: str = fields.String()
    payment_status: str = fields.String(validate=validate.OneOf(['paid', 'unpaid']))
    date_created: datetime = fields.DateTime(default=datetime.now())
    plan_start_date: date = fields.Date(default=datetime.now().date())
    payment_method: str = fields.String(validate=validate.OneOf(['paypal', 'eft']))
    is_active_subscription: bool = fields.Boolean(default=True)


class MembershipResponseSchema(ResponseSchema):
    """
        **Class MembershipResponseSchema**
            will send a single payload as response
    """
    payload = fields.Nested(MembershipPayloadSchema)


class MembershipResponseListSchema(ResponseSchema):
    """
        ** Class MembershipResponseListSchema **
            will send a list of payloads as response
    """
    payload = fields.Nested(MembershipResponseSchema(many=True))


class MembershipPaymentPayloadSchema(Schema):
    """
        ** Class MembershipPaymentPayloadSchema **
            Membership Payments Schema
    """
    organization_id: str = fields.String()
    uid: str = fields.String()
    plan_id: str = fields.String()
    payment_method: str = fields.String(validate=validate.OneOf(['paypal', 'eft']))
    payment_amount: int = fields.Integer()


class MembershipPaymentResponseSchema(ResponseSchema):
    """
        ** Class MembershipPaymentResponseSchema **
            membership payment response schema
    """
    payload = fields.Nested(MembershipPaymentPayloadSchema)


class MembershipPaymentResponseListSchema(ResponseSchema):
    """
        **Class MembershipPaymentResponseListSchema **
            membership payment list response schema
    """
    payload = fields.Nested(MembershipPaymentPayloadSchema)

from datetime import datetime, date

from marshmallow import Schema, fields, validate, ValidationError
from _swagger_api.schemas.response import ResponseSchema


class MembershipPayloadSchema(Schema):
    """
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
    """will send a single payload as response"""
    payload = fields.Nested(MembershipPayloadSchema)


class MembershipResponseListSchema(ResponseSchema):
    """ will send a list of payloads as response"""
    payload = fields.Nested(MembershipResponseSchema(many=True))

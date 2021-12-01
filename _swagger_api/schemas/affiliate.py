from datetime import datetime
from marshmallow import Schema, fields
from _swagger_api.schemas.response import ResponseSchema


class AffiliatePayloadSchema(Schema):
    """
        **Class AffiliatePayloadSchema**
    """
    organization_id: str = fields.String()
    affiliate_id: str = fields.String()
    uid: str = fields.String()
    last_updated: datetime = fields.DateTime()
    datetime_recruited: datetime = fields.DateTime()
    total_recruited: int = fields.Integer(default=0)
    is_active: bool = fields.Boolean(default=True)
    is_deleted: bool = fields.Boolean(default=False)


class AffiliateResponseSchema(ResponseSchema):
    """
        **Class AffiliateResponseSchema**
    """
    payload = fields.Nested(AffiliatePayloadSchema)


class AffiliateListResponseSchema(ResponseSchema):
    """
        **Class AffiliateListResponseSchema**
    """
    payload = fields.Nested(AffiliatePayloadSchema(many=True))




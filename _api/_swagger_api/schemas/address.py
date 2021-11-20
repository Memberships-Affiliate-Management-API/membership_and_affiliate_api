from marshmallow import Schema, fields


class AddressSchema(Schema):
    """
            **Class AddressSchema**
    """
    organization_id: str = fields.String(required=True)
    uid: str = fields.String(required=True)
    line_1: str = fields.String(required=True)
    city: str = fields.String()
    zip_code: str = fields.String(required=True)
    province: str = fields.String()
    state: str = fields.String()
    country: str = fields.String()

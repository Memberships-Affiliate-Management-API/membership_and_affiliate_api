from marshmallow import Schema, fields


class AddressSchema(Schema):
    """
            **Class AddressSchema**
    """
    organization_id: str = fields.String(required=True, description='the id of the registered organization')
    uid: str = fields.String(required=True, description='user id of the user making the request')
    line_1: str = fields.String(required=True, description='address line_1 field')
    city: str = fields.String(description='address city')
    zip_code: str = fields.String(required=True, description='address postal or zip code')
    province: str = fields.String(description='province if available')
    state: str = fields.String(description='address state')
    country: str = fields.String(description='address country')

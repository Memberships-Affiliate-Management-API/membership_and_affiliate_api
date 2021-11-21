from marshmallow import Schema, fields


class AuthPayload(Schema):
    organization_id: str = fields.String(required=True)
    uid: str = fields.String()
    email: str = fields.String(required=True)
    password: str = fields.String()
    token: str = fields.String()


class AuthSchema(Schema):
    payload = fields.Nested(AuthPayload)


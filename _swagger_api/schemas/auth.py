from marshmallow import Schema, fields


class AuthPayload(Schema):
    """
        ** Class AuthPayload **
            Auth payload schema
    """
    organization_id: str = fields.String(required=True)
    uid: str = fields.String()
    email: str = fields.String(required=True)
    password: str = fields.String()
    token: str = fields.String()


class AuthSchema(Schema):
    """
        ** Class AuthSchema **
            authorization schema
    """
    payload = fields.Nested(AuthPayload)


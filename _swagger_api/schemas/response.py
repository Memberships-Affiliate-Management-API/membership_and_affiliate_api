from marshmallow import Schema, fields


class ResponseSchema(Schema):
    """
    ** Class ResponseSchema **
        basic response schema all responses will be follow this basic structure
    """
    status = fields.Boolean(default=False, description='final status of request, True if successful')
    message = fields.String(description='message describing the results of the request')

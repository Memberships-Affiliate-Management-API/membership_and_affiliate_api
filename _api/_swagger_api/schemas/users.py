"""
    **Users Schema Classes**
"""

from marshmallow import Schema, fields
from datetime import datetime, date

from _api._swagger_api.schemas.address import AddressSchema


class UserPayloadSchema(Schema):
    """
        Payload Schema for Users
    """
    organization_id: str = fields.String(required=True)
    uid: str = fields.String(required=True)
    names: str = fields.String()
    surname: str = fields.String()
    cell: str = fields.String()
    email: str = fields.String(required=True)
    email_verified: bool = fields.Boolean(default=False)
    password: str = fields.String()
    is_active: bool = fields.Boolean(default=True)
    time_registered: int = fields.Integer()
    is_admin: bool = fields.Boolean(default=False)
    is_support: bool = fields.Boolean(default=False)
    address = fields.Nested(AddressSchema)
    recovery_code: str = fields.String()
    last_login_date: date = fields.Date()


class UserResponseSchema(Schema):
    """
        Response Schema for users
    """
    status: bool = fields.Boolean(default=False)
    message: str = fields.String()
    payload = fields.Nested(UserPayloadSchema)


class UsersListResponseSchema(UserResponseSchema):
    """
        List of Users Response Schema
    """
    payload = fields.List(UserPayloadSchema)

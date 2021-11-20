"""
    **Users Schema Classes**
"""
from lxml.html._diffcommand import description
from marshmallow import Schema, fields
from datetime import datetime, date

from _swagger_api.schemas.address import AddressSchema


class UserPayloadSchema(Schema):
    """
        Payload Schema for Users
    """
    organization_id: str = fields.String(required=True, description='id of the registered organization')
    uid: str = fields.String(required=True, description='user id of the user making the request')
    names: str = fields.String(description='name of user')
    surname: str = fields.String(description='surname of user')
    cell: str = fields.String(description='cell phone number of user')
    email: str = fields.String(required=True, description='email address of user')
    email_verified: bool = fields.Boolean(default=False, description='if email is verified this should be True')
    password: str = fields.String(description='user password')
    is_active: bool = fields.Boolean(default=True, description='if user is active this will be true')
    time_registered: int = fields.Integer(description='the time the user was registered')
    is_admin: bool = fields.Boolean(default=False, description='if user is admin this would be True')
    is_support: bool = fields.Boolean(default=False, description='if user is a member of the support team this will be true')
    address = fields.Nested(AddressSchema, description='User Address')
    recovery_code: str = fields.String(description='recovery code if password reset is requested')
    last_login_date: date = fields.Date(description='date of last login')


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

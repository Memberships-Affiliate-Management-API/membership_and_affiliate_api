from __future__ import annotations

from flask_apispec import doc, marshal_with, use_kwargs
from _swagger_api import ViewModel
from _swagger_api.schemas.auth import AuthSchema
from _swagger_api.schemas.users import UserResponseSchema, UsersListResponseSchema, UserRequestSchema
from security.api_authenticator import handle_api_auth
from security.apps_authenticator import handle_apps_authentication
from views import user_view


class UserViewModel(ViewModel):
    """
        **Class UserViewModel**

    """

    def __new__(cls, *args, **kwargs) -> UserViewModel:
        """new UserViewModel"""
        cls.methods = ['GET', 'POST', 'PUT', 'DELETE']
        cls.method_decorators = [handle_api_auth]
        return super().__new__(cls, *args, **kwargs)

    def __init__(self) -> None:
        """Initialize UserViewModel"""
        super().__init__()

    @staticmethod
    def user_details(payload: dict) -> dict:
        """
            parses payload and returns valid variables
        :param payload:
        :return:
        """
        organization_id: str = payload.get('organization_id')
        names: str = payload.get('names')
        surname: str = payload.get('surname')
        cell: str = payload.get('cell')
        email: str = payload.get('email')
        password: str = payload.get('password')
        uid: str = payload.get('uid')

        return dict(names=names, cell=cell, email=email, organization_id=organization_id, password=password,
                    surname=surname, uid=uid)

    @staticmethod
    @doc(description=user_view.get_user.__doc__)
    @marshal_with(UserResponseSchema)
    def get(organization_id: str, uid: str) -> tuple:
        """
        ** get **
            returns a user with a matching organization_id and uid
        :param organization_id: id of the organization the user belongs to
        :param uid: user id
        :return: tuple
        """
        return user_view.get_user(organization_id=organization_id, uid=uid)

    @staticmethod
    @doc(description=user_view.add_user.__doc__)
    @marshal_with(UserResponseSchema)
    @use_kwargs(UserRequestSchema, location='json')
    def post(**payload) -> tuple:
        """
        ** create post **
            fetches a single user by organization_id and uid
        :param payload: a dictionary containing user data
        :return: user
        """
        return user_view.add_user(**UserViewModel.user_details(payload))

    @staticmethod
    @doc(description=user_view.update_user.__doc__)
    @marshal_with(UserResponseSchema)
    @use_kwargs(UserRequestSchema, location='json')
    def put(**payload) -> tuple:
        """
            **updates**
                provided the user already exists update the user
        :param payload:
        :return: tuple
        """
        is_admin: bool = payload.get('is_admin')
        is_support: bool = payload.get('is_support')

        return user_view.update_user(**UserViewModel.user_details(payload),
                                     is_admin=is_admin, is_support=is_support)


class AuthViewModel(ViewModel):
    """
        an endpoint for handling user authentication
    """

    def __new__(cls, *args, **kwargs):
        """new AuthViewModel"""
        cls.methods = ['GET', 'POST', 'PUT']
        cls.method_decorators = [handle_api_auth]
        return super().__new__(cls, *args, **kwargs)

    def __init__(self) -> None:
        """initialize AuthViewModel"""
        super().__init__()

    @staticmethod
    @doc(description=user_view.logout.__doc__)
    @marshal_with(AuthSchema)
    @use_kwargs(AuthSchema, location='json')
    def put(**payload) -> tuple:
        """
        **sign-out user**
            will sign out the user through token invalidation

        :param payload: contains user authentication payload
        :return: tuple
        """
        organization_id: str = payload.get('organization_id')
        uid: str = payload.get('uid')
        token: str = payload.get('token')
        return user_view.logout(organization_id=organization_id, uid=uid, token=token)

    @staticmethod
    @doc(description=user_view.login.__doc__)
    @marshal_with(UserResponseSchema)
    @use_kwargs(AuthSchema, location='json')
    def post(**payload) -> tuple:
        """
        **user-login**
            will login a user into his or her account

        :param payload: the organization_id of the organization the user is registered in
        :return: tuple containing results
        """
        # organization_id: str, email: str, password: str
        organization_id: str = payload.get('organization_id')
        email: str = payload.get('email')
        password: str = payload.get('password')
        return user_view.login(organization_id=organization_id, email=email, password=password)


class UserListView(ViewModel):
    """
        **Class UserListView**
            allows admins to access a list of users
    """

    def __new__(cls, *args, **kwargs):
        """creating UserListView"""
        cls.methods = ["GET"]
        cls.method_decorators = [handle_apps_authentication]
        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        """initialize UserListView"""
        super().__init__()

    @staticmethod
    @doc(description=user_view.get_all_users.__doc__)
    @marshal_with(UsersListResponseSchema)
    def get(organization_id: str) -> tuple:
        """
            :param organization_id: organization_id of the admin
            :param uid:  user id of the admin users
            :return: tuple
        """
        return user_view.get_all_users(organization_id=organization_id)

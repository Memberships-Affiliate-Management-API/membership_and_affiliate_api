from __future__ import annotations
from flask_apispec import doc, marshal_with

from _swagger_api import ViewModel
from _swagger_api.schemas.users import UserResponseSchema, UsersListResponseSchema
from security.api_authenticator import handle_api_auth
from views import user_view


class UserViewModel(ViewModel):
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    method_decorators = [handle_api_auth]

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    @doc(description=user_view.add_user.__doc__)
    @marshal_with(schema=UserResponseSchema)
    def get(organization_id: str, uid: str) -> tuple:
        """
            returns a user with a matching organization_id and uid
        :param organization_id:
        :param uid:
        :return:
        """
        return user_view.get_user(organization_id=organization_id, uid=uid)

    @staticmethod
    @doc(description=user_view.add_user.__doc__)
    @marshal_with(schema=UserResponseSchema)
    def post(user_data: dict) -> tuple:
        """
            fetches a single user by organization_id and uid
        :param user_data: a dictionary containing user data
        :return: user
        """
        organization_id: str = user_data.get('organization_id')
        names: str = user_data.get('names')
        surname: str = user_data.get('surname')
        cell: str = user_data.get('cell')
        email: str = user_data.get('email')
        password: str = user_data.get('password')
        uid: str = user_data.get('uid')

        return user_view.add_user(organization_id=organization_id, uid=uid, names=names, surname=surname, cell=cell,
                                  email=email, password=password)

    @staticmethod
    @doc(description=user_view.update_user.__doc__)
    @marshal_with(schema=UserResponseSchema)
    def put(user_data: dict) -> tuple:
        """
            **updates**
                provided the user already exists update the user
        :param user_data:
        :return: tuple
        """
        organization_id: str = user_data.get('organization_id')
        names: str = user_data.get('names')
        surname: str = user_data.get('surname')
        cell: str = user_data.get('cell')
        email: str = user_data.get('email')
        password: str = user_data.get('password')
        uid: str = user_data.get('uid')
        is_admin: bool = user_data.get('is_admin')
        is_support: bool = user_data.get('is_support')

        return user_view.update_user(organization_id=organization_id, uid=uid, names=names, surname=surname, cell=cell,
                                     email=email, is_admin=is_admin, is_support=is_support)


class AuthViewModel(ViewModel):
    """
        an endpoint for handling user authentication
    """
    methods = ['GET', 'POST', 'PUT']
    method_decorators = [handle_api_auth]

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    @doc(description=user_view.logout.__doc__)
    def get(organization_id: str, uid: str, token: str):
        """
            **signout user**
                will sign out the user through token invalidation
        :param organization_id: the organization id the user is registered on
        :param uid: the user id of the signed in user
        :param token: valid authentication token
        :return: tuple
        """
        return user_view.logout(organization_id=organization_id, uid=uid, token=token)

    @staticmethod
    @doc(description=user_view.login.__doc__)
    @marshal_with(schema=UserResponseSchema)
    def post(organization_id: str, email: str, password: str) -> tuple:
        """
            **user login**
                will login a user into his or her account
            :param organization_id: the organization_id of the organization the user is registered in
            :param email: the email attached to the account
            :param password: password for the account
            :return: tuple containing results
        """
        return user_view.login(organization_id=organization_id, email=email, password=password)


class UserListView(ViewModel):
    """
        **UserListView**
            allows admins to access a list of users
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    @doc(description=user_view.get_all_users.__doc__)
    @marshal_with(schema=UsersListResponseSchema)
    def get(organization_id: str, uid: str):
        """

        :param organization_id: organization_id of the admin
        :param uid:  user id of the admin users
        :return: tuple
        """
        return user_view.get_all_users(organization_id=organization_id)

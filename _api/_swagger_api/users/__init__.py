from flask_apispec import doc, marshal_with

from _api._swagger_api import ViewModel
from _api._swagger_api.schemas.users import UserResponseSchema
from security.api_authenticator import handle_api_auth
from views import user_view


class UserViewModel(ViewModel):
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    method_decorators = [handle_api_auth]

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    @doc(description=user_view.add_user.__doc__)
    @marshal_with(UserResponseSchema)
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
    @marshal_with(UserResponseSchema)
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


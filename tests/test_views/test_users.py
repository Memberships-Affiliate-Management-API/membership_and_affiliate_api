from random import choice, randint, choices
from string import ascii_lowercase
from string import digits as digits_characters
from typing import List, Optional, Generator

from google.cloud import ndb
from pytest import raises
# noinspection PyUnresolvedReferences
from pytest_mock import mocker

from config import config_instance
from config.exceptions import status_codes, UnAuthenticatedError, InputError
from config.use_context import get_client
from database.users import UserModel
from tests import test_app
from utils import create_id, timestamp, today, _char_set

with test_app().app_context():
    user_instance: UserModel = UserModel()
    from views import user_view


class UsersQueryMock:
    user_instance: UserModel = UserModel()
    results_range: int = randint(10, 1000)

    def __init__(self) -> None:
        self.user_instance.uid = create_id()
        self.user_instance.organization_id = config_instance.ORGANIZATION_ID
        self.user_instance.names = "john"
        self.user_instance.surname = "doe"
        self.user_instance.cell = "+27818858156"
        self.user_instance.email = "john.doe@example.com"
        self.user_instance.email_verified = True
        self.user_instance.password = "JohnDoe12345@"
        self.user_instance.last_login_date = today()

    @staticmethod
    def rand_user() -> UserModel:
        """
        **rand_user**
            returns a randomly generated user
        :return:
        """
        return UserModel(uid=create_id(), organization_id=config_instance.ORGANIZATION_ID,
                         names='john', surname='doe', cell=f'+278188{choices(population=digits_characters, k=5)}',
                         email=f'{choices(population=ascii_lowercase, k=12)}@example.com',
                         email_verified=choice([True, False]), password=f'{choices(population=_char_set, k=12)}',
                         is_active=choice([True, False]), time_registered=timestamp(), is_admin=choice([True, False]),
                         is_support=choice([True, False]), last_login_date=today())

    def fetch_generator(self) -> Generator:
        _results_range: int = randint(10, 1000)
        return (self.rand_user() for _ in range(_results_range))

    def fetch(self) -> List[UserModel]:
        """
        **fetch**
        returns a list of users
        :return:
        """
        return [_user for _user in self.fetch_generator()]

    def get(self) -> UserModel:
        return self.user_instance

    @ndb.tasklet
    def get_async(self) -> UserModel:
        return self.user_instance

    def user_mock_data(self) -> dict:
        """
        **user_mock_data**

        :return:
        """
        user_data: dict = self.user_instance.to_dict()
        # NOTE: user_instance.to_dict() returns user dict without password field for security reasons
        user_data.update(password="Complicated Password 12345%$#")
        return user_data


user_mock_data: dict = UsersQueryMock().user_mock_data()


def get_user_data() -> tuple:
    """
    **get_user_data**
        returns complete list of user data
    :return: tuple -> user data
    """

    organization_id: str = user_mock_data.get('organization_id')
    uid: str = user_mock_data.get('uid')
    names: str = user_mock_data.get('names')
    surname: str = user_mock_data.get('surname')
    cell: str = user_mock_data.get('cell')
    email: str = user_mock_data.get('email')
    password: str = user_mock_data.get('password')

    return cell, email, names, organization_id, password, surname, uid


def nullish_value() -> Optional[str]:
    """
    **nullish_value**
        returns None Null or Empty String
    :return: Nullish
    """
    return choice([None, " ", ""])


# noinspection PyUnusedLocal,PyShadowingNames
def test_create_user(mocker):
    """
    **test_create_user**
        testing user creation with view

    :param mocker:
    :return:
    """
    with get_client().context():
        mocker.patch('database.users.UserModel.put',
                     return_value=ndb.Key(UserModel, create_id()))
        mocker.patch('database.users.UserModel.query',
                     return_value=UsersQueryMock())

    with test_app().app_context():
        mocker.patch('views.users.UserView.is_organization_exist',
                     return_value=True)
        mocker.patch('views.users.UserView.is_email_available',
                     return_value=True)
        mocker.patch('views.users.UserView.is_cell_available',
                     return_value=True)

        cell, email, names, organization_id, password, surname, uid = get_user_data()
        response, status = user_view.add_user(organization_id=organization_id, uid=uid, names=names,
                                              surname=surname, cell=cell, email=email, password=password)
        assert status == status_codes.successfully_updated_code
        json_data: dict = response.get_json()
        assert isinstance(
            json_data, dict), 'response data not formatted correctly'
        assert isinstance(json_data.get('payload'),
                          dict), json_data.get('message')

    mocker.stopall()


# noinspection PyShadowingNames
def test_create_user_un_auth(mocker):
    """
    **test_create_user_un_auth**
        testing if create_user can throw UnAuthenticatedError
    :param mocker:
    :return:
    """
    with get_client().context():
        mocker.patch('database.users.UserModel.put',
                     return_value=ndb.Key(UserModel, create_id()))
        mocker.patch('database.users.UserModel.query',
                     return_value=UsersQueryMock())

    with test_app().app_context():
        mocker.patch('views.users.UserView.is_organization_exist',
                     return_value=False)
        mocker.patch('views.users.UserView.is_email_available',
                     return_value=False)
        mocker.patch('views.users.UserView.is_cell_available',
                     return_value=True)

        cell, email, names, organization_id, password, surname, uid = get_user_data()
        with raises(UnAuthenticatedError):
            user_view.add_user(organization_id=organization_id, uid=uid, names=names, surname=surname,
                               cell=cell, email=email, password=password)

    mocker.stopall()


# noinspection PyShadowingNames
def test_create_user_input_errors(mocker):
    """
    **test_create_user_input_errors**
        tests if create_user throws all required Input Errors

    :param mocker:
    :return:
    """
    with get_client().context():
        mocker.patch('database.users.UserModel.put',
                     return_value=ndb.Key(UserModel, create_id()))
        mocker.patch('database.users.UserModel.query',
                     return_value=UsersQueryMock())

    with test_app().app_context():
        mocker.patch('views.users.UserView.is_organization_exist',
                     return_value=True)
        mocker.patch('views.users.UserView.is_email_available',
                     return_value=True)
        mocker.patch('views.users.UserView.is_cell_available',
                     return_value=True)

        cell, email, names, organization_id, password, surname, uid = get_user_data()

        with raises(InputError):
            user_view.add_user(organization_id=nullish_value(), uid=uid, names=names, surname=surname,
                               cell=cell, email=email, password=password)
        with raises(InputError):
            user_view.add_user(organization_id=organization_id, uid=uid, names=nullish_value(),
                               surname=surname, cell=cell, email=email, password=password)
        with raises(InputError):
            user_view.add_user(organization_id=organization_id, uid=uid, names=names,
                               surname=nullish_value(), cell=cell, email=email, password=password)
        with raises(InputError):
            user_view.add_user(organization_id=organization_id, uid=uid, names=names,
                               surname=surname, cell=nullish_value(), email=email, password=password)
        with raises(InputError):
            user_view.add_user(organization_id=organization_id, uid=uid, names=names,
                               surname=surname, cell=cell, email=nullish_value(), password=password)
        with raises(InputError):
            user_view.add_user(organization_id=organization_id, uid=uid, names=names, surname=surname,
                               cell=cell, email=email, password=nullish_value())

    mocker.stopall()

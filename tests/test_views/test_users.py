from datetime import datetime
from google.cloud import ndb
from random import choice, randint, choices
from string import digits as digits_characters
from string import ascii_lowercase
from typing import List
from pytest import raises
from pytest_mock import mocker
from config import config_instance
from config.exceptions import status_codes, UnAuthenticatedError, InputError
from database.mixins import AmountMixin, AddressMixin
from utils.utils import create_id, timestamp, today, _char_set
from tests import int_positive, test_app
from database.users import UserModel
from werkzeug.security import check_password_hash

from views.users import UserView

user_instance: UserModel = UserModel()


class UsersQueryMock:
    user_instance: UserModel = UserModel()
    results_range: int = randint(0, 100)

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
        ***REMOVED***
        **rand_user**
            returns a randomly generated user
        :return:
        ***REMOVED***
        return UserModel(uid=create_id(), organization_id=config_instance.ORGANIZATION_ID,
                         names='john', surname='doe', cell=f'+278188{choices(population=digits_characters,k=5)}',
                         email=f'{choices(population=ascii_lowercase, k=12)}@example.com',
                         email_verified=choice([True, False]), password=f'{choices(population=_char_set,k=12)}',
                         is_active=choice([True, False]), time_registered=timestamp(), is_admin=choice([True, False]),
                         is_support=choice([True, False]), last_login_date=today())

    def fetch(self) -> List[UserModel]:
        ***REMOVED***
        **fetch**
        returns a list of users
        :return:
        ***REMOVED***
        return [self.rand_user() for _ in range(self.results_range)]

    def get(self) -> UserModel:
        return self.user_instance

    @ndb.tasklet
    def get_async(self) -> UserModel:
        return self.user_instance

    def user_mock_data(self) -> dict:
        return self.user_instance.to_dict()


user_mock_data: dict = UsersQueryMock().user_mock_data()



def get_user_data():
    users_view_instance: UserView = UserView()
    organization_id: str = user_mock_data.get('organization_id')
    names: str = user_mock_data.get('names')
    surname: str = user_mock_data.get('surname')
    cell: str = user_mock_data.get('cell')
    email: str = user_mock_data.get('email')
    password: str = user_mock_data.get('password')
    uid: str = user_mock_data.get('uid')
    return cell, email, names, organization_id, password, surname, uid, users_view_instance


# noinspection PyUnusedLocal,PyShadowingNames
def test_create_user(mocker):
    ***REMOVED***
    **test_create_user**
        testing user creation with view

    :param mocker:
    :return:
    ***REMOVED***
    mocker.patch('database.users.UserModel.put', return_value=ndb.KeyProperty('Users'))
    mocker.patch('database.users.UserModel.query', return_value=UsersQueryMock())

    mocker.patch('views.users.UserView.is_organization_exist', return_value=True)
    mocker.patch('views.users.UserView.is_email_available', return_value=True)
    mocker.patch('views.users.UserView.is_cell_available', return_value=True)

    with test_app().app_context():
        cell, email, names, organization_id, password, surname, uid, users_view_instance = get_user_data()
        response, status = users_view_instance.add_user(organization_id=organization_id, uid=uid, names=names,
                                                        surname=surname, cell=cell, email=email, password=password)
        assert status == status_codes.successfully_updated_code
        json_data: dict = response.get_json()
        assert isinstance(json_data, dict), 'response data not formatted correctly'
        assert isinstance(json_data.get('payload'), dict), json_data.get('message')

    mocker.stopall()


# noinspection PyShadowingNames
def test_create_user_un_auth(mocker):
    ***REMOVED***
    **test_create_user_un_auth**
        testing if create_user can throw UnAuthenticatedError
    :param mocker:
    :return:
    ***REMOVED***
    mocker.patch('database.users.UserModel.put', return_value=ndb.KeyProperty('Users'))
    mocker.patch('database.users.UserModel.query', return_value=UsersQueryMock())

    mocker.patch('views.users.UserView.is_organization_exist', return_value=False)
    mocker.patch('views.users.UserView.is_email_available', return_value=False)
    mocker.patch('views.users.UserView.is_cell_available', return_value=True)

    with test_app().app_context():
        cell, email, names, organization_id, password, surname, uid, users_view_instance = get_user_data()
        with raises(UnAuthenticatedError):
            users_view_instance.add_user(organization_id=organization_id, uid=uid, names=names, surname=surname,
                                         cell=cell, email=email, password=password)

    mocker.stopall()


# noinspection PyShadowingNames
def test_create_user_input_errors(mocker):
    ***REMOVED***
    **test_create_user_input_errors**
        tests if create_user throws all required Input Errors

    :param mocker:
    :return:
    ***REMOVED***
    mocker.patch('database.users.UserModel.put', return_value=ndb.KeyProperty('Users'))
    mocker.patch('database.users.UserModel.query', return_value=UsersQueryMock())

    mocker.patch('views.users.UserView.is_organization_exist', return_value=True)
    mocker.patch('views.users.UserView.is_email_available', return_value=True)
    mocker.patch('views.users.UserView.is_cell_available', return_value=True)

    with test_app().app_context():
        cell, email, names, organization_id, password, surname, uid, users_view_instance = get_user_data()

        with raises(InputError):
            users_view_instance.add_user(organization_id=choice([None, " ", ""]), uid=uid, names=names, surname=surname,
                                         cell=cell, email=email, password=password)
        with raises(InputError):
            users_view_instance.add_user(organization_id=organization_id, uid=uid, names=choice([None, " ", ""]),
                                         surname=surname, cell=cell, email=email, password=password)
    mocker.stopall()




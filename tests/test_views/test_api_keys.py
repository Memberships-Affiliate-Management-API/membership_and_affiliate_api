from random import choice, randint
from typing import List, Optional, Generator

from google.cloud import ndb
from pytest import raises
# noinspection PyUnresolvedReferences
from pytest_mock import mocker

from config import config_instance
from config.exceptions import status_codes, UnAuthenticatedError, InputError, DataServiceError
from config.use_context import get_client
from database.apikeys import APIKeys
from tests import test_app
from utils import create_id

with test_app().app_context():
    from views import api_keys_view


class APIKeysQueryMock:
    api_key_instance: APIKeys = APIKeys()

    def __init__(self):
        self.api_key_instance.organization_id = config_instance.ORGANIZATION_ID
        self.api_key_instance.api_key = create_id()
        self.api_key_instance.secret_token = create_id()
        self.api_key_instance.assigned_to_uid = config_instance.ADMIN_UID
        self.api_key_instance.domain = 'https://example.com'
        self.api_key_instance.is_active = True

    @staticmethod
    def rand_api_key() -> APIKeys:
        """
            **rand_api_key**
                generates random api keys
        :return: APIKeys
        """
        return APIKeys(
            organization_id=create_id(),
            api_key=create_id(),
            secret_token=create_id(),
            assigned_to_uid=create_id(),
            domain='https://example.com',
            is_active=choice([True, False]))

    def fetch_generator(self) -> Generator:
        _results_range: int = randint(10, 1000)
        return (self.rand_api_key() for _ in range(_results_range))

    def fetch(self) -> List[APIKeys]:
        return [api_key for api_key in self.fetch_generator()]

    def get(self) -> APIKeys:
        return self.api_key_instance


def nullish_value() -> Optional[str]:
    """
    **nullish_value**
        returns None Null or Empty String
    :return: Nullish
    """
    return choice([None, " ", ""])


# noinspection PyShadowingNames
def test_create_api_key(mocker) -> None:
    """
        **test_create_api_key**
            tests api key create method on APIKeysView
    :param mocker:
    :return:
    """
    api_key_mock_data: dict = APIKeysQueryMock().get().to_dict()
    with test_app().app_context():
        with get_client().context():
            mocker.patch('database.apikeys.APIKeys.put', return_value=ndb.Key(APIKeys, create_id()))
            mocker.patch('database.apikeys.APIKeys.query', return_value=APIKeysQueryMock())
            mocker.patch('database.setters.PropertySetters.set_domain', return_value="https://example.com")
            mocker.patch('views.apikeys.APIKeysView.organization_exist', return_value=True)
            mocker.patch('views.apikeys.APIKeysView.user_can_create_key', return_value=True)
            mocker.patch('views.apikeys.APIKeysView._create_unique_api_key', return_value=create_id())
            mocker.patch('views.apikeys.APIKeysView._create_unique_secret_key', return_value=create_id())

        response, status = api_keys_view.create_keys(domain=api_key_mock_data.get('domain'),
                                                     uid=api_key_mock_data.get('uid'),
                                                     organization_id=api_key_mock_data.get('organization_id'))

        assert status == status_codes.successfully_updated_code, 'bad status code'
        response_data: dict = response.get_json()
        assert response_data.get('status') is True, response_data['message']

    mocker.stopall()


# noinspection PyShadowingNames
def test_create_api_key_raises(mocker) -> None:
    """

    :param mocker:
    :return:
    """
    api_key_mock_data: dict = APIKeysQueryMock().get().to_dict()
    with test_app().app_context():
        mocker.patch('database.apikeys.APIKeys.put', return_value=None)
        mocker.patch('database.apikeys.APIKeys.query', return_value=APIKeysQueryMock())
        mocker.patch('database.setters.PropertySetters.set_domain', return_value="https://example.com")
        mocker.patch('views.apikeys.APIKeysView.organization_exist', return_value=True)
        mocker.patch('views.apikeys.APIKeysView.user_can_create_key', return_value=True)
        mocker.patch('views.apikeys.APIKeysView._create_unique_api_key', return_value=create_id())
        mocker.patch('views.apikeys.APIKeysView._create_unique_secret_key', return_value=create_id())

        with raises(DataServiceError):
            api_keys_view.create_keys(domain=api_key_mock_data.get('domain'),
                                      uid=api_key_mock_data.get('uid'),
                                      organization_id=api_key_mock_data.get('organization_id'))

        with get_client().context():
            mocker.patch('database.apikeys.APIKeys.put', return_value=ndb.Key(APIKeys, create_id()))
            mocker.patch('views.apikeys.APIKeysView.organization_exist', return_value=False)

        with raises(UnAuthenticatedError):
            api_keys_view.create_keys(domain=api_key_mock_data.get('domain'),
                                      uid=api_key_mock_data.get('uid'),
                                      organization_id=api_key_mock_data.get('organization_id'))
        with get_client().context():
            mocker.patch('database.apikeys.APIKeys.put', return_value=ndb.Key(APIKeys, create_id()))
            mocker.patch('views.apikeys.APIKeysView.organization_exist', return_value=True)
            mocker.patch('views.apikeys.APIKeysView.user_can_create_key', return_value=False)

        with raises(UnAuthenticatedError):
            api_keys_view.create_keys(domain=api_key_mock_data.get('domain'),
                                      uid=api_key_mock_data.get('uid'),
                                      organization_id=api_key_mock_data.get('organization_id'))

    mocker.stopall()


def test_api_keys_validators() -> None:
    """
    **test_api_keys_validators**
        testing api keys validators
    :return:
    """
    with test_app().app_context():
        with get_client().context():
            with raises(InputError):
                api_keys_view.organization_exist(organization_id="")

            with raises(DataServiceError):
                api_keys_view.organization_exist(organization_id=config_instance.ORGANIZATION_ID)

            with raises(InputError):
                api_keys_view.user_can_create_key(uid="", organization_id=config_instance.ORGANIZATION_ID)
            with raises(InputError):
                api_keys_view.user_can_create_key(uid=config_instance.ADMIN_UID,
                                                  organization_id="")


# noinspection PyShadowingNames
def test_deactivate_key(mocker) -> None:
    """

    :param mocker:
    :return:
    """
    api_key_mock_data: dict = APIKeysQueryMock().get().to_dict()
    with test_app().app_context():
        with get_client().context():
            mocker.patch('database.apikeys.APIKeys.put', return_value=ndb.Key(APIKeys, create_id()))
            mocker.patch('database.apikeys.APIKeys.query', return_value=APIKeysQueryMock())

        response, status = api_keys_view.deactivate_key(key=api_key_mock_data.get('api_key'))
        assert status == status_codes.successfully_updated_code, 'code not set correctly'
        response_data: dict = response.get_json()
        assert response_data.get('status') is True, response_data['message']
        assert isinstance(response_data.get('payload'), dict), 'response payload not being set'

    mocker.stopall()


# noinspection PyShadowingNames
def test_deactivate_raises() -> None:
    """

    :return:
    """
    with test_app().app_context():
        with raises(InputError):
            api_keys_view.deactivate_key(key=None)


# noinspection PyShadowingNames
def test_activate_key(mocker) -> None:
    """
        **test_activate_key**
            test activate key no

    :param mocker:
    :return:
    """
    api_key_mock_data: dict = APIKeysQueryMock().get().to_dict()
    with test_app().app_context():
        with get_client().context():
            mocker.patch('database.apikeys.APIKeys.put', return_value=ndb.Key(APIKeys, create_id()))
            mocker.patch('database.apikeys.APIKeys.query', return_value=APIKeysQueryMock())

        response, status = api_keys_view.activate_key(key=api_key_mock_data.get('api_key'),
                                                      organization_id=api_key_mock_data.get('organization_id'))

        assert status == status_codes.successfully_updated_code, 'code not set correctly'
        response_data: dict = response.get_json()
        assert response_data.get('status') is True, response_data['message']
        assert isinstance(response_data.get('payload'), dict), 'response payload not being set'

    mocker.stopall()


# noinspection PyShadowingNames
def test_raises_activate_key(mocker) -> None:
    """
    **test_raises_activate_key**
        test exceptions activation keys

    :param mocker:
    :return:
    """
    api_key_mock_data: dict = APIKeysQueryMock().get().to_dict()
    with test_app().app_context():
        with get_client().context():
            mocker.patch('database.apikeys.APIKeys.put', return_value=ndb.Key(APIKeys, create_id()))
            mocker.patch('database.apikeys.APIKeys.query', return_value=APIKeysQueryMock())

        with raises(InputError):
            api_keys_view.activate_key(key="",
                                       organization_id=api_key_mock_data.get('organization_id'))

        with raises(InputError):
            api_keys_view.activate_key(key=api_key_mock_data.get('api_key'),
                                       organization_id="")

        with get_client().context():
            mocker.patch('database.apikeys.APIKeys.put', return_value=None)
            mocker.patch('database.apikeys.APIKeys.query', return_value=APIKeysQueryMock())

        with raises(DataServiceError):
            response, status = api_keys_view.activate_key(key=api_key_mock_data.get('api_key'),
                                                          organization_id=api_key_mock_data.get('organization_id'))
    mocker.stopall()


# noinspection PyShadowingNames
def test_return_all_organization_keys(mocker) -> None:
    """

    :param mocker:
    :return:
    """
    api_key_mock_data: dict = APIKeysQueryMock().get().to_dict()
    with test_app().app_context():
        with get_client().context():
            mocker.patch('database.apikeys.APIKeys.put', return_value=ndb.Key(APIKeys, create_id()))
            mocker.patch('database.apikeys.APIKeys.query', return_value=APIKeysQueryMock())

        organization_id: str = api_key_mock_data.get('organization_id')
        response, status = api_keys_view.return_all_organization_keys(organization_id=organization_id)
        assert status == status_codes.status_ok_code, 'code not set correctly'
        response_data: dict = response.get_json()
        assert response_data.get('status') is True, response_data['message']
        assert isinstance(response_data.get('payload'), list), 'response payload not being set correctly'
    mocker.stopall()


def test_raises_return_all_organization_keys() -> None:
    """
    :return: None
    """
    with test_app().app_context():
        with raises(InputError):
            api_keys_view.return_all_organization_keys(organization_id="")

        with raises(InputError):
            api_keys_view.return_all_organization_keys(organization_id=None)


# noinspection PyShadowingNames
def test_return_active_organization_keys(mocker) -> None:
    """

    :param mocker:
    :return:
    """
    api_key_mock_data: dict = APIKeysQueryMock().get().to_dict()
    with test_app().app_context():
        with get_client().context():
            mocker.patch('database.apikeys.APIKeys.put', return_value=ndb.Key(APIKeys, create_id()))
            mocker.patch('database.apikeys.APIKeys.query', return_value=APIKeysQueryMock())

        organization_id: str = api_key_mock_data.get('organization_id')
        response, status = api_keys_view.return_active_organization_keys(organization_id=organization_id)
        assert status == status_codes.status_ok_code, 'code not set correctly'
        response_data: dict = response.get_json()
        assert response_data.get('status') is True, response_data['message']
        assert isinstance(response_data.get('payload'), list), 'response payload not being set correctly'
    mocker.stopall()


def test_raises_return_active_organization_keys() -> None:
    """
        **test_raises_return_active_organization_keys**
    :return: None
    """
    with test_app().app_context():
        with raises(InputError):
            api_keys_view.return_active_organization_keys(organization_id="")

        with raises(InputError):
            api_keys_view.return_active_organization_keys(organization_id=None)


# noinspection PyShadowingNames
def test_get_api_key(mocker) -> None:
    """

    :param mocker:
    :return:
    """
    api_key_mock_data: dict = APIKeysQueryMock().get().to_dict()
    with test_app().app_context():
        with get_client().context():
            mocker.patch('database.apikeys.APIKeys.put', return_value=ndb.Key(APIKeys, create_id()))
            mocker.patch('database.apikeys.APIKeys.query', return_value=APIKeysQueryMock())

        organization_id: str = api_key_mock_data.get('organization_id')
        api_key: str = api_key_mock_data.get('api_key')
        response, status = api_keys_view.get_api_key(api_key=api_key, organization_id=organization_id)
        assert status == status_codes.status_ok_code, 'code not set correctly'
        response_data: dict = response.get_json()
        assert response_data.get('status') is True, response_data['message']
        assert isinstance(response_data.get('payload'), dict), 'response payload not being set correctly'
    mocker.stopall()

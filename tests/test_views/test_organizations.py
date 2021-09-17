from random import choice, randint, choices
from string import ascii_lowercase
from string import digits as digits_characters
from typing import List, Optional

import pytest
from google.cloud import ndb
from pytest import raises
# noinspection PyUnresolvedReferences
from pytest_mock import mocker

from config import config_instance
from config.exceptions import status_codes, UnAuthenticatedError, InputError

from database.organization import Organization
from tests import test_app, is_internet_on, random_int_positive, get_test_domain
from utils import create_id, timestamp, today, _char_set

with test_app().app_context():
    from views import organization_view


class OrganizationQueryMock:
    organization_instance: Organization = Organization()
    results_range: int = randint(10, 1000)

    def __init__(self):
        self.organization_instance.organization_id = create_id()
        self.organization_instance.organization_name = "Memberships & Affiliates API"
        self.organization_instance.description = "main organization for Memberships & Affiliates API"
        self.organization_instance.wallet_id = create_id()
        self.organization_instance.owner_uid = create_id()
        self.organization_instance.total_affiliates = random_int_positive()
        self.organization_instance.total_members = random_int_positive()
        self.organization_instance.total_users = random_int_positive()
        self.organization_instance.home_url = get_test_domain()
        self.organization_instance.login_callback_url = f'{get_test_domain()}login'
        self.organization_instance.recovery_callback_url = f'{get_test_domain()}recovery'

    @staticmethod
    def rand_organization() -> Organization:
        """
        **generate a random organization**
             for testing purposes
        :return: Organization
        """
        return Organization(
            organization_id=create_id(),
            organization_name="Memberships & Affiliates API",
            description="main organization for Memberships & Affiliates API",
            wallet_id=create_id(),
            owner_uid=create_id(),
            total_affiliates=random_int_positive(),
            total_members=random_int_positive(),
            total_users=random_int_positive(),
            home_url='https://memberships-affiliates-api.heroku.com',
            login_callback_url='https://memberships-affiliates-api.heroku.com/login',
            recovery_callback_url='https://memberships-affiliates-api.heroku.com/recovery'
        )

    def fetch(self) -> List[Organization]:
        """
            :param self:
            :return:
        """
        return [self.rand_organization() for _ in range(self.results_range)]

    def get(self) -> Organization:
        return self.organization_instance


def nullish_value() -> Optional[str]:
    """
    **nullish_value**
        returns None Null or Empty String
    :return: Nullish
    """
    return choice([None, " ", ""])


# noinspection PyShadowingNames
@pytest.mark.skip(reason="i need to implement better regex for domain handling")
def test_create_organization(mocker) -> None:
    """
    **test_create_organization**
         tests for the validity of view module create_organization method

        def create_organization(self,
                                uid: Optional[str],
                                organization_name: Optional[str],
                                description: Optional[str],
                                currency: Optional[str],
                                paypal_address: Optional[str],
                                home_url: Optional[str],
                                login_callback_url: Optional[str],
                                recovery_callback_url: Optional[str]) -> tuple

    :param mocker:
    :return:
    """
    organization_mock_data: dict = OrganizationQueryMock().get().to_dict()
    with test_app().app_context():
        mocker.patch('database.organization.Organization.put', return_value=ndb.KeyProperty('Organization'))
        mocker.patch('database.organization.Organization.query', return_value=OrganizationQueryMock())

        uid: str = organization_mock_data.get('uid')
        organization_name: str = organization_mock_data.get('organization_name')
        description: str = organization_mock_data.get('description')
        currency: str = organization_mock_data.get('currency')
        paypal_address: str = organization_mock_data.get('paypal_address')
        home_url: str = organization_mock_data.get('home_url')
        login_callback_url: str = organization_mock_data.get('login_callback_url')
        recovery_callback_url: str = organization_mock_data.get('recovery_callback_url')

        response, status = organization_view.create_organization(uid=uid, organization_name=organization_name,
                                                                 description=description, currency=currency,
                                                                 paypal_address=paypal_address, home_url=home_url,
                                                                 login_callback_url=login_callback_url,
                                                                 recovery_callback_url=recovery_callback_url)

        assert status == status_codes.successfully_updated_code, 'bad status code'
        response_data: dict = response.get_json()
        assert response_data['status'] is True, response_data['message']

    mocker.stopall()

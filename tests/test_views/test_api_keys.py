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
    from views.apikeys import APIKeysValidators
    from views.apikeys import APIKeys


class APIKeysQueryMock:
    api_key_instance: APIKeys = APIKeys()
    results_range: int = randint(10, 1000)

    def __init__(self):
        self.api_key_instance.organization_id = config_instance.ORGANIZATION_ID
        self.api_key_instance.api_key = create_id()
        self.api_key_instance.secret_token = create_id()
        self.api_key_instance.assigned_to_uid = config_instance.ADMIN_UID
        self.api_key_instance.domain = config_instance.ADMIN_APP_BASEURL
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




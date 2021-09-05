from random import choice, randint, choices
from string import ascii_lowercase
from string import digits as digits_characters
from typing import List, Optional

from google.cloud import ndb
from pytest import raises
# noinspection PyUnresolvedReferences
from pytest_mock import mocker

from config import config_instance
from config.exceptions import status_codes, UnAuthenticatedError, InputError

from database.organization import Organization
from tests import test_app
from utils import create_id, timestamp, today, _char_set

with test_app().app_context():
    from views import organization_view


class OrganizationQueryMock:
    organization_instance: Organization = Organization()

    def __init__(self):
        self.organization_instance.organization_id = create_id()
        self.organization_instance.organization_name = "Memberships & Affiliates API"
        self.organization_instance.description = "main organization for Memberships & Affiliates API"
        self.organization_instance.wallet_id = create_id()
        self.organization_instance.owner_uid = create_id()
        self.organization_instance.total_affiliates = randint(10, 1000)
        self.organization_instance.total_members = randint(10, 1000)
        self.organization_instance.total_users = self.organization_instance.total_members + randint(10, 1000)
        self.organization_instance.home_url = 'https://memberships-affiliates-api.heroku.com'
        self.organization_instance.login_callback_url = 'https://memberships-affiliates-api.heroku.com/login'
        self.organization_instance.recovery_callback_url = 'https://memberships-affiliates-api.heroku.com/recovery'

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


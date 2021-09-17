"""
    **Test cases for helpdesk endpoints**

"""
from pytest import raises
# noinspection PyUnresolvedReferences
from pytest_mock import mocker
from datetime import datetime
from random import randint, choice
from typing import List
from google.cloud import ndb
from config.exceptions import status_codes, InputError, UnAuthenticatedError, DataServiceError
from config.use_context import get_client
from database.affiliates import Affiliates
from tests import test_app
from utils import create_id
from config import config_instance

with test_app().app_context():
    from views import helpdesk_view, ticket_view



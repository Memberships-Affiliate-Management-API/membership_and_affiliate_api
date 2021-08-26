***REMOVED***
    **Test cases for public affiliate endpoints**

***REMOVED***

from pytest import raises
from pytest_mock import mocker
from datetime import datetime
from random import randint
from typing import List, Optional
from google.cloud import ndb
from config.exceptions import status_codes
from database.affiliates import Affiliates
from views.affiliates import AffiliatesView
from tests import test_app
from utils import create_id
from config import config_instance

affiliate_data_mock: dict = {
    "uid": create_id(),
    "organization_id": config_instance.ORGANIZATION_ID,
    "affiliate_id": create_id(),
    "last_updated": datetime.now(),
    "total_recruits": 0,
    "is_active": True,
    "is_deleted": False
}


class AffiliateQueryMock:
    affiliate_instance: Affiliates = Affiliates()
    results_range: int = randint(0, 100)

    def __init__(self):
        pass

    def fetch(self) -> List[Affiliates]:
        return [self.affiliate_instance for _ in range(self.results_range)]

    def get(self) -> Affiliates:
        return self.affiliate_instance

    @ndb.tasklet
    def get_async(self) -> Affiliates:
        return self.affiliate_instance


# noinspection PyShadowingNames
def test_register_affiliate(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=ndb.KeyProperty('Affiliates'))
    mocker.patch('google.cloud.ndb.Model.query', return_value=AffiliateQueryMock())

    with test_app().app_context():
        affiliates_view_instance = AffiliatesView()
        response, status = affiliates_view_instance.register_affiliate(affiliate_data=affiliate_data_mock)
        response_dict: dict = response.get_json()
        assert status == status_codes.successfully_updated_code, response_dict['message']
        assert response_dict['status'], "response status not set correctly"
        assert response_dict.get('payload') is not None, "affiliates payload is not being set correctly"
        assert response_dict.get('message') is not None, "affiliate message is not being set correctly"

    mocker.stopall()



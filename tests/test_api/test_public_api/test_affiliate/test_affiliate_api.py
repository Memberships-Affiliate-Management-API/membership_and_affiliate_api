***REMOVED***
    **Test cases for public affiliate endpoints**

***REMOVED***
from pytest import raises
# noinspection PyUnresolvedReferences
from pytest_mock import mocker
from datetime import datetime
from random import randint, choice
from typing import List
from google.cloud import ndb
from config.exceptions import status_codes, InputError, UnAuthenticatedError, DataServiceError
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
        self.affiliate_instance.affiliate_id = affiliate_data_mock.get('affiliate_id')
        self.affiliate_instance.organization_id = affiliate_data_mock.get('organization_id')
        self.affiliate_instance.uid = affiliate_data_mock.get('uid')
        self.affiliate_instance.last_updated = affiliate_data_mock.get('last_updated')
        self.affiliate_instance.datetime_recruited = datetime.now()
        self.affiliate_instance.total_recruits = 0
        self.affiliate_instance.is_active = True
        self.affiliate_instance.is_deleted = False

    @staticmethod
    def rand_affiliate() -> Affiliates:
        ***REMOVED***
        **rand_affiliate**
            returns a randomly generated affiliate for test cases
        :return: Affiliate Instance
        ***REMOVED***
        return Affiliates(affiliate_id=create_id(), organization_id=config_instance.ORGANIZATION_ID, uid=create_id(),
                          last_updated=datetime.now(), datetime_recruited=datetime.now(),
                          total_recruits=randint(10, 1000), is_active=bool(randint(0, 1)),
                          is_deleted=bool(randint(0, 1)))

    def fetch(self) -> List[Affiliates]:
        return [self.rand_affiliate() for _ in range(self.results_range)]

    def get(self) -> Affiliates:
        return self.affiliate_instance

    @ndb.tasklet
    def get_async(self) -> Affiliates:
        return self.affiliate_instance


# noinspection PyShadowingNames
def test_register_affiliate(mocker):
    mocker.patch('database.affiliates.Affiliates.put', return_value=ndb.KeyProperty('Affiliates'))
    mocker.patch('database.affiliates.Affiliates.query', return_value=AffiliateQueryMock())
    mocker.patch('database.affiliates.AffiliatesValidators.recruiter_registered', return_value=False)
    data_mock: dict = affiliate_data_mock.copy()

    with test_app().app_context():
        affiliates_view_instance = AffiliatesView()
        response, status = affiliates_view_instance.register_affiliate(affiliate_data=data_mock)
        response_dict: dict = response.get_json()
        assert status == status_codes.successfully_updated_code, response_dict['message']
        assert response_dict.get('status'), "response status not set correctly"
        assert response_dict.get('payload') is not None, "affiliates payload is not being set correctly"
        assert response_dict.get('message') is not None, "affiliate message is not being set correctly"

    mocker.stopall()


# noinspection PyShadowingNames
def test_affiliate_raises_data_service_error(mocker):
    mocker.patch('database.affiliates.Affiliates.put', return_value=None)
    data_mock: dict = affiliate_data_mock.copy()
    with test_app().app_context():
        with raises(DataServiceError):
            affiliates_view_instance = AffiliatesView()
            affiliates_view_instance.register_affiliate(affiliate_data=data_mock)

    mocker.stopall()


# noinspection PyShadowingNames
def test_un_auth_error(mocker):
    mocker.patch('database.affiliates.Affiliates.put', return_value=ndb.KeyProperty('Affiliates'))
    mocker.patch('database.affiliates.Affiliates.query', return_value=AffiliateQueryMock())
    mocker.patch('database.affiliates.AffiliatesValidators.recruiter_registered', return_value=True)
    data_mock: dict = affiliate_data_mock.copy()
    with test_app().app_context():
        # Raises Error
        with raises(UnAuthenticatedError):
            affiliates_view_instance = AffiliatesView()
            affiliates_view_instance.register_affiliate(affiliate_data=data_mock)
        # Does not raise an error
        mocker.patch('database.affiliates.AffiliatesValidators.recruiter_registered', return_value=False)
        affiliates_view_instance = AffiliatesView()
        affiliates_view_instance.register_affiliate(affiliate_data=data_mock)

    mocker.stopall()


# noinspection PyShadowingNames
def test_affiliate_input_error(mocker):
    with test_app().app_context():
        affiliates_view_instance = AffiliatesView()
        data_mock: dict = affiliate_data_mock.copy()

        with raises(InputError):
            data_mock.update(uid=choice([None, '', ' ']))
            affiliates_view_instance.register_affiliate(affiliate_data=data_mock)
        data_mock: dict = affiliate_data_mock.copy()
        with raises(InputError):
            data_mock.update(organization_id=choice([None, '', ' ']))
            affiliates_view_instance.register_affiliate(affiliate_data=data_mock)
        # NOTE: restoring data to its original form

    mocker.stopall()


# noinspection PyShadowingNames
def test_increment_decrement_total_recruits(mocker):
    mocker.patch('database.affiliates.Affiliates.put', return_value=ndb.KeyProperty('Affiliates'))
    mocker.patch('database.affiliates.Affiliates.query', return_value=AffiliateQueryMock())

    with test_app().app_context():
        affiliates_view_instance = AffiliatesView()
        data_mock: dict = affiliate_data_mock.copy()
        response, status = affiliates_view_instance.total_recruits(affiliate_data=data_mock, add=1)
        affiliate_dict: dict = response.get_json()

        assert affiliate_dict['payload']['total_recruits'] == 1, 'failed to increment number of affiliates'
        assert affiliate_dict['status'], "failing to set the return boolean status"
        assert affiliate_dict.get('message') is not None, "failed to set message"
    mocker.stopall()


# noinspection PyShadowingNames
def test_delete_affiliate(mocker):
    mocker.patch('database.affiliates.Affiliates.put', return_value=ndb.KeyProperty('Affiliates'))
    mocker.patch('database.affiliates.Affiliates.query', return_value=AffiliateQueryMock())

    with test_app().app_context():
        affiliates_view_instance = AffiliatesView()
        data_mock: dict = affiliate_data_mock.copy()
        response, status = affiliates_view_instance.delete_affiliate(affiliate_data=data_mock)
        assert status == status_codes.successfully_updated_code, "unable to delete affiliate"
        affiliate_dict: dict = response.get_json()
        assert affiliate_dict.get('payload') is not None, "could not access delete affiliate payload"
        assert affiliate_dict.get('message') is not None, "delete_affiliate response message must be set"
        message: str = "affiliate delete operation response status was not set correctly"
        assert isinstance(affiliate_dict['status'], bool) and affiliate_dict['status'], message
    mocker.stopall()


# noinspection PyShadowingNames
def test_delete_affiliate_data_service_error(mocker):
    mocker.patch('database.affiliates.Affiliates.put', return_value=None)
    mocker.patch('database.affiliates.Affiliates.query', return_value=AffiliateQueryMock())

    with test_app().app_context():
        affiliates_view_instance = AffiliatesView()
        with raises(DataServiceError):
            affiliates_view_instance.delete_affiliate(affiliate_data=affiliate_data_mock)
    mocker.stopall()


# noinspection PyShadowingNames
def test_delete_affiliate_auth_error(mocker):
    mocker.patch('database.affiliates.Affiliates.put', return_value=ndb.KeyProperty('Affiliates'))
    mocker.patch('database.affiliates.Affiliates.query', return_value=AffiliateQueryMock())

    with test_app().app_context():
        affiliates_view_instance = AffiliatesView()

        data_mock: dict = affiliate_data_mock.copy()
        data_mock.update(affiliate_id=choice([None, '', ' ']))
        with raises(InputError):
            affiliates_view_instance.delete_affiliate(affiliate_data=data_mock)
        data_mock_2: dict = affiliate_data_mock.copy()
        data_mock_2.update(organization_id=choice([None, '', ' ']))
        with raises(InputError):
            affiliates_view_instance.delete_affiliate(affiliate_data=data_mock_2)

    mocker.stopall()


# noinspection PyShadowingNames
def test_mark_active(mocker):
    mocker.patch('database.affiliates.Affiliates.put', return_value=ndb.KeyProperty('Affiliates'))
    mocker.patch('database.affiliates.Affiliates.query', return_value=AffiliateQueryMock())

    with test_app().app_context():
        affiliates_view_instance = AffiliatesView()
        data_mock: dict = affiliate_data_mock.copy()
        response, status = affiliates_view_instance.mark_active(affiliate_data=data_mock, is_active=False)
        assert status == status_codes.successfully_updated_code, "Unable to mark affiliate as in-active"
        response, status = affiliates_view_instance.mark_active(affiliate_data=data_mock, is_active=True)
        assert status == status_codes.successfully_updated_code, "Unable to mark affiliate as active"

        with raises(InputError):
            # noinspection PyTypeChecker
            affiliates_view_instance.mark_active(affiliate_data=affiliate_data_mock, is_active="True")

        with raises(InputError):
            data_mock: dict = affiliate_data_mock.copy()
            data_mock.update(affiliate_id=choice([None, '', ' ']))
            # noinspection PyTypeChecker
            affiliates_view_instance.mark_active(affiliate_data=data_mock, is_active=True)
    mocker.stopall()


# noinspection PyShadowingNames
def test_get_affiliate(mocker):
    mocker.patch('database.affiliates.Affiliates.put', return_value=ndb.KeyProperty('Affiliates'))
    mocker.patch('database.affiliates.Affiliates.query', return_value=AffiliateQueryMock())

    with test_app().app_context():
        affiliates_view_instance = AffiliatesView()
        data_mock: dict = affiliate_data_mock.copy()
        print(data_mock)
        response, status = affiliates_view_instance.get_affiliate(affiliate_data=data_mock)
        assert status == status_codes.status_ok_code, 'unable to locate affiliate'
        response_data: dict = response.get_json()
        assert isinstance(response_data['payload'], dict), 'payload is required'
        assert response_data['status'] == True, "response is false"
        assert isinstance(response_data['message'], str), "payload message is not set"
    mocker.stopall()


# noinspection PyShadowingNames,DuplicatedCode
def test_get_all_affiliate(mocker):
    mocker.patch('database.affiliates.Affiliates.put', return_value=ndb.KeyProperty('Affiliates'))
    mocker.patch('database.affiliates.Affiliates.query', return_value=AffiliateQueryMock())
    # TODo complete the test cases
    with test_app().app_context():
        affiliate_instance: AffiliatesView = AffiliatesView()
        response, status = affiliate_instance.get_all_affiliates(organization_id=config_instance.ORGANIZATION_ID)
        assert status == status_codes.status_ok_code, "get_all_affiliates unable to fetch affiliates"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, "get_all_affiliates payload is not set properly"
        assert response_data.get('message') is not None, "get_all_affiliates message is not set properly"

    mocker.stopall()


# noinspection PyShadowingNames,DuplicatedCode
def test_active_affiliates(mocker):
    mocker.patch('database.affiliates.Affiliates.put', return_value=ndb.KeyProperty('Affiliates'))
    mocker.patch('database.affiliates.Affiliates.query', return_value=AffiliateQueryMock())
    with test_app().app_context():
        affiliate_instance: AffiliatesView = AffiliatesView()
        response, status = affiliate_instance.get_active_affiliates(organization_id=config_instance.ORGANIZATION_ID)
        assert status == status_codes.status_ok_code, "get_active_affiliates unable to fetch affiliates"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, "get_active_affiliates payload is not set properly"
        assert response_data.get('message') is not None, "get_active_affiliates message is not set properly"

    mocker.stopall()


# noinspection PyShadowingNames,DuplicatedCode
def test_inactive_affiliates(mocker):
    mocker.patch('database.affiliates.Affiliates.put', return_value=ndb.KeyProperty('Affiliates'))
    mocker.patch('database.affiliates.Affiliates.query', return_value=AffiliateQueryMock())

    with test_app().app_context():
        affiliate_instance: AffiliatesView = AffiliatesView()
        response, status = affiliate_instance.get_in_active_affiliates(organization_id=config_instance.ORGANIZATION_ID)
        assert status == status_codes.status_ok_code, "get_inactive_affiliates unable to fetch affiliates"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, "get_inactive_affiliates payload is not set properly"
        assert response_data.get('message') is not None, "get_inactive_affiliates message is not set properly"
    mocker.stopall()


# noinspection PyShadowingNames,DuplicatedCode
def test_deleted_affiliates(mocker):
    mocker.patch('database.affiliates.Affiliates.put', return_value=ndb.KeyProperty('Affiliates'))
    mocker.patch('database.affiliates.Affiliates.query', return_value=AffiliateQueryMock())

    with test_app().app_context():
        affiliate_instance: AffiliatesView = AffiliatesView()
        response, status = affiliate_instance.get_deleted_affiliates(organization_id=config_instance.ORGANIZATION_ID)
        assert status == status_codes.status_ok_code, "get_deleted_affiliates unable to fetch affiliates"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, "get_deleted_affiliates payload is not set properly"
        assert response_data.get('message') is not None, "get_deleted_affiliates message is not set properly"
    mocker.stopall()


# noinspection PyShadowingNames,DuplicatedCode
def test_undeleted_affiliates(mocker):
    mocker.patch('database.affiliates.Affiliates.put', return_value=ndb.KeyProperty('Affiliates'))
    mocker.patch('database.affiliates.Affiliates.query', return_value=AffiliateQueryMock())

    with test_app().app_context():
        affiliate_instance: AffiliatesView = AffiliatesView()
        response, status = affiliate_instance.get_not_deleted_affiliates(
            organization_id=config_instance.ORGANIZATION_ID)
        assert status == status_codes.status_ok_code, "get_not_deleted_affiliates unable to fetch affiliates"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, "get_not_deleted_affiliates payload is not set properly"
        assert response_data.get('message') is not None, "get_not_deleted_affiliates message is not set properly"
    mocker.stopall()

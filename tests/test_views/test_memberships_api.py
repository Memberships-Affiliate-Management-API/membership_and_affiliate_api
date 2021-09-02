import random
from typing import Optional, List
from datetime import datetime, timedelta, date
from random import randint
from google.cloud import ndb
from config import config_instance
from config.currencies import currency_util
from config.exceptions import DataServiceError, status_codes, UnAuthenticatedError, InputError
from database.mixins import AmountMixin
from views import memberships_view
from database.memberships import Memberships, MembershipPlans
from utils import create_id, today, datetime_now
from tests import test_app
from pytest import raises
# noinspection PyUnresolvedReferences
from pytest_mock import mocker


class MembershipsQueryMock:
    membership_instance: Memberships = Memberships()
    results_range: int = randint(0, 100)

    def __init__(self) -> None:
        self.membership_instance.plan_id = create_id()
        self.membership_instance.organization_id = config_instance.ORGANIZATION_ID
        self.membership_instance.uid = create_id()
        self.membership_instance.plan_id = create_id()
        self.membership_instance.payment_status = "paid"
        self.membership_instance.date_created = datetime.now()
        self.membership_instance.plan_start_date = datetime.now().date()
        self.membership_instance.payment_method = 'paypal'

    @staticmethod
    def rand_membership() -> Memberships:
        ***REMOVED***
        **rand_membership**
            create a random membership for testing purposes
        :return: Membership Instance
        ***REMOVED***
        return Memberships(organization_id=config_instance.ORGANIZATION_ID, uid=create_id(), plan_id=create_id(),
                           payment_status=random.choice(['paid', 'unpaid']), date_created=datetime_now(),
                           plan_start_date=today(), payment_method='paypal',
                           is_active_subscription=random.choice([True, False]))

    def fetch(self) -> List[Memberships]:
        return [self.rand_membership() for _ in range(self.results_range)]

    def get(self) -> Memberships:
        return self.membership_instance

    @ndb.tasklet
    def get_async(self) -> Memberships:
        return self.membership_instance


class MembershipPlansQueryMock:
    membership_plan_instance: MembershipPlans = MembershipPlans()
    results_range: int = randint(0, 100)

    def __init__(self):
        self.membership_plan_instance.service_id = create_id()
        self.membership_plan_instance.organization_id = create_id()
        self.membership_plan_instance.plan_id = create_id()
        self.membership_plan_instance.date_created = datetime.now()
        self.membership_plan_instance.plan_name = "bronze"
        self.membership_plan_instance.description = "bronze plan"
        self.membership_plan_instance.total_members = 10
        self.membership_plan_instance.schedule_day = 1
        self.membership_plan_instance.schedule_term = "monthly"
        self.membership_plan_instance.term_payment_amount = AmountMixin(
            amount_cents=10000, currency=random.choice(currency_util.currency_symbols()))
        self.membership_plan_instance.registration_amount = AmountMixin(
            amount_cents=10000, currency=random.choice(currency_util.currency_symbols()))

    def fetch(self) -> List[MembershipPlans]:
        return [self.membership_plan_instance for _ in range(self.results_range)]

    def get(self) -> MembershipPlans:
        return self.membership_plan_instance


membership_mock_data: dict = {
    "uid": create_id(),
    "organization_id": config_instance.ORGANIZATION_ID,
    "plan_id": create_id(),
    "payment_status": "unpaid",
    "date_created": datetime.now(),
    "plan_start_date": datetime.date(datetime.now() + timedelta(days=5))
}


# noinspection PyShadowingNames
def test_create_membership(mocker) -> None:
    ***REMOVED***
    **test_create_membership**
        test if memberships can be created properly without errors
    :param mocker:
    :return: None
    ***REMOVED***
    # Note: Patching put and Query Model requests so they do not perform the operations on the database
    mocker.patch('database.memberships.Memberships.put', return_value=ndb.KeyProperty('Memberships'))
    mocker.patch('database.memberships.Memberships.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        uid: str = membership_mock_data['uid']
        organization_id: str = membership_mock_data['organization_id']
        plan_id: str = membership_mock_data['plan_id']
        plan_start_date: date = membership_mock_data['plan_start_date']

        mocker.patch('database.users.UserValidators.is_user_valid', return_value=True)
        mocker.patch('database.memberships.PlanValidators.plan_exist', return_value=False)
        mocker.patch('database.memberships.MembershipValidators.start_date_valid', return_value=True)

        response, status = memberships_view.add_membership(organization_id=organization_id, uid=uid,
                                                           plan_id=plan_id, plan_start_date=plan_start_date)
        response_data: dict = response.get_json()
        assert response_data.get('message') is not None, 'Unable to read response message'
        assert status == status_codes.successfully_updated_code, response_data['message']
        assert response_data.get('payload') is not None, response_data.get('message')

    mocker.stopall()


# noinspection PyShadowingNames
def test_memberships_create_memberships_data_service_error(mocker) -> None:
    ***REMOVED***
    **test_memberships_create_memberships_un_auth**
        tests if errors will be thrown in-case the application cannot determine the legitimacy of the user request
        or if user isn't suppose to perform the action as needed

    :param mocker:
    :return: None
    ***REMOVED***
    # Note: Patching put and Query Model requests so they do not perform the operations on the database
    mocker.patch('database.memberships.Memberships.put', return_value=ndb.KeyProperty('Memberships'))
    mocker.patch('database.memberships.Memberships.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        uid: str = membership_mock_data['uid']
        organization_id: str = membership_mock_data['organization_id']
        plan_id: str = membership_mock_data['plan_id']
        plan_start_date: date = membership_mock_data['plan_start_date']

        mocker.patch('database.users.UserValidators.is_user_valid', return_value=None)
        mocker.patch('database.memberships.PlanValidators.plan_exist', return_value=None)
        mocker.patch('database.memberships.MembershipValidators.start_date_valid', return_value=None)

        with raises(DataServiceError):
            memberships_view.add_membership(organization_id=organization_id, uid=uid, plan_id=plan_id,
                                            plan_start_date=plan_start_date)

    mocker.stopall()


# noinspection PyShadowingNames
def test_create_memberships_input_errors(mocker) -> None:
    ***REMOVED***
    **test_create_memberships_input_errors**
        test create memberships in-case of faulty data

    :param mocker:
    :return: None
    ***REMOVED***
    # Note: Patching put and Query Model requests so they do not perform the operations on the database
    mocker.patch('database.memberships.Memberships.put', return_value=ndb.KeyProperty('Memberships'))
    mocker.patch('database.memberships.Memberships.query', return_value=MembershipsQueryMock())

    mocker.patch('database.users.UserValidators.is_user_valid', return_value=True)
    mocker.patch('database.memberships.PlanValidators.plan_exist', return_value=False)
    mocker.patch('database.memberships.MembershipValidators.start_date_valid', return_value=True)

    with test_app().app_context():
        # Note: testing for invalid uid
        uid: Optional[str] = random.choice([None, "", " "])
        organization_id: str = membership_mock_data['organization_id']
        plan_id: str = membership_mock_data['plan_id']
        plan_start_date: date = membership_mock_data['plan_start_date']
        with raises(InputError):
            memberships_view.add_membership(organization_id=organization_id, uid=uid,
                                            plan_id=plan_id, plan_start_date=plan_start_date)
        # Note: testing for invalid organization_id
        uid: str = create_id()
        organization_id: Optional[str] = random.choice([None, "", " "])
        with raises(InputError):
            memberships_view.add_membership(organization_id=organization_id, uid=uid,
                                            plan_id=plan_id, plan_start_date=plan_start_date)
        # Note: testing for invalid plan_start_date
        organization_id: str = create_id()
        plan_start_date: Optional[date] = random.choice([None, "", " "])
        with raises(InputError):
            memberships_view.add_membership(organization_id=organization_id, uid=uid,
                                            plan_id=plan_id, plan_start_date=plan_start_date)

        # NOTE : testing for invalid plan id
        plan_start_date: date = today()
        plan_id: Optional[str] = random.choice([None, "", " "])
        with raises(InputError):
            # noinspection PyTypeChecker
            memberships_view.add_membership(organization_id=organization_id, uid=uid,
                                            plan_id=plan_id, plan_start_date=plan_start_date)

    mocker.stopall()


# noinspection PyShadowingNames
def test_update_membership(mocker) -> None:
    ***REMOVED***
    **test_update_membership**
        testing updated membership view function

    :param mocker: mocker module used to patch functions for testing purposes
    :return: None
    ***REMOVED***
    # Note: Patching put and Query Model requests so they do not perform the operations on the database
    mocker.patch('database.memberships.Memberships.put', return_value=ndb.KeyProperty('Memberships'))
    mocker.patch('database.memberships.Memberships.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        uid: str = membership_mock_data['uid']
        organization_id: str = config_instance.ORGANIZATION_ID
        plan_id: str = membership_mock_data['plan_id']
        plan_start_date: date = membership_mock_data['plan_start_date']
        # Note: Mocking test utilities to return results which allows the update process to proceed
        mocker.patch('database.users.UserValidators.is_user_valid', return_value=True)
        mocker.patch('database.memberships.PlanValidators.plan_exist', return_value=False)
        mocker.patch('database.memberships.MembershipValidators.start_date_valid', return_value=True)

        response, status = memberships_view.update_membership(organization_id=organization_id, uid=uid,
                                                              plan_id=plan_id, plan_start_date=plan_start_date)

        assert status == status_codes.successfully_updated_code, "Unable to update membership"
        response_data: dict = response.get_json()
        assert isinstance(response_data, dict), "invalid return data"
        assert response_data.get('message') is not None, "message was not set properly"
        assert response_data.get('payload') is not None, response_data['message']
        assert isinstance(response_data.get('payload'), dict), response_data['message']

    mocker.stopall()


# noinspection PyShadowingNames
def test_update_membership_input_errors(mocker) -> None:
    ***REMOVED***
        **test_update_membership_input_errors**
            tries to run update membership with faulty data,  if an error is not raised
            the test fails
    :param mocker:
    :return: None
    ***REMOVED***
    # Note: Patching put and Query Model requests so they do not perform the operations on the database
    mocker.patch('database.memberships.Memberships.put', return_value=ndb.KeyProperty('Memberships'))
    mocker.patch('database.memberships.Memberships.query', return_value=MembershipsQueryMock())

    mocker.patch('database.users.UserValidators.is_user_valid', return_value=True)
    mocker.patch('database.memberships.PlanValidators.plan_exist', return_value=False)
    mocker.patch('database.memberships.MembershipValidators.start_date_valid', return_value=True)

    with test_app().app_context():
        uid: Optional[str] = random.choice([None, "", " "])
        organization_id: str = config_instance.ORGANIZATION_ID
        plan_id: str = membership_mock_data['plan_id']
        plan_start_date: date = membership_mock_data['plan_start_date']

        with raises(InputError):
            memberships_view.update_membership(organization_id=organization_id, uid=uid, plan_id=plan_id,
                                               plan_start_date=plan_start_date)

        uid: str = create_id()
        organization_id: Optional[str] = random.choice([None, "", " "])
        with raises(InputError):
            memberships_view.update_membership(organization_id=organization_id, uid=uid, plan_id=plan_id,
                                               plan_start_date=plan_start_date)

        organization_id: str = config_instance.ORGANIZATION_ID
        plan_id: Optional[str] = random.choice([None, "", " "])
        with raises(InputError):
            memberships_view.update_membership(organization_id=organization_id, uid=uid, plan_id=plan_id,
                                               plan_start_date=plan_start_date)

    mocker.stopall()


# noinspection PyShadowingNames
def test_set_membership_status(mocker) -> None:
    ***REMOVED***
    **test_set_membership_status**
        testing the ability to set membership payment status

    :param mocker:
    :return: None
    ***REMOVED***
    mocker.patch('database.memberships.Memberships.put', return_value=ndb.KeyProperty('Memberships'))
    mocker.patch('database.memberships.Memberships.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        uid: str = membership_mock_data['uid']
        organization_id: str = config_instance.ORGANIZATION_ID
        status: str = membership_mock_data['payment_status']
        response, status = memberships_view.set_membership_payment_status(organization_id=organization_id,
                                                                          uid=uid, status=status)
        response_data: dict = response.get_json()
        assert status == status_codes.successfully_updated_code, response_data['message']
        assert response_data.get('payload') is not None, response_data['message']

    mocker.stopall()


# noinspection PyShadowingNames
def test_set_membership_status_errors(mocker) -> None:
    ***REMOVED***
    **test_set_membership_status_errors**
        test set_membership_payment_status with faulty data

    :param mocker:
    :return: None
    ***REMOVED***
    mocker.patch('database.memberships.Memberships.put', return_value=ndb.KeyProperty('Memberships'))
    mocker.patch('database.memberships.Memberships.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        uid: Optional[str] = random.choice([None, "", " "])
        organization_id: str = config_instance.ORGANIZATION_ID
        status: str = membership_mock_data['payment_status']
        with raises(InputError):
            memberships_view.set_membership_payment_status(organization_id=organization_id,
                                                           uid=uid, status=status)

        uid: str = create_id()
        organization_id: Optional[str] = random.choice([None, " ", ""])
        with raises(InputError):
            memberships_view.set_membership_payment_status(organization_id=organization_id,
                                                           uid=uid, status=status)

        status: Optional[str] = random.choice([None, "", " "])
        organization_id: str = config_instance.ORGANIZATION_ID
        with raises(InputError):
            memberships_view.set_membership_payment_status(organization_id=organization_id,
                                                           uid=uid, status=status)

    mocker.stopall()


# noinspection PyShadowingNames
def test_change_membership(mocker) -> None:
    ***REMOVED***
    **test_change_membership**
        testing the ability to change_membership

    :param mocker:
    :return: None
    ***REMOVED***
    mocker.patch('database.memberships.Memberships.put', return_value=ndb.KeyProperty('Memberships'))
    membership_query_mock_instance = MembershipsQueryMock()
    membership_query_mock_instance.membership_instance.plan_id = membership_mock_data['plan_id']
    mocker.patch('database.memberships.Memberships.query', return_value=membership_query_mock_instance)

    with test_app().app_context():
        uid: str = membership_mock_data['uid']
        organization_id: str = config_instance.ORGANIZATION_ID
        plan_id: str = membership_mock_data['plan_id']
        dest_plan_id: str = create_id()
        mocker.patch('views.memberships.MembershipsView.plan_exist', return_value=True)
        response, status = memberships_view.change_membership(organization_id=organization_id, uid=uid,
                                                              origin_plan_id=plan_id, dest_plan_id=dest_plan_id)
        assert status == status_codes.successfully_updated_code, "Unable to change membership"

    mocker.stopall()


# noinspection PyShadowingNames
def test_change_memberships_input_errors(mocker):
    ***REMOVED***
    **test_change_memberships_input_errors**

    :param mocker:
    :return:
    ***REMOVED***
    mocker.patch('database.memberships.Memberships.put', return_value=ndb.KeyProperty('Memberships'))
    mocker.patch('database.memberships.Memberships.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        uid: Optional[str] = random.choice([None, "", " "])
        organization_id: str = config_instance.ORGANIZATION_ID
        plan_id: str = membership_mock_data['plan_id']
        dest_plan_id: str = create_id()
        with raises(InputError):
            memberships_view.change_membership(organization_id=organization_id, uid=uid,
                                               origin_plan_id=plan_id, dest_plan_id=dest_plan_id)

        uid: str = create_id()
        organization_id: Optional[str] = random.choice([None, "", " "])
        with raises(InputError):
            memberships_view.change_membership(organization_id=organization_id, uid=uid,
                                               origin_plan_id=plan_id, dest_plan_id=dest_plan_id)

        organization_id: str = create_id()
        plan_id: Optional[str] = random.choice([None, "", " "])
        with raises(InputError):
            memberships_view.change_membership(organization_id=organization_id, uid=uid,
                                               origin_plan_id=plan_id, dest_plan_id=dest_plan_id)

        plan_id: str = create_id()
        dest_plan_id: Optional[str] = random.choice([None, "", " "])
        with raises(InputError):
            memberships_view.change_membership(organization_id=organization_id, uid=uid,
                                               origin_plan_id=plan_id, dest_plan_id=dest_plan_id)

        mocker.stopall()


# noinspection PyShadowingNames
def test_send_welcome_email(mocker) -> None:
    ***REMOVED***
    **test_send_welcome_email**
        tests the ability to schedule a welcome email for members

    :param mocker:
    :return: None
    ***REMOVED***
    mocker.patch('database.memberships.Memberships.put', return_value=ndb.KeyProperty('Memberships'))
    mocker.patch('database.memberships.Memberships.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        uid: str = membership_mock_data['uid']
        organization_id: str = config_instance.ORGANIZATION_ID
        plan_id: str = membership_mock_data['plan_id']
        response, status = memberships_view.send_welcome_email(organization_id=organization_id, uid=uid,
                                                               plan_id=plan_id)
        response_data: dict = response.get_json()
        assert isinstance(response_data, dict), 'bad payload format'
        assert status == status_codes.status_ok_code, "unable to send welcome email"

    mocker.stopall()


# noinspection PyShadowingNames
def test_plan_members_payment_status(mocker) -> None:
    ***REMOVED***
    **test_plan_members_payment_status**
        test the ability to return members with a certain payment status
    :param mocker:
    :return: None
    ***REMOVED***
    mocker.patch('database.memberships.Memberships.put', return_value=ndb.KeyProperty('Memberships'))
    mocker.patch('database.memberships.Memberships.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        organization_id: str = config_instance.ORGANIZATION_ID
        plan_id: str = membership_mock_data['plan_id']
        status: str = membership_mock_data['payment_status']
        response, status = memberships_view.return_plan_members_by_payment_status(
            organization_id=organization_id, plan_id=plan_id, status=status)

        response_data: dict = response.get_json()

        assert isinstance(response_data, dict), 'badly formatted data'
        assert status == status_codes.status_ok_code, "unable to fetch plan members by status"
        assert isinstance(response_data.get('payload'), list), response_data['message']

    mocker.stopall()


# noinspection PyShadowingNames
def test_return_plan_members(mocker) -> None:
    ***REMOVED***
    **test_return_plan_members**
        testing the ability to return plan members
    :param mocker:
    :return: None
    ***REMOVED***
    mocker.patch('database.memberships.Memberships.put', return_value=ndb.KeyProperty('Memberships'))
    mocker.patch('database.memberships.Memberships.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        plan_id: str = membership_mock_data['plan_id']
        organization_id: str = config_instance.ORGANIZATION_ID
        response, status = memberships_view.return_plan_members(organization_id=organization_id, plan_id=plan_id)
        response_data: dict = response.get_json()

        assert isinstance(response_data, dict), 'badly formatted data'
        assert status == status_codes.status_ok_code, response_data['message']
        assert isinstance(response_data.get('payload'), list), response_data['message']

    mocker.stopall()


# noinspection PyShadowingNames
def test_is_member_off(mocker) -> None:
    ***REMOVED***
    **test_is_member_off**
        checks membership plan of a certain member
    :param mocker:
    :return: None
    ***REMOVED***
    mocker.patch('database.memberships.Memberships.put', return_value=ndb.KeyProperty('Memberships'))
    mocker.patch('database.memberships.Memberships.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        uid: str = membership_mock_data['uid']
        organization_id: str = config_instance.ORGANIZATION_ID
        response, status = memberships_view.is_member_off(organization_id=organization_id, uid=uid)

        response_data: dict = response.get_json()
        assert isinstance(response_data, dict), 'badly formatted data'
        assert status == status_codes.status_ok_code, response_data['message']

    mocker.stopall()


# noinspection PyShadowingNames
def test_payment_amount(mocker) -> None:
    ***REMOVED***
    **test_payment_amount**
        test the ability to return payment amount for a user

    :param mocker:
    :return: None
    ***REMOVED***
    mocker.patch('database.memberships.Memberships.put', return_value=ndb.KeyProperty('Memberships'))
    mocker.patch('database.memberships.Memberships.query', return_value=MembershipsQueryMock())
    mocker.patch('views.memberships.MembershipPlansView._get_plan', return_value=MembershipPlansQueryMock().get())

    with test_app().app_context():
        uid: str = membership_mock_data['uid']
        organization_id: str = config_instance.ORGANIZATION_ID
        response, status = memberships_view.payment_amount(organization_id=organization_id, uid=uid)
        response_data: dict = response.get_json()
        assert status == status_codes.status_ok_code, response_data['message']
    mocker.stopall()

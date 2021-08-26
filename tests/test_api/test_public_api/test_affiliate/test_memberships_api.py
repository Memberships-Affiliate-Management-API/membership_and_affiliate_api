import random
from typing import Optional, List
from datetime import datetime, timedelta, date
from random import randint
from google.cloud import ndb
from config import config_instance
from config.currencies import currency_util
from config.exceptions import DataServiceError, status_codes, UnAuthenticatedError, InputError
from database.mixins import AmountMixin
from views.memberships import MembershipsView
from database.memberships import Memberships, MembershipPlans
from utils import create_id, today, datetime_now
from tests import test_app
# noinspection PyUnresolvedReferences
from pytest import raises
# noinspection PyUnresolvedReferences
from pytest_mock import mocker


class MembershipsQueryMock:
    membership_instance: Memberships = Memberships()
    results_range: int = randint(0, 100)

    def __init__(self) -> None:
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
        self.membership_plan_instance.date_created = datetime.now()
        self.membership_plan_instance.plan_name = "bronze"
        self.membership_plan_instance.description = "bronze plan"
        self.membership_plan_instance.total_members = 10
        self.membership_plan_instance.schedule_day = 1
        self.membership_plan_instance.schedule_term = "monthly"
        self.membership_plan_instance.term_payment_amount = AmountMixin(
            amount=100, currency=random.choice(currency_util.currency_symbols()))
        self.membership_plan_instance.registration_amount = AmountMixin(
            amount=100, currency=random.choice(currency_util.currency_symbols()))

    def fetch(self) -> List[MembershipPlans]:
        return [self.membership_plan_instance for _ in range(self.results_range)]

    def get(self) -> MembershipPlans:
        return self.membership_plan_instance


membership_mock_data: dict = {
    "uid": create_id(),
    "organization_id": config_instance.ORGANIZATION_ID,
    "plan_id": create_id(),
    "status": "unpaid",
    "date_created": datetime.now(),
    "plan_start_date": datetime.date(datetime.now() + timedelta(days=5))
}


# noinspection PyShadowingNames
def test_create_membership(mocker) -> None:
    ***REMOVED***
    **test_create_membership**
        test if memberships can be created properly without errors
    :param mocker:
    :return:
    ***REMOVED***
    mocker.patch('google.cloud.ndb.Model.put', return_value=ndb.KeyProperty('Memberships'))
    mocker.patch('google.cloud.ndb.Model.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        membership_view_instance: MembershipsView = MembershipsView()
        uid: str = membership_mock_data['uid']
        organization_id: str = membership_mock_data['organization_id']
        plan_id: str = membership_mock_data['plan_id']
        plan_start_date: date = membership_mock_data['plan_start_date']

        mocker.patch('database.users.UserValidators.is_user_valid', return_value=True)
        mocker.patch('database.memberships.PlanValidators.plan_exist', return_value=False)
        mocker.patch('database.memberships.MembershipValidators.start_date_valid', return_value=True)

        response, status = membership_view_instance.add_membership(
            organization_id=organization_id, uid=uid, plan_id=plan_id, plan_start_date=plan_start_date)
        response_data: dict = response.get_json()
        assert response_data.get('message') is not None, 'Unable to read response message'
        assert status == status_codes.successfully_updated_code, response_data['message']
        assert response_data.get('payload') is not None, response_data.get('message')

    mocker.stopall()


# noinspection PyShadowingNames
def test_memberships_create_memberships_un_auth(mocker) -> None:
    ***REMOVED***
    **test_memberships_create_memberships_un_auth**
        tests if errors will be thrown in-case the application cannot determine the legitimacy of the user request
        or if user isn't suppose to perform the action as needed

    :param mocker:
    :return:
    ***REMOVED***
    mocker.patch('google.cloud.ndb.Model.put', return_value=ndb.KeyProperty('Memberships'))
    mocker.patch('google.cloud.ndb.Model.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        membership_view_instance: MembershipsView = MembershipsView()
        uid = membership_mock_data['uid']
        organization_id = membership_mock_data['organization_id']
        plan_id = membership_mock_data['plan_id']
        plan_start_date = membership_mock_data['plan_start_date']

        with raises(UnAuthenticatedError):
            membership_view_instance.add_membership(organization_id=organization_id, uid=uid,
                                                    plan_id=plan_id, plan_start_date=plan_start_date)

    mocker.stopall()


# noinspection PyUnusedLocal,PyShadowingNames
def test_create_memberships_input_errors(mocker) -> None:
    ***REMOVED***
    **test_create_memberships_input_errors**
        test create memberships in-case of faulty data

    :param mocker:
    :return:
    ***REMOVED***
    mocker.patch('google.cloud.ndb.Model.put', return_value=ndb.KeyProperty('Memberships'))
    mocker.patch('google.cloud.ndb.Model.query', return_value=MembershipsQueryMock())
    with test_app().app_context():
        membership_view_instance: MembershipsView = MembershipsView()
        uid = ''
        organization_id = membership_mock_data['organization_id']
        plan_id = membership_mock_data['plan_id']
        plan_start_date = membership_mock_data['plan_start_date']
        with raises(InputError):
            membership_view_instance.add_membership(organization_id=organization_id, uid=uid,
                                                    plan_id=plan_id, plan_start_date=plan_start_date)
        uid = create_id()
        organization_id = random.choice([None, ""])
        with raises(InputError):
            membership_view_instance.add_membership(organization_id=organization_id, uid=uid,
                                                    plan_id=plan_id, plan_start_date=plan_start_date)
        organization_id = create_id()
        plan_start_date = random.choice([None, ""])
        with raises(InputError):
            # noinspection PyTypeChecker
            membership_view_instance.add_membership(organization_id=organization_id, uid=uid,
                                                    plan_id=plan_id, plan_start_date=plan_start_date)

        plan_start_date = today()
        plan_id = random.choice([None, ""])
        with raises(InputError):
            # noinspection PyTypeChecker
            membership_view_instance.add_membership(organization_id=organization_id, uid=uid,
                                                    plan_id=plan_id, plan_start_date=plan_start_date)

    mocker.stopall()


# noinspection PyShadowingNames
def test_update_membership(mocker) -> None:
    mocker.patch('google.cloud.ndb.Model.put', return_value=ndb.KeyProperty('Memberships'))
    mocker.patch('google.cloud.ndb.Model.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        membership_view_instance: MembershipsView = MembershipsView()
        uid = membership_mock_data['uid']
        organization_id = config_instance.ORGANIZATION_ID
        plan_id = membership_mock_data['plan_id']
        plan_start_date = membership_mock_data['plan_start_date']
        mocker.patch('database.users.UserValidators.is_user_valid', return_value=True)
        mocker.patch('database.memberships.PlanValidators.plan_exist', return_value=False)
        mocker.patch('database.memberships.MembershipValidators.start_date_valid', return_value=True)
        response, status = membership_view_instance.update_membership(organization_id=organization_id, uid=uid,
                                                                      plan_id=plan_id, plan_start_date=plan_start_date)
        assert status == status_codes.successfully_updated_code, "Unable to update membership"
        response_data: dict = response.get_json()
        assert response_data.get('message') is not None, "message was not set properly"
        assert response_data.get('payload') is not None, response_data['message']

    mocker.stopall()


# noinspection PyShadowingNames
def test_update_membership_input_errors(mocker) -> None:
    ***REMOVED***
        **test_update_membership_input_errors**
            tries to run update membership with faulty data,  if an error is not raised
            the test fails
    :param mocker:
    :return:
    ***REMOVED***
    mocker.patch('google.cloud.ndb.Model.put', return_value=ndb.KeyProperty('Memberships'))
    mocker.patch('google.cloud.ndb.Model.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        membership_view_instance: MembershipsView = MembershipsView()
        uid = random.choice([None, ""])
        organization_id = config_instance.ORGANIZATION_ID
        plan_id = membership_mock_data['plan_id']
        plan_start_date = membership_mock_data['plan_start_date']
        with raises(InputError):
            membership_view_instance.update_membership(organization_id=organization_id, uid=uid, plan_id=plan_id,
                                                       plan_start_date=plan_start_date)

        uid = create_id()
        organization_id = random.choice([None, ""])
        with raises(InputError):
            membership_view_instance.update_membership(organization_id=organization_id, uid=uid, plan_id=plan_id,
                                                       plan_start_date=plan_start_date)

        organization_id = create_id()
        plan_id: Optional[str] = random.choice([None, ""])
        with raises(InputError):
            membership_view_instance.update_membership(organization_id=organization_id, uid=uid, plan_id=plan_id,
                                                       plan_start_date=plan_start_date)

    mocker.stopall()


# noinspection PyShadowingNames
def test_set_membership_status(mocker) -> None:
    mocker.patch('google.cloud.ndb.Model.put', return_value=ndb.KeyProperty('Memberships'))
    mocker.patch('google.cloud.ndb.Model.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        membership_view_instance: MembershipsView = MembershipsView()
        uid = membership_mock_data['uid']
        organization_id = config_instance.ORGANIZATION_ID
        status = membership_mock_data['status']
        response, status = membership_view_instance.set_membership_payment_status(organization_id=organization_id,
                                                                                  uid=uid, status=status)
        assert status == status_codes.successfully_updated_code, "Unable to set membership status"
        response, status = membership_view_instance.set_membership_payment_status(organization_id=organization_id,
                                                                                  uid=uid, status="paid")
        assert status == status_codes.successfully_updated_code, "Unable to set membership status"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, response_data['message']
    mocker.stopall()

# # noinspection PyShadowingNames
# def test_change_membership(mocker):
#     mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
#     membership_query_mock_instance = MembershipsQueryMock()
#     membership_query_mock_instance.membership_instance.plan_id = membership_mock_data['plan_id']
#     mocker.patch('google.cloud.ndb.Model.query', return_value=membership_query_mock_instance)
#     with test_app().app_context():
#         membership_view_instance: MembershipsView = MembershipsView()
#         uid: str = membership_mock_data['uid']
#         plan_id: str = membership_mock_data['plan_id']
#         dest_plan_id: str = create_id()
#         mocker.patch('views.memberships.MembershipsView.plan_exist', return_value=True)
#         response, status = membership_view_instance.change_membership(
#             organization_id=config_instance.ORGANIZATION_ID, uid=uid, origin_plan_id=plan_id, dest_plan_id=dest_plan_id)
#         assert status == 200, "Unable to change membership"
#
#     mocker.stopall()
#
#
# # noinspection PyShadowingNames
# def test_send_welcome_email(mocker):
#     mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
#     mocker.patch('google.cloud.ndb.Model.query', return_value=MembershipsQueryMock())
#
#     with test_app().app_context():
#         membership_view_instance: MembershipsView = MembershipsView()
#         uid: str = membership_mock_data['uid']
#         plan_id: str = membership_mock_data['plan_id']
#         response, status = membership_view_instance.send_welcome_email(organization_id=config_instance.ORGANIZATION_ID,
#                                                                        uid=uid, plan_id=plan_id)
#         assert status == 200, "unable to send welcome email"
#
#     mocker.stopall()
#
#
# # noinspection PyShadowingNames
# def test_plan_members_payment_status(mocker):
#     mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
#     mocker.patch('google.cloud.ndb.Model.query', return_value=MembershipsQueryMock())
#
#     with test_app().app_context():
#         membership_view_instance: MembershipsView = MembershipsView()
#
#         plan_id: str = membership_mock_data['plan_id']
#         status: str = membership_mock_data['status']
#         response, status = membership_view_instance.return_plan_members_by_payment_status(
#             organization_id=config_instance.ORGANIZATION_ID, plan_id=plan_id, status=status)
#         assert status == 200, "unable to fetch plan members by status"
#
#     mocker.stopall()
#
#
# # noinspection PyShadowingNames
# def test_return_plan_members(mocker):
#     mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
#     mocker.patch('google.cloud.ndb.Model.query', return_value=MembershipsQueryMock())
#
#     with test_app().app_context():
#         membership_view_instance: MembershipsView = MembershipsView()
#         plan_id: str = membership_mock_data['plan_id']
#         response, status = membership_view_instance.return_plan_members(organization_id=config_instance.ORGANIZATION_ID,
#                                                                         plan_id=plan_id)
#         assert status == 200, "unable to fetch plan members"
#
#     mocker.stopall()
#
#
# # noinspection PyShadowingNames
# def test_is_member_off(mocker):
#     mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
#     mocker.patch('google.cloud.ndb.Model.query', return_value=MembershipsQueryMock())
#
#     with test_app().app_context():
#         membership_view_instance: MembershipsView = MembershipsView()
#         uid: str = membership_mock_data['uid']
#         response, status = membership_view_instance.is_member_off(organization_id=config_instance.ORGANIZATION_ID,
#                                                                   uid=uid)
#
#         assert status == 200, "unable to test membership status"
#
#     mocker.stopall()
#
#
# # noinspection PyShadowingNames
# def test_payment_amount(mocker):
#     mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
#     mocker.patch('google.cloud.ndb.Model.query', return_value=MembershipsQueryMock())
#     with test_app().app_context():
#         membership_view_instance: MembershipsView = MembershipsView()
#         uid: str = membership_mock_data['uid']
#         mocker.patch('views.memberships.MembershipPlansView.get_plan',
#                      return_value=MembershipPlansQueryMock().get())
#
#         response, status = membership_view_instance.payment_amount(organization_id=config_instance.ORGANIZATION_ID, uid=uid)
#         response_data: dict = response.get_json()
#         assert status == 200, response_data['message']
#     mocker.stopall()
#
#
# # noinspection PyShadowingNames
# def test_set_payment_status(mocker):
#     mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
#     mocker.patch('google.cloud.ndb.Model.query', return_value=MembershipsQueryMock())
#
#     with test_app().app_context():
#         membership_view_instance: MembershipsView = MembershipsView()
#         uid: str = membership_mock_data['uid']
#         status: str = "paid"
#         response, status = membership_view_instance.set_membership_payment_status(
#             organization_id=config_instance.ORGANIZATION_ID, uid=uid, status=status)
#         assert status == 200, "Unable to set payment status"
#         status: str = "unpaid"
#         response, status = membership_view_instance.set_membership_payment_status(
#             organization_id=config_instance.ORGANIZATION_ID, uid=uid, status=status)
#         assert status == 200, "Unable to set payment status"
#
#     mocker.stopall()

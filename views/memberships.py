import functools
import typing
from google.api_core.exceptions import RetryError, Aborted
from flask import jsonify, current_app
from datetime import datetime, date
from config.exceptions import DataServiceError, InputError, error_codes
from database.memberships import MembershipPlans, AccessRights, Memberships, Coupons
from database.memberships import PlanValidators as PlanValid
from database.mixins import AmountMixin
from database.users import UserValidators as UserValid
from database.memberships import MembershipValidators as MemberValid
from database.memberships import CouponsValidator as CouponValid
from utils.utils import create_id, return_ttl, timestamp, can_cache
from main import app_cache
from config.exception_handlers import handle_view_errors
from config.use_context import use_context


# TODO Create Test Cases for Memberships & Documentations
class Validators(UserValid, PlanValid, MemberValid, CouponValid):
    ***REMOVED***
        validators for membership views
    ***REMOVED***

    def __init__(self):
        super(Validators, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def can_add_member(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                       plan_id: typing.Union[str, None], start_date: date) -> bool:
        user_valid: typing.Union[None, bool] = self.is_user_valid(organization_id=organization_id, uid=uid)
        plan_exist: typing.Union[None, bool] = self.plan_exist(organization_id=organization_id, plan_id=plan_id)
        date_valid: typing.Union[None, bool] = self.start_date_valid(start_date=start_date)

        if isinstance(user_valid, bool) and isinstance(plan_exist, bool) and isinstance(date_valid, bool):
            return user_valid and not plan_exist and date_valid

        message: str = "Unable to verify input data, due to database error, please try again later"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def can_add_member_async(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                                   plan_id: typing.Union[str, None],
                                   start_date: date) -> bool:
        user_valid: typing.Union[None, bool] = await self.is_user_valid_async(organization_id=organization_id, uid=uid)
        plan_exist: typing.Union[None, bool] = await self.plan_exist_async(organization_id=organization_id,
                                                                           plan_id=plan_id)
        date_valid: typing.Union[None, bool] = await self.start_date_valid_async(start_date=start_date)

        if isinstance(user_valid, bool) and isinstance(plan_exist, bool) and isinstance(date_valid, bool):
            return user_valid and not plan_exist and date_valid

        message: str = "Unable to verify input data, due to database error, please try again later"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def can_add_plan(self, organization_id: typing.Union[str, None], plan_name: typing.Union[str, None]) -> bool:
        name_exist: typing.Union[None, bool] = self.plan_name_exist(organization_id=organization_id,
                                                                    plan_name=plan_name)
        if isinstance(name_exist, bool):
            return not name_exist
        message: str = "Unable to verify input data, due to database error, please try again later"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def can_add_plan_async(self, organization_id: typing.Union[str, None],
                                 plan_name: typing.Union[str, None]) -> bool:
        name_exist: typing.Union[None, bool] = await self.plan_name_exist_async(
            organization_id=organization_id, plan_name=plan_name)

        if isinstance(name_exist, bool):
            return not name_exist
        message: str = "Unable to verify input data, due to database error, please try again later"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def can_update_plan(self, organization_id: typing.Union[str, None],
                        plan_id: typing.Union[str, None], plan_name: typing.Union[str, None]) -> bool:
        plan_exist: typing.Union[None, bool] = self.plan_exist(organization_id=organization_id, plan_id=plan_id)
        plan_name_exist: typing.Union[None, bool] = self.plan_name_exist(
            organization_id=organization_id, plan_name=plan_name)

        if isinstance(plan_exist, bool) and isinstance(plan_name_exist, bool):
            return plan_exist and plan_name_exist
        message: str = "Unable to verify input data, due to database error, please try again later"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def can_update_plan_async(self, organization_id: typing.Union[str, None],
                                    plan_id: typing.Union[str, None], plan_name: typing.Union[str, None]) -> bool:

        plan_exist: typing.Union[None, bool] = await self.plan_exist_async(
            organization_id=organization_id, plan_id=plan_id)

        plan_name_exist: typing.Union[None, bool] = await self.plan_name_exist_async(
            organization_id=organization_id, plan_name=plan_name)

        if isinstance(plan_exist, bool) and isinstance(plan_name_exist, bool):
            return plan_exist and plan_name_exist
        message: str = "Unable to verify input data, due to database error, please try again later"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def can_add_coupon(self, organization_id: typing.Union[str, None], code: typing.Union[str, None],
                       expiration_time: typing.Union[int, None],
                       discount: typing.Union[int, None]) -> bool:

        coupon_exist: typing.Union[None, bool] = self.coupon_exist(organization_id=organization_id, code=code)
        expiration_valid: typing.Union[None, bool] = self.expiration_valid(expiration_time=expiration_time)
        discount_valid: typing.Union[None, bool] = self.discount_valid(discount_valid=discount)

        if isinstance(coupon_exist, bool) and isinstance(expiration_valid, bool) and isinstance(discount_valid, bool):
            return (not coupon_exist) and expiration_valid and discount_valid
        message: str = "Unable to verify input data"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def can_add_coupon_async(self, organization_id: typing.Union[str, None], code: typing.Union[str, None],
                                   expiration_time: typing.Union[int, None],
                                   discount: typing.Union[int, None]) -> bool:
        coupon_exist: typing.Union[None, bool] = await self.coupon_exist_async(organization_id=organization_id,
                                                                               code=code)

        expiration_valid: typing.Union[None, bool] = await self.expiration_valid_async(expiration_time=expiration_time)
        discount_valid: typing.Union[None, bool] = await self.discount_valid_async(discount_valid=discount)

        if isinstance(coupon_exist, bool) and isinstance(expiration_valid, bool) and isinstance(discount_valid, bool):
            return (not coupon_exist) and expiration_valid and discount_valid
        message: str = "Unable to verify input data"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def can_update_coupon(self, organization_id: typing.Union[str, None], code: typing.Union[str, None],
                          expiration_time: typing.Union[int, None],
                          discount: typing.Union[int, None]) -> bool:

        coupon_exist: typing.Union[None, bool] = self.coupon_exist(organization_id=organization_id, code=code)
        expiration_valid: typing.Union[None, bool] = self.expiration_valid(expiration_time=expiration_time)
        discount_valid: typing.Union[None, bool] = self.discount_valid(discount_valid=discount)

        if isinstance(coupon_exist, bool) and isinstance(expiration_valid, bool) and isinstance(discount_valid, bool):
            return coupon_exist and expiration_valid and discount_valid
        message: str = "Unable to verify input data"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def can_update_coupon_async(self, organization_id: typing.Union[str, None], code: typing.Union[str, None],
                                      expiration_time: typing.Union[int, None],
                                      discount: typing.Union[int, None]) -> bool:

        coupon_exist: typing.Union[None, bool] = await self.coupon_exist_async(organization_id=organization_id,
                                                                               code=code)
        expiration_valid: typing.Union[None, bool] = await self.expiration_valid_async(expiration_time=expiration_time)
        discount_valid: typing.Union[None, bool] = await self.discount_valid_async(discount_valid=discount)

        if isinstance(coupon_exist, bool) and isinstance(expiration_valid, bool) and isinstance(discount_valid, bool):
            return coupon_exist and expiration_valid and discount_valid
        message: str = "Unable to verify input data"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)


# noinspection DuplicatedCode
class MembershipsView(Validators):

    def __init__(self):
        super(MembershipsView, self).__init__()

    @use_context
    @handle_view_errors
    def _create_or_update_membership(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                                     plan_id: typing.Union[str, None], plan_start_date: date) -> tuple:

        if self.can_add_member(organization_id=organization_id, uid=uid, plan_id=plan_id,
                               start_date=plan_start_date) is True:

            # can use get to simplify this and make transactions faster
            membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                                 Memberships.uid == uid).get()

            if not (isinstance(membership_instance, Memberships)):
                membership_instance: Memberships = Memberships()
                membership_instance.plan_id = create_id()
                membership_instance.status = 'Unpaid'
                membership_instance.date_created = datetime.now()

            membership_instance.uid = uid
            membership_instance.plan_start_date = plan_start_date
            key = membership_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "Unable to save membership instance to database, please try again"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
            return jsonify({'status': True, 'message': 'successfully updated membership',
                            'payload': membership_instance.to_dict()}), 200

        message: str = ***REMOVED***Unable to create or update memberships this may be 
        due to errors in database connections or duplicate data***REMOVED***
        return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    async def _create_or_update_membership_async(self, organization_id: typing.Union[str, None],
                                                 uid: typing.Union[str, None], plan_id: typing.Union[str, None],
                                                 plan_start_date: date) -> tuple:

        # TODO update can_add_member_async to include organization_id
        if await self.can_add_member_async(organization_id=organization_id, uid=uid, plan_id=plan_id,
                                           start_date=plan_start_date) is True:

            # can use get to simplify this and make transactions faster
            membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                                 Memberships.uid == uid).get_async().get_result()

            if not (isinstance(membership_instance, Memberships)):
                membership_instance: Memberships = Memberships()
                membership_instance.plan_id = create_id()
                membership_instance.status = 'Unpaid'
                membership_instance.date_created = datetime.now()

            membership_instance.uid = uid
            membership_instance.plan_start_date = plan_start_date
            key = membership_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
            if not bool(key):
                message: str = "Unable to save membership instance to database, please try again"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
            return jsonify({'status': True, 'message': 'successfully updated membership',
                            'payload': membership_instance.to_dict()}), 200

        message: str = ***REMOVED***Unable to create or update memberships this may be 
        due to errors in database connections or duplicate data***REMOVED***
        return jsonify({'status': False, 'message': message}), 500

    def add_membership(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                       plan_id: typing.Union[str, None], plan_start_date: date) -> tuple:

        return self._create_or_update_membership(organization_id=organization_id, uid=uid, plan_id=plan_id,
                                                 plan_start_date=plan_start_date)

    async def add_membership_async(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                                   plan_id: typing.Union[str, None], plan_start_date: date) -> tuple:

        return await self._create_or_update_membership_async(organization_id=organization_id, uid=uid,
                                                             plan_id=plan_id, plan_start_date=plan_start_date)

    def update_membership(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                          plan_id: typing.Union[str, None], plan_start_date: date) -> tuple:

        return self._create_or_update_membership(organization_id=organization_id, uid=uid, plan_id=plan_id,
                                                 plan_start_date=plan_start_date)

    async def update_membership_async(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                                      plan_id: typing.Union[str, None], plan_start_date: date) -> tuple:

        return await self._create_or_update_membership_async(organization_id=organization_id, uid=uid, plan_id=plan_id,
                                                             plan_start_date=plan_start_date)

    @use_context
    @handle_view_errors
    def set_membership_status(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                              status: typing.Union[str, None]) -> tuple:

        membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                             Memberships.uid == uid).get()

        if isinstance(membership_instance, Memberships):
            membership_instance.status = status
            key = membership_instance.put(retries=self._max_retries, timeout=self._max_timeout)

            if not bool(key):
                message: str = "Unable to save membership instance to database, please try again"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            message: str = "Successfully update membership status"
            return jsonify({'status': True, 'payload': membership_instance.to_dict(), 'message': message}), 200

        message: str = "Memberships record not found"
        return jsonify({'status': True, 'payload': membership_instance.to_dict(), 'message': message}), 200

    @use_context
    @handle_view_errors
    async def set_membership_status_async(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                                          status: typing.Union[str, None]) -> tuple:

        membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                             Memberships.uid == uid).get_async().get_result()

        if isinstance(membership_instance, Memberships):
            membership_instance.status = status
            key = membership_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
            if not bool(key):
                message: str = "Unable to save membership instance to database, please try again"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
            message: str = "Successfully update membership status"
            return jsonify({'status': True, 'payload': membership_instance.to_dict(), 'message': message}), 200
        message: str = "Memberships record not found"
        return jsonify({'status': True, 'payload': membership_instance.to_dict(), 'message': message}), 200

    @use_context
    @handle_view_errors
    def change_membership(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                          origin_plan_id: typing.Union[str, None], dest_plan_id: str) -> tuple:

        membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                             Memberships.uid == uid).get()

        if isinstance(membership_instance, Memberships) and (membership_instance.plan_id == origin_plan_id):

            if self.plan_exist(organization_id=organization_id, plan_id=dest_plan_id) is True:
                membership_instance.plan_id = dest_plan_id
                key = membership_instance.put(retries=self._max_retries,
                                              timeout=self._max_timeout)
            else:
                # This maybe be because the original plan is deleted but its a rare case
                membership_instance.plan_id = dest_plan_id
                key = membership_instance.put(retries=self._max_retries,
                                              timeout=self._max_timeout)
            if key is None:
                message: str = "Unable to Change Membership, please try again later"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
        else:
            message: str = "Unable to change membership, cannot find original membership record"
            return jsonify({'status': False, 'message': message}), 500
        return jsonify({'status': True, 'message': 'successfully updated membership',
                        'payload': membership_instance.to_dict()}), 200

    @use_context
    @handle_view_errors
    async def change_membership_async(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                                      origin_plan_id: typing.Union[str, None], dest_plan_id: str) -> tuple:

        membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                             Memberships.uid == uid).get_async().get_result()

        if isinstance(membership_instance, Memberships) and (membership_instance.plan_id == origin_plan_id):
            if await self.plan_exist_async(organization_id=organization_id, plan_id=dest_plan_id) is True:
                membership_instance.plan_id = dest_plan_id
                key = membership_instance.put_async(retries=self._max_retries,
                                                    timeout=self._max_timeout).get_result()
            else:
                # This maybe be because the original plan is deleted but its a rare case
                membership_instance.plan_id = dest_plan_id
                key = membership_instance.put_async(retries=self._max_retries,
                                                    timeout=self._max_timeout).get_result()

            if not (bool(key)):
                message: str = "Unable to Change Membership, please try again later"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
        else:
            message: str = "Unable to change membership, cannot find original membership record"
            return jsonify({'status': False, 'message': message}), 500
        return jsonify({'status': True, 'message': 'successfully updated membership',
                        'payload': membership_instance.to_dict()}), 200

    # noinspection PyUnusedLocal
    @use_context
    @handle_view_errors
    def send_welcome_email(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                           plan_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            just send a request to the email service to send emails
        ***REMOVED***
        return "Ok", 200

    # noinspection PyUnusedLocal
    @use_context
    @handle_view_errors
    async def send_welcome_email_async(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                                       plan_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            just send a request to the email service to send emails
        ***REMOVED***
        return "Ok", 200

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def return_plan_members_by_payment_status(self, organization_id: typing.Union[str, None],
                                              plan_id: typing.Union[str, None],
                                              status: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            for members of this plan_id return members by payment_status
            payment status should either be paid or unpaid
        ***REMOVED***
        membership_list: typing.List[Memberships] = Memberships.query(Memberships.organization_id == organization_id,
                                                                      Memberships.plan_id == plan_id,
                                                                      Memberships.status == status).fetch()

        if isinstance(membership_list, list) and len(membership_list) > 0:
            response_data: typing.List[dict] = [member.to_dict() for member in membership_list]
            message: str = 'successfully fetched members'
            return jsonify({'status': True, 'payload': response_data, 'message': message}), 200
        else:
            message: str = "Unable to find plan members whose payment status is {}".format(status)
            return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def return_plan_members_by_payment_status_async(self, organization_id: typing.Union[str, None],
                                                          plan_id: typing.Union[str, None],
                                                          status: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            for members of this plan_id return members by payment_status
            payment status should either be paid or unpaid
        ***REMOVED***
        membership_list: typing.List[Memberships] = Memberships.query(
            Memberships.organization_id == organization_id, Memberships.plan_id == plan_id,
            Memberships.status == status).fetch_async().get_result()

        if isinstance(membership_list, list) and len(membership_list) > 0:
            response_data: typing.List[dict] = [member.to_dict() for member in membership_list]
            message: str = 'successfully fetched members'
            return jsonify({'status': True, 'payload': response_data, 'message': message}), 200
        else:
            message: str = "Unable to find plan members whose payment status is {}".format(status)
            return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def return_members_by_payment_status(self, organization_id: typing.Union[str, None],
                                         status: typing.Union[str, None]) -> tuple:

        membership_list: typing.List[Memberships] = Memberships.query(Memberships.organization_id == organization_id,
                                                                      Memberships.status == status).fetch()

        if isinstance(membership_list, list) and len(membership_list) > 0:
            response_data: typing.List[dict] = [member.to_dict() for member in membership_list]
            message: str = 'successfully fetched members'
            return jsonify({'status': True, 'payload': response_data, 'message': message}), 200
        else:
            message: str = "Unable to find plan members whose payment status is {}".format(status)
            return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def return_members_by_payment_status_async(self, organization_id: typing.Union[str, None],
                                                     status: typing.Union[str, None]) -> tuple:

        membership_list: typing.List[Memberships] = Memberships.query(
            Memberships.organization_id == organization_id, Memberships.status == status).fetch_async().get_result()

        if isinstance(membership_list, list) and len(membership_list) > 0:
            response_data: typing.List[dict] = [member.to_dict() for member in membership_list]
            message: str = 'successfully fetched members'
            return jsonify({'status': True, 'payload': response_data, 'message': message}), 200
        else:
            message: str = "Unable to find plan members whose payment status is {}".format(status)
            return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def return_plan_members(self, organization_id: typing.Union[str, None], plan_id: typing.Union[str, None]) -> tuple:

        ***REMOVED***
            return all members of a plan
        ***REMOVED***
        if not isinstance(plan_id, str) or (not bool(plan_id)):
            return jsonify({'status': False, 'message': 'plan_id is required'}), 500
        membership_list: typing.List[Memberships] = Memberships.query(Memberships.organization_id == organization_id,
                                                                      Memberships.plan_id == plan_id).fetch()

        if isinstance(membership_list, list) and len(membership_list) > 0:
            response_data: typing.List[dict] = [member.to_dict() for member in membership_list]
            message: str = 'successfully fetched members'
            return jsonify({'status': True, 'payload': response_data, 'message': message}), 200
        else:
            message: str = "Unable to find members of plan {}"
            return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def return_plan_members_async(self, organization_id: typing.Union[str, None],
                                        plan_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            return all members of a plan
        ***REMOVED***
        if not isinstance(plan_id, str) or (not bool(plan_id)):
            return jsonify({'status': False, 'message': 'plan_id is required'}), 500

        membership_list: typing.List[Memberships] = Memberships.query(
            Memberships.organization_id == organization_id, Memberships.plan_id == plan_id).fetch_async().get_result()

        if isinstance(membership_list, list) and len(membership_list) > 0:
            response_data: typing.List[dict] = [member.to_dict() for member in membership_list]
            message: str = 'successfully fetched members'
            return jsonify({'status': True, 'payload': response_data, 'message': message}), 200
        else:
            message: str = "Unable to find members of plan {}"
            return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def return_plan_members_async(self, organization_id: typing.Union[str, None],
                                        plan_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            return all members of a plan
        ***REMOVED***
        if not isinstance(plan_id, str) or (not bool(plan_id)):
            return jsonify({'status': False, 'message': 'plan_id is required'}), 500

        membership_list: typing.List[Memberships] = Memberships.query(
            Memberships.organization_id == organization_id, Memberships.plan_id == plan_id).fetch_async().get_result()

        if isinstance(membership_list, list) and len(membership_list) > 0:
            response_data: typing.List[dict] = [member.to_dict() for member in membership_list]
            message: str = 'successfully fetched members'
            return jsonify({'status': True, 'payload': response_data, 'message': message}), 200
        else:
            message: str = "Unable to find members of plan {}"
            return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def is_member_off(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            returns user membership details
        ***REMOVED***
        member_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                         Memberships.uid == uid).get()

        if isinstance(member_instance, Memberships):
            return jsonify(
                {'status': True, 'payload': member_instance.to_dict(), 'message': 'successfully fetched members'}), 200
        else:
            return jsonify({'status': False, 'message': 'user does not have any membership plan'}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def is_member_off_async(self, organization_id: typing.Union[str, None],
                                  uid: typing.Union[str, None]) -> tuple:

        ***REMOVED***
            returns user membership details
        ***REMOVED***
        member_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                         Memberships.uid == uid).get_async().get_result()

        if isinstance(member_instance, Memberships):
            return jsonify(
                {'status': True, 'payload': member_instance.to_dict(), 'message': 'successfully fetched members'}), 200
        else:
            message: str = 'user does not have any membership plan'
            return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def payment_amount(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            for a specific user return payment amount
        ***REMOVED***
        # TODO this function has to be secured
        membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                             Memberships.uid == uid).get()

        if isinstance(membership_instance, Memberships):
            plan_id: str = membership_instance.plan_id
            membership_plan_instance: MembershipPlans = MembershipPlansView().get_plan(
                organization_id=organization_id, plan_id=plan_id)

            if not bool(membership_plan_instance):
                message: str = 'could not find plan associate with the plan_id'
                return jsonify({'status': False, 'message': message}), 500

            if bool(membership_plan_instance.term_payment_amount) and bool(
                    membership_plan_instance.registration_amount):
                amount_data: dict = {
                    'term_payment_amount': membership_plan_instance.term_payment_amount.to_dict(),
                    'registration_amount': membership_plan_instance.registration_amount.to_dict()}
                message: str = 'successfully returned payment details'
                return jsonify({'status': True, 'payload': amount_data, 'message': message}), 200

        message: str = 'unable to locate membership details'
        return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def payment_amount_async(self, organization_id: typing.Union[str, None],
                                   uid: typing.Union[str, None]) -> tuple:

        ***REMOVED***
            for a specific user return payment amount
        ***REMOVED***

        membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                             Memberships.uid == uid).get_async().get_result()

        if isinstance(membership_instance, Memberships):
            plan_id: str = membership_instance.plan_id
            membership_plan_instance: MembershipPlans = await MembershipPlansView().get_plan_async(
                organization_id=organization_id, plan_id=plan_id)

            if not bool(membership_plan_instance):
                message: str = 'could not find plan associate with the plan_id'
                return jsonify({'status': False, 'message': message}), 500

            if bool(membership_plan_instance.term_payment_amount) and bool(
                    membership_plan_instance.registration_amount):
                amount_data: dict = {
                    'term_payment_amount': membership_plan_instance.term_payment_amount.to_dict(),
                    'registration_amount': membership_plan_instance.registration_amount.to_dict()}
                message: str = 'successfully returned payment details'
                return jsonify({'status': True, 'payload': amount_data, 'message': message}), 200

        message: str = 'unable to locate membership details'
        return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    def set_payment_status(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                           status: typing.Union[str, None]) -> tuple:

        ***REMOVED***
            # status is paid or unpaid
            for a specific user set payment status
        ***REMOVED***
        membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                             Memberships.uid == uid).get()

        if isinstance(membership_instance, Memberships):
            membership_instance.status = status
            key = membership_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = 'for some reason we are unable to set payment status'
                raise InputError(status=422, description=message)
        else:
            message: str = "Membership not found"
            return jsonify({'status': False, 'message': message}), 500

        message: str = 'payment status has been successfully set'
        return jsonify({'status': True, 'message': message,
                        'payload': membership_instance.to_dict()}), 200

    @use_context
    @handle_view_errors
    async def set_payment_status_async(self, organization_id: typing.Union[str, None],
                                       uid: typing.Union[str, None], status: typing.Union[str, None]) -> tuple:

        ***REMOVED***
            # status is paid or unpaid
            for a specific user set payment status
        ***REMOVED***

        membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                             Memberships.uid == uid).get_async().get_result()

        if isinstance(membership_instance, Memberships):
            membership_instance.status = status
            key = membership_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
            if not bool(key):
                message: str = 'for some reason we are unable to set payment status'
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
        else:
            message: str = "Membership not found"
            return jsonify({'status': False, 'message': message}), 500

        return jsonify({'status': True, 'message': 'payment status has been successfully set',
                        'payload': membership_instance.to_dict()}), 200


def plan_data_wrapper(func):
    ***REMOVED***
        wraps add plan in order to check validity of the input data,
        throws InputError in-case of an error in Input
    :param func:
    :return: func with correct variables

    ***REMOVED***

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        membership_plan_data = kwargs.get('membership_plan_data')
        if not bool(membership_plan_data):
            message: str = "Input is required"
            raise InputError(status=422, description=message)

        plan_name: typing.Union[str, None] = membership_plan_data.get('plan_name')
        if not bool(plan_name.strip()):
            message: str = "plan name is required"
            raise InputError(status=422, description=message)

        description: typing.Union[str, None] = membership_plan_data.get('description')
        if not bool(description.strip()):
            message: str = "description is required"
            raise InputError(status=422, description=message)

        schedule_day: typing.Union[int, None] = membership_plan_data.get('schedule_day')
        # NOTE: if schedule_day is None or Zero then this is an Error
        if not bool(schedule_day):
            message: str = "schedule_day is required and cannot be zero or Null"
            raise InputError(status=422, description=message)

        schedule_term: typing.Union[str, None] = membership_plan_data.get('schedule_term')
        if not bool(schedule_term.strip()):
            message: str = "schedule term is required"
            raise InputError(status=422, description=message)

        # int(None) avoiding this
        term_payment: int = int(membership_plan_data.get('term_payment') or 0)

        registration_amount: int = int(membership_plan_data.get('registration_amount') or 0)

        currency: typing.Union[str, None] = membership_plan_data.get('currency')
        if not bool(currency.strip()):
            message: str = "currency is required"
            raise InputError(status=422, description=message)

        organization_id: typing.Union[str, None] = membership_plan_data.get('organization_id')
        if not bool(organization_id.strip()):
            message: str = "organization is required"
            raise InputError(status=422, description=message)

        service_id: typing.Union[str, None] = membership_plan_data.get('service_id')
        if not bool(service_id.strip()):
            message: str = "service or product must be created first before payment plans are created"
            raise InputError(status=error_codes.input_error_code, description=message)

        return func(organization_id=organization_id, service_id=service_id, plan_name=plan_name,
                    description=description, schedule_day=schedule_day,
                    schedule_term=schedule_term, term_payment=term_payment, registration_amount=registration_amount,
                    currency=currency, *args)

    return wrapper


# noinspection DuplicatedCode
class MembershipPlansView(Validators):
    def __init__(self):
        super(MembershipPlansView, self).__init__()

    # TODO - add Membership Plans Validators

    @staticmethod
    def create_plan_in_paypal_services(organization_id: str, service_id: str, plan_name: str, description: str,
                                       schedule_day: int, schedule_term: str, term_payment: int,
                                       registration_amount: int, currency: str) -> typing.Union[str, None]:
        ***REMOVED***
            creates this plan in paypal services first
        :param service_id:
        :param organization_id:
        :param plan_name:
        :param description:
        :param schedule_day:
        :param schedule_term:
        :param term_payment:
        :param registration_amount:
        :param currency:
        :return: a string representing payment plan_id or None
        ***REMOVED***
        pass

    @use_context
    @handle_view_errors
    @plan_data_wrapper
    def add_plan(self, organization_id: str, service_id: str, plan_name: str, description: str, schedule_day: int,
                 schedule_term: str, term_payment: int, registration_amount: int, currency: str) -> tuple:
        ***REMOVED***
            checks to see if the plan actually exists and the new plan name wont cause a conflict with
            an existing name
             plan_name: str, description: str, schedule_day: int, schedule_term: str,
                 term_payment: int, registration_amount: int, currency: str, is_active: bool) -> tuple:

        ***REMOVED***

        is_active = True
        # Note: Creating the payment plan in PayPal Services Note: this means the product for the
        #  payment plan is already created

        plan_id: typing.Union[str, None] = self.create_plan_in_paypal_services(
            organization_id=organization_id, service_id=service_id, plan_name=plan_name, description=description,
            schedule_day=schedule_day,
            schedule_term=schedule_term, term_payment=term_payment, registration_amount=registration_amount,
            currency=currency)
        if not bool(plan_id):
            message: str = "Unable to create Payment Plan check your service_id or inform admin"
            raise InputError(status=error_codes.input_error_code, description=message)

        if self.can_add_plan(organization_id=organization_id, plan_name=plan_name) is True:
            total_members: int = 0
            # Creating Amount Mixins to represent real currency
            curr_term_payment: AmountMixin = AmountMixin(amount=term_payment, currency=currency)
            curr_registration_amount: AmountMixin = AmountMixin(amount=registration_amount, currency=currency)
            # IF one of the values is not defined then this will throw an error
            plan_instance: MembershipPlans = MembershipPlans(organization_id=organization_id,
                                                             service_id=service_id,
                                                             plan_id=plan_id,
                                                             plan_name=plan_name,
                                                             description=description,
                                                             total_members=total_members,
                                                             schedule_day=schedule_day,
                                                             schedule_term=schedule_term,
                                                             term_payment=curr_term_payment,
                                                             registration_amount=curr_registration_amount,
                                                             is_active=is_active,
                                                             date_created=datetime.now().date())

            key = plan_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = 'for some reason we are unable to create a new plan'
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
        else:
            message: str = 'Unable to create plan'
            return jsonify({'status': False, 'message': message}), 500
        return jsonify({'status': True, 'message': 'successfully created new membership plan',
                        'payload': plan_instance.to_dict()}), 200

    @use_context
    @handle_view_errors
    @plan_data_wrapper
    async def add_plan_async(self, organization_id: str, service_id: str, plan_name: str, description: str,
                             schedule_day: int,
                             schedule_term: str, term_payment: int, registration_amount: int, currency: str) -> tuple:
        ***REMOVED***
            checks to see if the plan actually exists and the new plan name wont cause a conflict with
            an existing name
             plan_name: str, description: str, schedule_day: int, schedule_term: str,
                 term_payment: int, registration_amount: int, currency: str, is_active: bool) -> tuple:

        ***REMOVED***

        is_active = True
        # Note: Creating the payment plan in PayPal Services Note: this means the product for the
        #  payment plan is already created

        plan_id: typing.Union[str, None] = self.create_plan_in_paypal_services(
            organization_id=organization_id, service_id=service_id, plan_name=plan_name, description=description,
            schedule_day=schedule_day,
            schedule_term=schedule_term, term_payment=term_payment, registration_amount=registration_amount,
            currency=currency)

        if not bool(plan_id):
            message: str = "Unable to create Payment Plan check your service_id or inform admin"
            raise InputError(status=error_codes.input_error_code, description=message)

        if self.can_add_plan_async(organization_id=organization_id, plan_name=plan_name) is True:
            total_members: int = 0
            # Creating Amount Mixins to represent real currency
            curr_term_payment: AmountMixin = AmountMixin(amount=term_payment, currency=currency)
            curr_registration_amount: AmountMixin = AmountMixin(amount=registration_amount, currency=currency)
            # IF one of the values is not defined then this will throw an error
            plan_instance: MembershipPlans = MembershipPlans(organization_id=organization_id,
                                                             service_id=service_id,
                                                             plan_id=plan_id,
                                                             plan_name=plan_name,
                                                             description=description,
                                                             total_members=total_members,
                                                             schedule_day=schedule_day,
                                                             schedule_term=schedule_term,
                                                             term_payment=curr_term_payment,
                                                             registration_amount=curr_registration_amount,
                                                             is_active=is_active,
                                                             date_created=datetime.now().date())

            key = plan_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
            if not bool(key):
                message: str = 'for some reason we are unable to create a new plan'
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
        else:
            message: str = 'Unable to create plan'
            return jsonify({'status': False, 'message': message}), 500
        return jsonify({'status': True, 'message': 'successfully created new membership plan',
                        'payload': plan_instance.to_dict()}), 200

    # noinspection DuplicatedCode
    @use_context
    @handle_view_errors
    def update_plan(self, organization_id: typing.Union[str, None], plan_id: str, plan_name: str, description: str,
                    schedule_day: int, schedule_term: str, term_payment: int, registration_amount: int,
                    currency: str, is_active: bool) -> tuple:

        if self.can_update_plan(organization_id=organization_id, plan_id=plan_id, plan_name=plan_name) is True:

            membership_plans_instance: MembershipPlans = MembershipPlans.query(
                MembershipPlans.organization_id == organization_id, MembershipPlans.plan_id == plan_id).get()

            if isinstance(membership_plans_instance, MembershipPlans):
                curr_term_payment: AmountMixin = AmountMixin(amount=term_payment, currency=currency)
                curr_registration_amount: AmountMixin = AmountMixin(amount=registration_amount,
                                                                    currency=currency)
                membership_plans_instance.plan_name = plan_name
                membership_plans_instance.description = description
                membership_plans_instance.schedule_day = schedule_day
                membership_plans_instance.schedule_term = schedule_term
                membership_plans_instance.term_payment_amount = curr_term_payment
                membership_plans_instance.registration_amount = curr_registration_amount
                membership_plans_instance.is_active = is_active

                key = membership_plans_instance.put(retries=self._max_retries, timeout=self._max_timeout)

                if not bool(key):
                    message: str = 'for some reason we are unable to create a new plan'
                    raise DataServiceError(status=error_codes.data_service_error_code, description=message)
                return jsonify({'status': True, 'message': 'successfully created new membership plan',
                                'payload': membership_plans_instance.to_dict()}), 200

            else:
                message: str = 'Membership plan not found'
                return jsonify({'status': False, 'message': message}), 500
        else:
            message: str = 'Conditions to update plan not satisfied'
            return jsonify({'status': False, 'message': message}), 500

    # noinspection DuplicatedCode
    @use_context
    @handle_view_errors
    async def update_plan_async(self, organization_id: typing.Union[str, None], plan_id: str, plan_name: str,
                                description: str, schedule_day: int, schedule_term: str, term_payment: int,
                                registration_amount: int, currency: str, is_active: bool) -> tuple:
        ***REMOVED***
                # TODO - synchronise the actions of this functions with PayPal MembershipPlans
                updates a membership plan
        :param organization_id:
        :param plan_id:
        :param plan_name:
        :param description:
        :param schedule_day:
        :param schedule_term:
        :param term_payment:
        :param registration_amount:
        :param currency:
        :param is_active:
        :return:
        ***REMOVED***

        if await self.can_update_plan_async(organization_id=organization_id, plan_id=plan_id,
                                            plan_name=plan_name) is True:
            membership_plans_instance: MembershipPlans = MembershipPlans.query(
                MembershipPlans.organization_id == organization_id,
                MembershipPlans.plan_id == plan_id).get_async().get_result()

            if isinstance(membership_plans_instance, MembershipPlans):
                curr_term_payment: AmountMixin = AmountMixin(amount=term_payment, currency=currency)
                curr_registration_amount: AmountMixin = AmountMixin(amount=registration_amount,
                                                                    currency=currency)
                membership_plans_instance.plan_name = plan_name
                membership_plans_instance.description = description
                membership_plans_instance.schedule_day = schedule_day
                membership_plans_instance.schedule_term = schedule_term
                membership_plans_instance.term_payment_amount = curr_term_payment
                membership_plans_instance.registration_amount = curr_registration_amount
                membership_plans_instance.is_active = is_active
                key = membership_plans_instance.put_async(
                    retries=self._max_retries, timeout=self._max_timeout).get_result()
                if not bool(key):
                    message: str = 'for some reason we are unable to create a new plan'
                    raise DataServiceError(status=error_codes.data_service_error_code, description=message)
                return jsonify({'status': True, 'message': 'successfully created new membership plan',
                                'payload': membership_plans_instance.to_dict()}), 200
            else:
                message: str = 'Membership plan not found'
                return jsonify({'status': False, 'message': message}), 500
        else:
            message: str = 'Conditions to update plan not satisfied'
            return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    def set_is_active(self, organization_id: typing.Union[str, None], plan_id: typing.Union[str, None],
                      is_active: bool) -> tuple:
        ***REMOVED***
            TODO- Synchronize the actions of this function with PayPal through the SDK
            activate or de-activate a membership plan
            :param organization_id:
            :param plan_id:
            :param is_active: bool indicating weather to activate or de-activate the membership plan.
            :return:
        ***REMOVED***

        membership_plans_instance: MembershipPlans = MembershipPlans.query(
            MembershipPlans.organization_id == organization_id, MembershipPlans.plan_id == plan_id).get()

        if isinstance(membership_plans_instance, MembershipPlans):
            membership_plans_instance.is_active = is_active
            key = membership_plans_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = 'for some reason we are unable to create a new plan'
                return jsonify({'status': False, 'message': message}), 500
            message: str = 'successfully update membership plan status'
            return jsonify({'status': True, 'message': message,
                            'payload': membership_plans_instance.to_dict()}), 200
        else:
            message: str = 'Membership plan not found'
            return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    async def set_is_active_async(self, organization_id: typing.Union[str, None], plan_id: typing.Union[str, None],
                                  is_active: bool) -> tuple:
        ***REMOVED***
            activate or de-activate a membership plan
            :param organization_id:
            :param plan_id:
            :param is_active: bool indicating weather to activate or de-activate the membership plan.
            :return:
        ***REMOVED***

        membership_plans_instance: MembershipPlans = MembershipPlans.query(
            MembershipPlans.organization_id == organization_id,
            MembershipPlans.plan_id == plan_id).get_async().get_result()

        if isinstance(membership_plans_instance, MembershipPlans):
            membership_plans_instance.is_active = is_active
            # TODO- this action has to be updated also in PayPal
            key = membership_plans_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
            if not bool(key):
                message: str = 'for some reason we are unable to create a new plan'
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
            return jsonify({'status': True, 'message': 'successfully update membership plan status',
                            'payload': membership_plans_instance.to_dict()}), 200
        else:
            message: str = 'Membership plan not found'
            return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def return_plans_by_schedule_term(self, organization_id: typing.Union[str, None], schedule_term: str) -> tuple:
        ***REMOVED***
            returns plan schedules - this is a payment schedule for the plan
        :param organization_id:
        :param schedule_term:
        :return:
        ***REMOVED***

        membership_plan_list: typing.List[MembershipPlans] = MembershipPlans.query(
            MembershipPlans.organization_id == organization_id, MembershipPlans.schedule_term == schedule_term).fetch()

        payload: typing.List[dict] = [membership.to_dict() for membership in membership_plan_list]
        return jsonify({'status': False, 'payload': payload,
                        'message': 'successfully retrieved monthly plans'}), 200

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def return_plans_by_schedule_term_async(self, organization_id: typing.Union[str, None],
                                                  schedule_term: str) -> tuple:
        ***REMOVED***
            returns plan schedules - this is a payment schedule for the plan
        :param organization_id:
        :param schedule_term:
        :return:
        ***REMOVED***

        membership_plan_list: typing.List[MembershipPlans] = MembershipPlans.query(
            MembershipPlans.organization_id == organization_id,
            MembershipPlans.schedule_term == schedule_term).fetch_async().get_result()

        payload: typing.List[dict] = [membership.to_dict() for membership in membership_plan_list]

        return jsonify({'status': False, 'payload': payload,
                        'message': 'successfully retrieved monthly plans'}), 200

    @staticmethod
    def get_plan(organization_id: str, plan_id: str) -> typing.Union[None, MembershipPlans]:
        ***REMOVED***
            this utility will be used by other views to obtain information about membershipPlans
        :param organization_id:
        :param plan_id:
        :return:
        ***REMOVED***
        if isinstance(plan_id, str):
            try:
                membership_plan_instance: MembershipPlans = MembershipPlans.query(
                    Memberships.organization_id == organization_id, MembershipPlans.plan_id == plan_id).get()

                if isinstance(membership_plan_instance, MembershipPlans):
                    return membership_plan_instance
                else:
                    return None
            except ConnectionRefusedError:
                return None
            except RetryError:
                return None
            except Aborted:
                return None
        return None

    @staticmethod
    async def get_plan_async(organization_id: str, plan_id: str) -> typing.Union[None, MembershipPlans]:
        ***REMOVED***
            this utility will be used by other views to obtain information about membershipPlans
        ***REMOVED***
        if isinstance(plan_id, str):
            try:
                membership_plan_instance: MembershipPlans = MembershipPlans.query(
                    MembershipPlans.organization_id == organization_id,
                    MembershipPlans.plan_id == plan_id).get_async().get_result()

                if isinstance(membership_plan_instance, MembershipPlans):
                    return membership_plan_instance
                else:
                    return None
            except ConnectionRefusedError:
                return None
            except RetryError:
                return None
            except Aborted:
                return None
        return None

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def return_plan(self, organization_id: str, plan_id: str) -> tuple:
        ***REMOVED***
            return a specific membership plan
        :param organization_id:
        :param plan_id: the id of the plan to return - Note: this plan id is the same as the plan id / product id in PayPal
        :return: plan details
        ***REMOVED***

        plan_instance = self.get_plan(organization_id=organization_id, plan_id=plan_id)
        if bool(plan_instance):
            message: str = "successfully fetched plan"
            return jsonify({'status': True, 'payload': plan_instance.to_dict(), 'message': message}), 200
        return jsonify({'status': False, 'message': 'Unable to get plan'}), 500

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def return_plan_async(self, organization_id: str, plan_id: str) -> tuple:
        ***REMOVED***
            return a specific membership plan
        :param organization_id:
        :param plan_id: the id of the plan to return - Note: this plan id is the same as the plan id / product id in PayPal
        :return: plan details
        ***REMOVED***

        plan_instance = await self.get_plan_async(organization_id=organization_id, plan_id=plan_id)
        if bool(plan_instance):
            message: str = "successfully fetched plan"
            return jsonify({'status': True, 'payload': plan_instance.to_dict(), 'message': message}), 200
        return jsonify({'status': False, 'message': 'Unable to get plan'}), 500

    @staticmethod
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def return_all_plans(organization_id: str) -> tuple:
        ***REMOVED***
            returns all memberships plans, Note that some more details on membership plans are located in PayPal
            :param organization_id:
            :return: memberships plans
        ***REMOVED***

        membership_plan_list: typing.List[MembershipPlans] = MembershipPlans.query(
            MembershipPlans.organization_id == organization_id).fetch()

        plan_list: typing.List[dict] = [plan.to_dict() for plan in membership_plan_list]
        return jsonify({'status': True, 'payload': plan_list,
                        'message': 'successfully fetched all memberships'}), 200

    @staticmethod
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def return_all_plans_async(organization_id: str) -> tuple:
        ***REMOVED***
            returns all memberships plans, Note that some more details on membership plans are located in PayPal
            :param organization_id:
            :return: memberships plans
        ***REMOVED***

        membership_plan_list: typing.List[MembershipPlans] = MembershipPlans.query(
            MembershipPlans.organization_id == organization_id).fetch_async().get_result()

        plan_list: typing.List[dict] = [plan.to_dict() for plan in membership_plan_list]
        return jsonify({'status': True, 'payload': plan_list,
                        'message': 'successfully fetched all memberships'}), 200


class AccessRightsView:
    ***REMOVED***
        manage the view for AccessRights
    ***REMOVED***

    def __init__(self):
        pass

    @use_context
    def get_access_rights(self, organization_id: str, plan_id: str) -> typing.Union[None, AccessRights]:
        if isinstance(plan_id, str):
            try:
                access_rights_instance: AccessRights = AccessRights.query(
                    AccessRights.organization_id == organization_id, AccessRights.plan_id == plan_id).get()

                if isinstance(access_rights_instance, AccessRights):
                    return access_rights_instance
                return None
            except ConnectionRefusedError:
                return None
            except RetryError:
                return None
            except Aborted:
                return None
        return None

    @use_context
    async def get_access_rights_async(self, organization_id: str, plan_id: str) -> typing.Union[None, AccessRights]:
        if isinstance(plan_id, str):
            try:
                access_rights_instance: AccessRights = AccessRights.query(
                    AccessRights.organization_id == organization_id,
                    AccessRights.plan_id == plan_id).get_async().get_result()

                if isinstance(access_rights_instance, AccessRights):
                    return access_rights_instance
                return None
            except ConnectionRefusedError:
                return None
            except RetryError:
                return None
            except Aborted:
                return None
        return None


# Coupon data wrapper
def get_coupon_data(func):
    ***REMOVED***
            data wrapper designed to gather coupon variables and checks for validity
        :param func: returns a function populated with the required variables otherwise returns an error indicating the
                    the problem
        :return: func
    ***REMOVED***

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        coupon_data: typing.Union[dict, None] = kwargs.get('coupon_data')
        if not bool(coupon_data):
            message: str = "Input is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        code: typing.Union[str, None] = coupon_data.get('code')
        if not bool(code):
            message: str = "coupon code is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        discount: typing.Union[int, None] = int(coupon_data.get('discount'))
        if not bool(discount):
            message: str = "discount is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        expiration_time: typing.Union[int, None] = int(coupon_data['expiration_time'])
        if not bool(expiration_time):
            message: str = "expiration_time is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_id: typing.Union[str, None] = coupon_data.get("organization_id")
        if not bool(organization_id):
            message: str = "Please specify organization_id"
            raise InputError(status=error_codes.input_error_code, description=message)

        return func(organization_id=organization_id, code=code, discount=discount, expiration_time=expiration_time,
                    *args)

    return wrapper


# noinspection DuplicatedCode
class CouponsView(Validators):
    ***REMOVED***
        manages the view instance for organization coupon codes..
    ***REMOVED***

    def __init__(self):
        super(CouponsView, self).__init__()

    @get_coupon_data
    @use_context
    @handle_view_errors
    def add_coupon(self, organization_id: typing.Union[str, None], code: typing.Union[str, None],
                   discount: typing.Union[int, None],
                   expiration_time: typing.Union[int, None]) -> tuple:
        ***REMOVED***
            creates new coupon
        :param organization_id: organization id of the org creating the coupon_instance
        :param code:  coupon code
        :param discount: discount amount in percent
        :param expiration_time: timestamp indicating the time the coupon will expire
        :return: newly minted coupon
        ***REMOVED***

        if self.can_add_coupon(organization_id=organization_id, code=code, expiration_time=expiration_time,
                               discount=discount) is True:

            coupons_instance: Coupons = Coupons(organization_id=organization_id, code=code, discount=discount,
                                                expiration_time=expiration_time)

            key = coupons_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "an error occured while creating coupon"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
        else:
            message: str = 'Unable to add coupon, please check expiration time or coupon code'
            return jsonify({'status': False, 'message': message}), 500
        return jsonify({'status': True, 'message': 'successfully created coupon code',
                        'payload': coupons_instance.to_dict()}), 200

    @get_coupon_data
    @use_context
    @handle_view_errors
    async def add_coupon_async(self, organization_id: typing.Union[str, None], code: typing.Union[str, None],
                               discount: typing.Union[int, None], expiration_time: typing.Union[int, None]) -> tuple:
        ***REMOVED***
            creates new coupon
        :param organization_id: organization id of the org creating the coupon_instance
        :param code:  coupon code
        :param discount: discount amount in percent
        :param expiration_time: timestamp indicating the time the coupon will expire
        :return: newly minted coupon
        ***REMOVED***

        if await self.can_add_coupon_async(organization_id=organization_id, code=code, expiration_time=expiration_time,
                                           discount=discount) is True:
            coupons_instance: Coupons = Coupons(organization_id=organization_id, code=code,
                                                discount=discount, expiration_time=expiration_time)

            key = coupons_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
            if not bool(key):
                message: str = "an error occured while creating coupon"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
        else:
            message: str = 'Unable to add coupon, please check expiration time or coupon code'
            return jsonify({'status': False, 'message': message}), 500
        return jsonify({'status': True, 'message': 'successfully created coupon code',
                        'payload': coupons_instance.to_dict()}), 200

    @get_coupon_data
    @use_context
    @handle_view_errors
    def update_coupon(self, organization_id: typing.Union[str, None], code: str, discount: int,
                      expiration_time: int) -> tuple:
        ***REMOVED***
            update coupons asynchronously
            :param organization_id:
            :param code: code relating to the coupon - this field must not be updated - used to locate coupon_instance
            :param discount: up-datable a percentage indicating how much of the original amount should be discountable
            :param expiration_time: up-datable value indicates the time the coupon code will expire
            :return:  updated coupon
        ***REMOVED***
        if self.can_update_coupon(code=code, expiration_time=expiration_time, discount=discount) is True:
            coupon_instance: Coupons = Coupons.query(Coupons.organization_id == organization_id,
                                                     Coupons.code == code).get()
            # Discounted amount in percent
            coupon_instance.discount_percent = discount
            # timestamp indicating the time the coupon will expire
            coupon_instance.expiration_time = expiration_time
            key = coupon_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "Error updating coupon"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            return jsonify({'status': True, 'message': 'successfully updated coupon'}), 200
        else:
            message: str = "Unable to update coupon code"
            return jsonify({'status': False, 'message': message}), 500

    @get_coupon_data
    @use_context
    @handle_view_errors
    async def update_coupon_async(self, organization_id: typing.Union[str, None], code: str, discount: int,
                                  expiration_time: int) -> tuple:
        ***REMOVED***
            update coupons asynchronously
            :param organization_id:
            :param code: code relating to the coupon - this field must not be updated - used to locate coupon_instance
            :param discount: up-datable a percentage indicating how much of the original amount should be discountable
            :param expiration_time: up-datable value for coupons
            :return:  updated coupon
        ***REMOVED***
        if await self.can_update_coupon_async(organization_id=organization_id, code=code,
                                              expiration_time=expiration_time, discount=discount) is True:

            coupon_instance: Coupons = Coupons.query(
                Coupons.organization_id == organization_id, Coupons.code == code).get_async().get_result()

            # Discount a percentage indicating how much of the original price should be knocked off
            coupon_instance.discount_percent = discount
            coupon_instance.expiration_time = expiration_time
            key = coupon_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
            if not bool(key):
                message: str = "Error updating coupon"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            return jsonify({'status': True, 'message': 'successfully updated coupon'}), 200
        else:
            message: str = "Unable to update coupon code"
            return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    def cancel_coupon(self, coupon_data: dict) -> tuple:
        ***REMOVED***
            cancels coupon code require organization_id and coupon_data
        :param coupon_data: contains coupon code and organization_id
        :return: cancelled coupon code
        ***REMOVED***
        code: typing.Union[str, None] = coupon_data.get("code")
        organization_id: typing.Union[str, None] = coupon_data.get('organization_id')
        if not bool(code):
            return jsonify({'status': False, 'message': 'coupon is required'}), 500
        if not bool(organization_id):
            return jsonify({'status': False, 'message': 'organization id is required'}), 500

        coupon_instance: Coupons = Coupons.query(Coupons.organization_id == organization_id,
                                                 Coupons.code == code).get()

        if isinstance(coupon_instance, Coupons):
            coupon_instance.is_valid = False
            key = coupon_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "Unable to cancel coupon"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
            return jsonify({'status': True, 'message': 'successfully cancelled coupon code'}), 200

        return jsonify({'status': False, 'message': 'unable to cancel coupon code'}), 500

    @use_context
    @handle_view_errors
    async def cancel_coupon_async(self, coupon_data: dict) -> tuple:
        ***REMOVED***
            cancels coupon code
        :param coupon_data: contains coupon code and organization_id
        :return:
        ***REMOVED***
        code: typing.Union[str, None] = coupon_data.get("code")
        organization_id: typing.Union[str, None] = coupon_data.get('organization_id')
        if not bool(code):
            return jsonify({'status': False, 'message': 'coupon code is required'}), 500
        if not bool(organization_id):
            return jsonify({'status': False, 'message': 'organization_id is required'}), 500

        coupon_instance: Coupons = Coupons.query(Coupons.organization_id == organization_id,
                                                 Coupons.code == code).get_async().get_result()

        if isinstance(coupon_instance, Coupons):
            coupon_instance.is_valid = False
            key = coupon_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
            if not bool(key):
                message: str = "Unable to cancel coupon"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
            return jsonify({'status': True, 'message': 'successfully cancelled coupon code'}), 200

        return jsonify({'status': False, 'message': 'unable to cancel coupon code'}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_all_coupons(self, organization_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            returns a list of all coupons
        :param organization_id:
        :return:
        ***REMOVED***

        coupons_list: typing.List[Coupons] = Coupons.query(Coupons.organization_id == organization_id).fetch()

        payload: typing.List[dict] = [coupon.to_dict() for coupon in coupons_list]
        message: str = "coupons successfully created"
        return jsonify({'status': True, 'payload': payload, 'message': message}), 200

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def get_all_coupons_async(self, organization_id: typing.Union[str, None]) -> tuple:
        coupons_list: typing.List[Coupons] = Coupons.query(
            Coupons.organization_id == organization_id).fetch_async().get_result()

        payload: typing.List[dict] = [coupon.to_dict() for coupon in coupons_list]
        message: str = "coupons successfully created"
        return jsonify({'status': True, 'payload': payload, 'message': message}), 200

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_valid_coupons(self, organization_id: typing.Union[str, None]) -> tuple:

        coupons_list: typing.List[Coupons] = Coupons.query(
            Coupons.organization_id == organization_id, Coupons.is_valid == True).fetch()

        payload: typing.List[dict] = [coupon.to_dict() for coupon in coupons_list]
        message: str = "coupons successfully created"
        return jsonify({'status': True, 'payload': payload, 'message': message}), 200

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def get_valid_coupons_async(self, organization_id: typing.Union[str, None]) -> tuple:
        coupons_list: typing.List[Coupons] = Coupons.query(Coupons.organization_id == organization_id,
                                                           Coupons.is_valid == True).fetch_async().get_result()

        payload: typing.List[dict] = [coupon.to_dict() for coupon in coupons_list]
        message: str = "coupons successfully created"
        return jsonify({'status': True, 'payload': payload, 'message': message}), 200

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_expired_coupons(self, organization_id: typing.Union[str, None]) -> tuple:
        coupons_list: typing.List[Coupons] = Coupons.query(Coupons.organization_id == organization_id,
                                                           Coupons.expiration_time < timestamp()).fetch()

        payload: typing.List[dict] = [coupon.to_dict() for coupon in coupons_list]
        message: str = "coupons successfully created"
        return jsonify({'status': True, 'payload': payload, 'message': message}), 200

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def get_expired_coupons_async(self, organization_id: typing.Union[str, None]) -> tuple:
        coupons_list: typing.List[Coupons] = Coupons.query(
            Coupons.organization_id == organization_id,
            Coupons.expiration_time < timestamp()).fetch_async().get_result()

        payload: typing.List[dict] = [coupon.to_dict() for coupon in coupons_list]
        message: str = "coupons successfully created"
        return jsonify({'status': True, 'payload': payload, 'message': message}), 200

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_coupon(self, coupon_data: dict) -> tuple:
        code: typing.Union[str, None] = coupon_data.get("code")
        if not bool(code):
            return jsonify({'status': False, 'message': 'coupon is required'}), 500
        organization_id: typing.Union[str, None] = coupon_data.get('organization_id')
        if not bool(organization_id):
            return jsonify({'status': False, 'message': 'organization_id is required'}), 500

        coupon_instance: Coupons = Coupons.query(Coupons.organization_id == organization_id,
                                                 Coupons.code == code).get()

        if isinstance(coupon_instance, Coupons):
            message: str = "Coupon has been found"
            return jsonify({'status': True, 'message': message, 'payload': coupon_instance.to_dict()}), 200

        message: str = "Invalid Coupon Code"
        return jsonify({'status': True, 'message': message}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def get_coupon_async(self, coupon_data: dict) -> tuple:
        code: typing.Union[str, None] = coupon_data.get("code")
        if not bool(code):
            return jsonify({'status': False, 'message': 'coupon is required'}), 500
        organization_id: typing.Union[str, None] = coupon_data.get('organization_id')
        if not bool(organization_id):
            return jsonify({'status': False, 'message': 'organization_id is required'}), 500

        coupon_instance: Coupons = Coupons.query(Coupons.organization_id == organization_id,
                                                 Coupons.code == code).get_async().get_result()

        if isinstance(coupon_instance, Coupons):
            message: str = "Coupon has been found"
            return jsonify({'status': True, 'message': message, 'payload': coupon_instance.to_dict()}), 200
        message: str = "Invalid Coupon Code"
        return jsonify({'status': True, 'message': message}), 500

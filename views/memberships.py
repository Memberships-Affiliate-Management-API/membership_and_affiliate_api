***REMOVED***
    ** Module - Memberships View Controller**
    * Class Definitions for controlling access and presenting data to and from Memberships related classes *
***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import functools
from typing import Optional, List
from google.api_core.exceptions import RetryError, Aborted
from flask import jsonify, current_app
from datetime import datetime, date, timedelta
from google.cloud import ndb

from _cron.scheduler import schedule
from config.exceptions import (DataServiceError, InputError, error_codes, status_codes,
                               UnAuthenticatedError, RequestError, RemoteDataError)
from database.memberships import MembershipPlans, AccessRights, Memberships, Coupons
from database.memberships import PlanValidators as PlanValid
from database.mixins import AmountMixin
from database.users import UserValidators as UserValid
from database.memberships import MembershipValidators as MemberValid
from database.memberships import CouponsValidator as CouponValid
from utils.utils import return_ttl, timestamp, get_payment_methods, datetime_now, create_id
from main import app_cache
from config.exception_handlers import handle_view_errors, handle_store_errors
from config.use_context import use_context
from _sdk._email import Mailgun
import asyncio


class MembershipsEmails(Mailgun):
    ***REMOVED***
        **Class MembershipsEmails**
            Class Used to send emails and notifications related to Memberships

    ***REMOVED***

    def __init__(self):
        super(MembershipsEmails, self).__init__()

    @staticmethod
    def welcome_email_body_composer(_names: str, _surname: str, _plan_name: str, _plan_description: str,
                                    _organization_name: str,
                                    _organization_description: str) -> tuple:
        # Include Powered by Message on the Footer of the Email Message
        ***REMOVED***
            **Email body Composer**
                compose the two email bodies given the above variables

        :param _names:
        :param _surname:
        :param _plan_name:
        :param _plan_description:
        :param _organization_name:
        :param _organization_description:
        :return:
        ***REMOVED***
        # TODO find a way to format the email body wonderfully
        _text_body = f'''
            Hi {_names} {_surname}

            Welcome to : {_organization_name}

            You have recently subscribe to : {_plan_name}
            {_plan_description}

            Thank you
            {_organization_name}

        '''
        _html_body = f'''
            Hi {_names} {_surname}

            Welcome to : {_organization_name}

            You have recently subscribe to : {_plan_name}
            {_plan_description}

            Thank you
            {_organization_name}

        '''
        return _text_body, _html_body

    @staticmethod
    def _get_requests_results(results) -> tuple:
        ***REMOVED***
            **_get_requests_results**
                obtains results
        :param results:
        :return: tuple containing results
        ***REMOVED***
        if not isinstance(results, tuple):
            message: str = "Remote data error: Unable to obtain data"
            raise RemoteDataError(status=error_codes.remote_data_error, description=message)

        user_data: Optional[dict] = results[0].result()
        membership_data: Optional[dict] = results[1].result()
        organization_data: Optional[dict] = results[2].result()
        return membership_data, organization_data, user_data

    def send_memberships_welcome_email(self, organization_id: str, uid: str) -> None:
        ***REMOVED***
            **send_memberships_welcome_email**
                ideally this process should be run on a separate work instance if on Heroku or as a task in GCP**
                once a client or user has registered to a membership plan send them an email welcoming them
                on board

            :param organization_id
            :param uid
            :return:
        ***REMOVED***
        # TODO find out how to create templates and allow clients to create their email templates
        loop = asyncio.get_event_loop()

        data_tasks = asyncio.gather(self.__get_user_data_async(organization_id=organization_id, uid=uid),
                                    self.__get_membership_data_async(organization_id=organization_id, uid=uid),
                                    self.__get_organization_data_async(organization_id=organization_id))

        results = loop.run_until_complete(data_tasks)
        membership_data, organization_data, user_data = self._get_requests_results(results)
        loop.close()

        email: str = user_data.get('email')
        names: str = user_data.get('names', " ")
        surname: str = user_data.get('surname', " ")
        plan_name: str = membership_data.get('plan_name')
        plan_description: str = membership_data.get('description')
        organization_name: str = organization_data.get('organization_name')
        description: str = organization_data.get('description')

        # Note: composes and returns email body given membership and organization details the member joined
        text_body, html_body = self.welcome_email_body_composer(_names=names, _surname=surname, _plan_name=plan_name,
                                                                _plan_description=plan_description,
                                                                _organization_name=organization_name,
                                                                _organization_description=description)

        subject: str = 'Welcome to : {}'.format(organization_name)
        email_verified: bool = user_data.get('email_verified')
        if email_verified and bool(email):
            self.__do_schedule_mail(to_email=email, subject=subject, text=text_body, html=html_body)

        message: str = "Bad Request Error: Email not verified please verify your account"
        raise RequestError(status=error_codes.bad_request_error_code, description=message)

    def send_change_of_membership_notification_email(self, organization_id: str, uid: str) -> None:
        ***REMOVED***
            **send_change_of_membership_notification_email**
                once a user membership plan details changes send a notification to the client with the details

            :param: organization_id
            :param: uid
            :return:
        ***REMOVED***
        # TODO find out how to create templates and allow clients to create their email templates
        user_data, organization_data = self.return_organization_user(organization_id=organization_id, uid=uid)
        membership_data: dict = asyncio.run(self.__get_membership_data_async(organization_id=organization_id, uid=uid))

        email_verified: bool = user_data.get('email_verified')
        subject: str = f"{organization_data.get('organization_name')} Your Membership Details have changed"

        text: str = f'''
        Hi {user_data.get('names', " ")} {user_data.get('surname', " ")}
        
        Your Subscription details have changed: 
        
            Subscription Name: {membership_data.get('plan_name')}
            Registration Amount: {membership_data.get('registration_amount')}
            Payment Schedule: {membership_data.get('schedule_term')}
            Scheduled Amount: {membership_data.get('term_payment_amount')}
         
        Thank you
        {organization_data.get('organization_name')}        
        
        '''

        html: str = f'''
        <h3>Hi {user_data.get('names', " ")} {user_data.get('surname', " ")}</h3>
        
        <h3>Your Subscription details have changed</h3> 
        
        <ol>
            <li>Subscription Name: {membership_data.get('plan_name')}</li>
            <li>Registration Amount: {membership_data.get('registration_amount')}</li>
            <li>Payment Schedule: {membership_data.get('schedule_term')}</li>
            <li>Scheduled Amount: {membership_data.get('term_payment_amount')}</li>
        </ol>
         
        <h4>Thank you </h4>
        <strong>{organization_data.get('organization_name')}</strong>        
        '''
        email: str = user_data.get('email')
        if email_verified and bool(email):
            self.__do_schedule_mail(to_email=email, subject=subject, text=text, html=html)

        message: str = "Bad Request Error: Email not verified please verify your account"
        raise RequestError(status=error_codes.bad_request_error_code, description=message)

    def send_payment_method_changed_email(self, organization_id: str, uid: str,
                                          membership_instance: Memberships) -> None:
        ***REMOVED***
            **send_payment_method_changed_email**
                send an email notifying the user that their payment method changed
                TODO - call user api to fetch user details
                TODO - with user details compile the payment changed email and send

            :param membership_instance:
            :param organization_id : required
            :param uid: required
            :return:
        ***REMOVED***
        # TODO find out how to create templates and allow clients to create their email templates
        user_data, organization_data = self.return_organization_user(organization_id=organization_id, uid=uid)
        email_verified: bool = user_data.get('email_verified')
        subject: str = f"From: {organization_data.get('organization_name')} Your Payment Method has changed"

        text: str = f'''
        hi {user_data.get('names', " ")} {user_data.get('surname', " ")}
        
        Payment Method Changed Notification from : {organization_data.get('organization_name')}
        
        Your Present Payment Method is : {membership_instance.payment_method}
        
        Thank You
            {organization_data.get('organization_name')}
            Website: {organization_data.get('home_url')}        
        '''
        html: str = f'''
        <h3>Hi {user_data.get('names', " ")} {user_data.get('surname', " ")}</h3>
        
        <p>Payment Method Changed Notification from : {organization_data.get('organization_name')}</p>
        
        <h4>Your Present Payment Method is : {membership_instance.payment_method}</h4>
        
        <h3>Thank You</h3>
            <p>{organization_data.get('organization_name')}</p>
            <p>Website: {organization_data.get('home_url')}</p>                
        '''
        email: str = user_data.get('email')
        if email_verified and bool(email):
            self.__do_schedule_mail(to_email=email, subject=subject, text=text, html=html)

        message: str = "Bad Request Error: Email not verified please verify your account"
        raise RequestError(status=error_codes.bad_request_error_code, description=message)


# TODO Create Test Cases for Memberships & Documentations
class Validators(UserValid, PlanValid, MemberValid, CouponValid):
    ***REMOVED***
        **Class Validators**
            a group of validators for membership views
    ***REMOVED***

    def __init__(self):
        super(Validators, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @app_cache.memoize(timeout=return_ttl('short'))
    def can_add_member(self, organization_id: Optional[str], uid: Optional[str],
                       plan_id: Optional[str], start_date: date) -> bool:
        ***REMOVED***
            **can_add_member**
                checks if user can add a member to memberships record
        :param organization_id:
        :param uid:
        :param plan_id:
        :param start_date:
        :return:
        ***REMOVED***
        user_valid: Optional[bool] = self.is_user_valid(organization_id=organization_id, uid=uid)
        # TODO - may need to revise this, there is no reason to check if a plan_exist - just if a membership exist
        plan_exist: Optional[bool] = self.plan_exist(organization_id=organization_id, plan_id=plan_id)
        date_valid: Optional[bool] = self.start_date_valid(start_date=start_date)

        if isinstance(user_valid, bool) and isinstance(plan_exist, bool) and isinstance(date_valid, bool):
            return user_valid and not plan_exist and date_valid

        message: str = "Unable to verify input data, due to database error, please try again later"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'))
    async def can_add_member_async(self, organization_id: Optional[str], uid: Optional[str],
                                   plan_id: Optional[str],
                                   start_date: date) -> bool:
        ***REMOVED***
            **can_add_member_async**
                asynchronous version of can_add_member

            **PARAMETERS**
                :param organization_id:
                :param uid:
                :param plan_id:
                :param start_date:
                :return: boolean -> indicating if member can be added or not
        ***REMOVED***
        user_valid: Optional[bool] = await self.is_user_valid_async(organization_id=organization_id, uid=uid)
        plan_exist: Optional[bool] = await self.plan_exist_async(organization_id=organization_id,
                                                                 plan_id=plan_id)
        date_valid: Optional[bool] = await self.start_date_valid_async(start_date=start_date)

        if isinstance(user_valid, bool) and isinstance(plan_exist, bool) and isinstance(date_valid, bool):
            return user_valid and not plan_exist and date_valid

        message: str = "Unable to verify input data, due to database error, please try again later"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'))
    def can_add_plan(self, organization_id: Optional[str], plan_name: Optional[str]) -> bool:
        ***REMOVED***
            **can_add_plan**
                check if a new plan can be added

            **PARAMETERS**
                :param organization_id:
                :param plan_name:
                :return: boolean -> indicating if plan can be added or not
        ***REMOVED***
        name_exist: Optional[bool] = self.plan_name_exist(organization_id=organization_id,
                                                          plan_name=plan_name)
        if isinstance(name_exist, bool):
            return not name_exist
        message: str = "Database Error: Unable to verify input data, please try again later"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'))
    async def can_add_plan_async(self, organization_id: Optional[str],
                                 plan_name: Optional[str]) -> bool:
        ***REMOVED***
            **can_add_plan_async**
                checks if user can add plan

        **PARAMETERS**
            :param organization_id:
            :param plan_name:
            :return: boolean -> user can add plan or not
        ***REMOVED***
        name_exist: Optional[bool] = await self.plan_name_exist_async(
            organization_id=organization_id, plan_name=plan_name)

        if isinstance(name_exist, bool):
            return not name_exist
        message: str = "Database Error: Unable to verify input data, please try again later"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'))
    def can_update_plan(self, organization_id: Optional[str],
                        plan_id: Optional[str], plan_name: Optional[str]) -> bool:
        ***REMOVED***
            **can_update_plan**
                checks if plan can be updated

        :param organization_id:
        :param plan_id:
        :param plan_name:
        :return:
        ***REMOVED***
        plan_exist: Optional[bool] = self.plan_exist(organization_id=organization_id, plan_id=plan_id)
        # TODO - verify if checking of plan_name_exist is really needed
        plan_name_exist: Optional[bool] = self.plan_name_exist(
            organization_id=organization_id, plan_name=plan_name)

        if isinstance(plan_exist, bool) and isinstance(plan_name_exist, bool):
            return plan_exist and plan_name_exist
        message: str = "Database Error: Unable to verify input data, please try again later"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'))
    async def can_update_plan_async(self, organization_id: Optional[str],
                                    plan_id: Optional[str], plan_name: Optional[str]) -> bool:
        ***REMOVED***
            **can_update_plan_async**
                check if plan can be updated

        :param organization_id:
        :param plan_id:
        :param plan_name:
        :return:
        ***REMOVED***

        plan_exist: Optional[bool] = await self.plan_exist_async(
            organization_id=organization_id, plan_id=plan_id)

        plan_name_exist: Optional[bool] = await self.plan_name_exist_async(
            organization_id=organization_id, plan_name=plan_name)

        if isinstance(plan_exist, bool) and isinstance(plan_name_exist, bool):
            return plan_exist and plan_name_exist
        message: str = "Unable to verify input data, due to database error, please try again later"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'))
    def can_add_coupon(self, organization_id: Optional[str], code: Optional[str],
                       expiration_time: Optional[int],
                       discount: Optional[int]) -> bool:
        ***REMOVED***
            **can_add_coupon**
                check if coupon can be updated

        :param organization_id:
        :param code:
        :param expiration_time:
        :param discount:
        :return:
        ***REMOVED***

        coupon_exist: Optional[bool] = self.coupon_exist(organization_id=organization_id, code=code)
        expiration_valid: Optional[bool] = self.expiration_valid(expiration_time=expiration_time)
        discount_valid: Optional[bool] = self.discount_valid(discount_valid=discount)

        if isinstance(coupon_exist, bool) and isinstance(expiration_valid, bool) and isinstance(discount_valid, bool):
            return (not coupon_exist) and expiration_valid and discount_valid
        message: str = "Unable to verify input data"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'))
    async def can_add_coupon_async(self, organization_id: Optional[str], code: Optional[str],
                                   expiration_time: Optional[int],
                                   discount: Optional[int]) -> bool:
        ***REMOVED***
            **can_add_coupon_async**
                check if coupon can be added

        :param organization_id:
        :param code:
        :param expiration_time:
        :param discount:
        :return:
        ***REMOVED***
        coupon_exist: Optional[bool] = await self.coupon_exist_async(organization_id=organization_id,
                                                                     code=code)

        expiration_valid: Optional[bool] = await self.expiration_valid_async(expiration_time=expiration_time)
        discount_valid: Optional[bool] = await self.discount_valid_async(discount_valid=discount)

        if isinstance(coupon_exist, bool) and isinstance(expiration_valid, bool) and isinstance(discount_valid, bool):
            return (not coupon_exist) and expiration_valid and discount_valid
        message: str = "Unable to verify input data"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'))
    def can_update_coupon(self, organization_id: Optional[str], code: Optional[str],
                          expiration_time: Optional[int],
                          discount: Optional[int]) -> bool:
        ***REMOVED***
            **can_update_coupon**
                check if coupon can be updated

        :param organization_id:
        :param code:
        :param expiration_time:
        :param discount:
        :return:
        ***REMOVED***

        coupon_exist: Optional[bool] = self.coupon_exist(organization_id=organization_id, code=code)
        expiration_valid: Optional[bool] = self.expiration_valid(expiration_time=expiration_time)
        discount_valid: Optional[bool] = self.discount_valid(discount_valid=discount)

        if isinstance(coupon_exist, bool) and isinstance(expiration_valid, bool) and isinstance(discount_valid, bool):
            return coupon_exist and expiration_valid and discount_valid
        message: str = "Unable to verify input data"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'))
    async def can_update_coupon_async(self, organization_id: Optional[str], code: Optional[str],
                                      expiration_time: Optional[int],
                                      discount: Optional[int]) -> bool:
        ***REMOVED***
            **can_update_coupon_async**
                check if coupon can be updated

        :param organization_id:
        :param code:
        :param expiration_time:
        :param discount:
        :return:
        ***REMOVED***

        coupon_exist: Optional[bool] = await self.coupon_exist_async(organization_id=organization_id,
                                                                     code=code)
        expiration_valid: Optional[bool] = await self.expiration_valid_async(expiration_time=expiration_time)
        discount_valid: Optional[bool] = await self.discount_valid_async(discount_valid=discount)

        if isinstance(coupon_exist, bool) and isinstance(expiration_valid, bool) and isinstance(discount_valid, bool):
            return coupon_exist and expiration_valid and discount_valid
        message: str = "Unable to verify input data - could be due to database access errors - contact your admin"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)


# noinspection DuplicatedCode
class MembershipsView(Validators, MembershipsEmails):
    ***REMOVED***
        **MembershipsView**
            class intended to control access to memberships
    ***REMOVED***

    def __init__(self):
        super(MembershipsView, self).__init__()

    @use_context
    @handle_view_errors
    def _create_or_update_membership(self, organization_id: Optional[str], uid: Optional[str],
                                     plan_id: Optional[str], plan_start_date: date,
                                     payment_method: Optional[str] = "paypal") -> tuple:
        ***REMOVED***
            **_create_or_update_membership**
                this merely creates a relationship between a payment plan for a service or product to a client

        :param organization_id: id of the organization the client belongs to
        :param uid: id of the client who is getting into a payment plan
        :param plan_id: id the payment plan the client is joining
        :param plan_start_date: the date the plan will commence sometimes not the same as the date of creation

        :return:
        ***REMOVED***

        if self.can_add_member(organization_id=organization_id, uid=uid, plan_id=plan_id, start_date=plan_start_date):

            membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                                 Memberships.uid == uid).get()
            new_member: bool = False
            if not (isinstance(membership_instance, Memberships)):
                membership_instance: Memberships = Memberships()
                membership_instance.uid = uid
                membership_instance.organization_id = organization_id
                new_member = True

            membership_instance.payment_status = 'unpaid'
            membership_instance.plan_start_date = plan_start_date
            membership_instance.plan_id = plan_id
            membership_instance.payment_method = payment_method
            key: Optional[ndb.Key] = membership_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "Database Error: Unable to save membership instance to database, please try again"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            if new_member:
                # Note only sending welcome emails for new members
                self.send_memberships_welcome_email(organization_id=organization_id, uid=uid)

            return jsonify({'status': True, 'message': 'successfully subscribed to membership',
                            'payload': membership_instance.to_dict()}), status_codes.successfully_updated_code

        message: str = ***REMOVED***User Un-Authorized: You cannot perform this action consider contacting your admin***REMOVED***
        raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

    @use_context
    @handle_view_errors
    async def _create_or_update_membership_async(self, organization_id: Optional[str],
                                                 uid: Optional[str], plan_id: Optional[str],
                                                 plan_start_date: date,
                                                 payment_method: Optional[str] = "paypal") -> tuple:
        ***REMOVED***
            **_create_or_update_membership_async**
                this merely creates a relationship between a payment plan for a service or product to a client

        :param organization_id: id of the organization the client belongs to
        :param uid: id of the client who is getting into a payment plan
        :param plan_id: id the payment plan the client is joining
        :param plan_start_date: the date the plan will commence sometimes not the same as the date of creation
        :return:
        ***REMOVED***

        if await self.can_add_member_async(organization_id=organization_id, uid=uid, plan_id=plan_id,
                                           start_date=plan_start_date):
            # can use get to simplify this and make transactions faster
            membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                                 Memberships.uid == uid).get_async().get_result()

            if not (isinstance(membership_instance, Memberships)):
                membership_instance: Memberships = Memberships()

                membership_instance.uid = uid
                membership_instance.organization_id = organization_id

            membership_instance.payment_status = 'unpaid'
            membership_instance.plan_id = plan_id
            membership_instance.plan_start_date = plan_start_date
            membership_instance.payment_method = payment_method
            key: Optional[ndb.Key] = membership_instance.put_async(retries=self._max_retries,
                                                                   timeout=self._max_timeout).get_result()
            if not bool(key):
                message: str = "Unable to save membership instance to database, please try again"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
            return jsonify({'status': True, 'message': 'successfully updated membership',
                            'payload': membership_instance.to_dict()}), status_codes.status_ok_code

        message: str = ***REMOVED***Operation Denied: unable to create or update membership***REMOVED***
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    def add_membership(self, organization_id: Optional[str], uid: Optional[str],
                       plan_id: Optional[str], plan_start_date: date,
                       payment_method: Optional[str] = "paypal") -> tuple:
        ***REMOVED***

            **add_membership**
                add new membership

        :param organization_id:
        :param uid:
        :param plan_id:
        :param plan_start_date:
        :param payment_method:
        :return:
        ***REMOVED***

        # TODO - some form of error checking must be conducted here
        return self._create_or_update_membership(organization_id=organization_id, uid=uid, plan_id=plan_id,
                                                 plan_start_date=plan_start_date, payment_method=payment_method)

    async def add_membership_async(self, organization_id: Optional[str], uid: Optional[str],
                                   plan_id: Optional[str], plan_start_date: date,
                                   payment_method: Optional[str]) -> tuple:
        ***REMOVED***
            **add_membership_async**
                create new membership_instance

        :param organization_id:
        :param uid:
        :param plan_id:
        :param plan_start_date:
        :param payment_method:
        :return:
        ***REMOVED***

        return await self._create_or_update_membership_async(organization_id=organization_id, uid=uid,
                                                             plan_id=plan_id, plan_start_date=plan_start_date,
                                                             payment_method=payment_method)

    def update_membership(self, organization_id: Optional[str], uid: Optional[str],
                          plan_id: Optional[str], plan_start_date: date,
                          payment_method: Optional[str] = "paypal") -> tuple:
        ***REMOVED***
            **update_membership**
                update membership

        :param organization_id:
        :param uid:
        :param plan_id:
        :param plan_start_date:
        :param payment_method:
        :return:
        ***REMOVED***

        return self._create_or_update_membership(organization_id=organization_id, uid=uid, plan_id=plan_id,
                                                 plan_start_date=plan_start_date, payment_method=payment_method)

    async def update_membership_async(self, organization_id: Optional[str], uid: Optional[str],
                                      plan_id: Optional[str], plan_start_date: date,
                                      payment_method: Optional[str] = "paypal") -> tuple:
        ***REMOVED***
            **update_membership_async**
                update membership

        :param organization_id:
        :param uid:
        :param plan_id:
        :param plan_start_date:
        :param payment_method:
        :return:
        ***REMOVED***

        return await self._create_or_update_membership_async(organization_id=organization_id, uid=uid, plan_id=plan_id,
                                                             plan_start_date=plan_start_date,
                                                             payment_method=payment_method)

    @use_context
    @handle_view_errors
    def set_membership_payment_status(self, organization_id: Optional[str], uid: Optional[str],
                                      status: Optional[str]) -> tuple:
        ***REMOVED***
            **set_membership_status**
                set membership status

            :param organization_id:
            :param uid:
            :param status: the membership status to set - note if this is not a valid status the database
            setter / validator will catch the error
            :return:
        ***REMOVED***

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "Organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(status, str) or not bool(status.strip()):
            message: str = "status is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                             Memberships.uid == uid).get()

        if isinstance(membership_instance, Memberships):
            membership_instance.payment_status = status
            key: Optional[ndb.Key] = membership_instance.put(retries=self._max_retries, timeout=self._max_timeout)

            if not bool(key):
                message: str = "Unable to save membership instance to database, please try again"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            message: str = "Successfully update membership status"
            return jsonify({'status': True, 'payload': membership_instance.to_dict(),
                            'message': message}), status_codes.status_ok_code

        message: str = "Memberships record not found"
        return jsonify({'status': True, 'payload': membership_instance.to_dict(),
                        'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    async def set_membership_status_async(self, organization_id: Optional[str], uid: Optional[str],
                                          status: Optional[str]) -> tuple:
        ***REMOVED***
            **set_membership_status_async**
                an asynchronous version of set_membership_status

        :param organization_id:
        :param uid:
        :param status:
        :return:
        ***REMOVED***

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "Organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(status, str) or not bool(status.strip()):
            message: str = "status is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                             Memberships.uid == uid).get_async().get_result()

        if isinstance(membership_instance, Memberships):
            membership_instance.payment_status = status
            key: Optional[ndb.Key] = membership_instance.put_async(retries=self._max_retries,
                                                                   timeout=self._max_timeout).get_result()
            if not bool(key):
                message: str = "Unable to save membership instance to database, please try again"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
            message: str = "Successfully update membership status"
            return jsonify({'status': True, 'payload': membership_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code
        message: str = "Memberships record not found"
        return jsonify({'status': True, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def change_membership(self, organization_id: Optional[str], uid: Optional[str], origin_plan_id: Optional[str],
                          dest_plan_id: str) -> tuple:
        ***REMOVED***
            **change_membership**
                change Memberships

            :param organization_id:
            :param uid:
            :param origin_plan_id:
            :param dest_plan_id:
            :return:
        ***REMOVED***
        # TODO sync this with paypal payment plans - or maybe this will occur after the changes have taken place
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "user id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(origin_plan_id, str) or not bool(origin_plan_id.strip()):
            message: str = "origin_plan_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(dest_plan_id, str) or not bool(dest_plan_id.strip()):
            message: str = "dest_plan_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                             Memberships.uid == uid).get()

        if isinstance(membership_instance, Memberships) and (membership_instance.plan_id == origin_plan_id):

            if self.plan_exist(organization_id=organization_id, plan_id=dest_plan_id) is True:
                membership_instance.plan_id = dest_plan_id
                key: Optional[ndb.Key] = membership_instance.put(retries=self._max_retries,
                                                                 timeout=self._max_timeout)
            else:
                # This maybe be because the original plan is deleted but its a rare case
                membership_instance.plan_id = dest_plan_id
                key: Optional[ndb.Key] = membership_instance.put(retries=self._max_retries,
                                                                 timeout=self._max_timeout)
            if not bool(key):
                message: str = "Unable to Change Membership, please try again later"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            self.send_change_of_membership_notification_email(organization_id=organization_id, uid=uid)

            return jsonify({'status': True, 'message': 'successfully updated membership',
                            'payload': membership_instance.to_dict()}), status_codes.successfully_updated_code

        message: str = "Unable to change membership, cannot find original membership record"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    async def change_membership_async(self, organization_id: Optional[str], uid: Optional[str],
                                      origin_plan_id: Optional[str], dest_plan_id: str) -> tuple:

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "user id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(origin_plan_id, str) or not bool(origin_plan_id.strip()):
            message: str = "origin_plan_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(dest_plan_id, str) or not bool(dest_plan_id.strip()):
            message: str = "dest_plan_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                             Memberships.uid == uid).get_async().get_result()

        if isinstance(membership_instance, Memberships) and (membership_instance.plan_id == origin_plan_id):
            if await self.plan_exist_async(organization_id=organization_id, plan_id=dest_plan_id) is True:
                membership_instance.plan_id = dest_plan_id
                key: Optional[ndb.Key] = membership_instance.put_async(retries=self._max_retries,
                                                                       timeout=self._max_timeout).get_result()
            else:
                # This maybe be because the original plan is deleted but its a rare case
                membership_instance.plan_id = dest_plan_id
                key: Optional[ndb.Key] = membership_instance.put_async(retries=self._max_retries,
                                                                       timeout=self._max_timeout).get_result()

            if not (bool(key)):
                message: str = "Database Error: Unable to update Membership, please try again later"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            self.send_change_of_membership_notification_email(organization_id=organization_id, uid=uid)

            return jsonify({'status': True, 'message': 'successfully updated membership',
                            'payload': membership_instance.to_dict()}), status_codes.successfully_updated_code

        message: str = "Data Not Found: Unable to update membership"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def set_payment_method(self, organization_id: Optional[str], uid: Optional[str],
                           payment_method: Optional[str] = "paypal") -> tuple:
        ***REMOVED***
            **set_payment_method**
                default is payment method is paypal

        :param organization_id:
        :param uid:
        :param payment_method:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)
        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(payment_method, str) or payment_method.lower() not in get_payment_methods():
            message: str = "payment method is required and should be one of : {}".format(get_payment_methods())
            raise InputError(status=error_codes.input_error_code, description=message)

        membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                             Memberships.uid == uid).get()
        if isinstance(membership_instance, Memberships):
            membership_instance.payment_method = payment_method
            key: Optional[ndb.Key] = membership_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "Database Error: Unable to update payment method"
                raise InputError(status=error_codes.input_error_code, description=message)

            # Sending User payment method changed notification
            self.send_payment_method_changed_email(organization_id=organization_id, uid=uid,
                                                   membership_instance=membership_instance)

            message: str = "successfully updated payment method"
            return jsonify({'status': True, 'payload': membership_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = "Memberships record not found: Unable to update payment method"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    # noinspection PyUnusedLocal
    @use_context
    @handle_view_errors
    def send_welcome_email(self, organization_id: Optional[str], uid: Optional[str], plan_id: Optional[str]) -> tuple:
        ***REMOVED***
            **send_welcome_email**
                just send a request to the email service to send emails
            :param organization_id: -> str: unique organization id
            :param uid: -> str: unique user id
            :param plan_id: -> str: unique plan_id
            :return : tuple indicating if sending email as a success or failed
        ***REMOVED***
        return "Ok", status_codes.status_ok_code

    # noinspection PyUnusedLocal
    @use_context
    @handle_view_errors
    async def send_welcome_email_async(self, organization_id: Optional[str], uid: Optional[str],
                                       plan_id: Optional[str]) -> tuple:
        ***REMOVED***
            **send_welcome_email_async**
                just send a request to the email service to send emails

            :param organization_id: -> str: unique organization id
            :param uid: -> str: unique user id
            :param plan_id: -> str: unique plan_id
            :return : tuple indicating if sending email as a success or failed        
            
        ***REMOVED***
        # TODO- complete this and add email sending capability
        return "Ok", status_codes.status_ok_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    def return_plan_members_by_payment_status(self, organization_id: Optional[str], plan_id: Optional[str],
                                              status: Optional[str]) -> tuple:
        ***REMOVED***
            **return_plan_members_by_payment_status**
                return plan members with a certain status

        :param organization_id:
        :param plan_id:
        :param status:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "Organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(plan_id, str) or not bool(plan_id.strip()):
            message: str = "plan_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(status, str) or not bool(status.strip()):
            message: str = "status is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        membership_list: List[Memberships] = Memberships.query(Memberships.organization_id == organization_id,
                                                               Memberships.plan_id == plan_id,
                                                               Memberships.payment_status == status).fetch()

        if isinstance(membership_list, list) and len(membership_list):
            response_data: List[dict] = [member.to_dict() for member in membership_list]
            message: str = 'successfully fetched members'
            return jsonify({'status': True, 'payload': response_data, 'message': message}), status_codes.status_ok_code
        else:
            message: str = "Unable to find plan members whose payment status is {}".format(status)
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    async def return_plan_members_by_payment_status_async(self, organization_id: Optional[str], plan_id: Optional[str],
                                                          status: Optional[str]) -> tuple:
        ***REMOVED***
        **return_plan_members_by_payment_status_async
            for members of this plan_id return members by payment_status
            payment status should either be paid or unpaid

        :param organization_id:
        :param plan_id:
        :param status:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "Organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(plan_id, str) or not bool(plan_id.strip()):
            message: str = "plan_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(status, str) or not bool(status.strip()):
            message: str = "status is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        membership_list: List[Memberships] = Memberships.query(
            Memberships.organization_id == organization_id, Memberships.plan_id == plan_id,
            Memberships.payment_status == status).fetch_async().get_result()

        if isinstance(membership_list, list) and len(membership_list):
            response_data: List[dict] = [member.to_dict() for member in membership_list]
            message: str = 'successfully fetched members'
            return jsonify({'status': True, 'payload': response_data, 'message': message}), status_codes.status_ok_code
        else:
            message: str = "Unable to find plan members whose payment status is {}".format(status)
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    def return_members_by_payment_status(self, organization_id: Optional[str], status: Optional[str]) -> tuple:
        ***REMOVED***
        **return_members_by_payment_status**
            return members by payment status

        :param organization_id:
        :param status: payment status
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "Organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(status, str) or not bool(status.strip()):
            message: str = "status is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        membership_list: List[Memberships] = Memberships.query(Memberships.organization_id == organization_id,
                                                               Memberships.payment_status == status).fetch()

        if isinstance(membership_list, list) and len(membership_list):
            response_data: List[dict] = [member.to_dict() for member in membership_list]
            message: str = 'successfully fetched members'
            return jsonify({'status': True, 'payload': response_data, 'message': message}), status_codes.status_ok_code
        else:
            message: str = "Unable to find plan members whose payment status is {}".format(status)
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    async def return_members_by_payment_status_async(self, organization_id: Optional[str],
                                                     status: Optional[str]) -> tuple:
        ***REMOVED***
        **return_members_by_payment_status_async**
            async return members by payment status

        :param organization_id:
        :param status: payment status
        :return: 
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "Organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(status, str) or not bool(status.strip()):
            message: str = "status is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        membership_list: List[Memberships] = Memberships.query(
            Memberships.organization_id == organization_id,
            Memberships.payment_status == status).fetch_async().get_result()

        if isinstance(membership_list, list) and len(membership_list):
            response_data: List[dict] = [member.to_dict() for member in membership_list]
            message: str = 'successfully fetched members'
            return jsonify({'status': True, 'payload': response_data, 'message': message}), status_codes.status_ok_code
        else:
            message: str = "Unable to find plan members whose payment status is {}".format(status)
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    def return_plan_members(self, organization_id: Optional[str], plan_id: Optional[str]) -> tuple:

        ***REMOVED***
            **return_plan_members**
                return all members of a plan
            :param organization_id
            :param plan_id
            :return -> tuple with response , status_code
        ***REMOVED***
        if not isinstance(plan_id, str) or not bool(plan_id.strip()):
            message: str = "plan_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        membership_list: List[Memberships] = Memberships.query(Memberships.organization_id == organization_id,
                                                               Memberships.plan_id == plan_id).fetch()

        if isinstance(membership_list, list) and len(membership_list):
            response_data: List[dict] = [member.to_dict() for member in membership_list]
            message: str = 'successfully fetched members'
            return jsonify({'status': True, 'payload': response_data, 'message': message}), status_codes.status_ok_code
        else:
            message: str = "Unable to find members of plan"
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    async def return_plan_members_async(self, organization_id: Optional[str], plan_id: Optional[str]) -> tuple:
        ***REMOVED***
            **return_plan_members_async**
                return all members of a plan
            :param organization_id: -> str : unique organization identifier
            :param plan_id: -> str : unique user identifier
            :return -> tuple response, status_code 
        ***REMOVED***
        if not isinstance(plan_id, str) or not bool(plan_id.strip()):
            message: str = "plan_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        membership_list: List[Memberships] = Memberships.query(
            Memberships.organization_id == organization_id, Memberships.plan_id == plan_id).fetch_async().get_result()

        if isinstance(membership_list, list) and len(membership_list):
            response_data: List[dict] = [member.to_dict() for member in membership_list]
            message: str = 'successfully fetched members'
            return jsonify({'status': True, 'payload': response_data, 'message': message}), status_codes.status_ok_code
        else:
            message: str = "Unable to find members of plan {}"
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    def is_member_off(self, organization_id: Optional[str], uid: Optional[str]) -> tuple:
        ***REMOVED***
            **is_member_off**
                returns user membership details
            :param organization_id -> string 
            :param uid -> string 
            :return -> tuple : response, status_code 
        ***REMOVED***
        if not isinstance(organization_id, str) or bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        member_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                         Memberships.uid == uid).get()

        if isinstance(member_instance, Memberships):
            return jsonify(
                {'status': True, 'payload': member_instance.to_dict(),
                 'message': 'successfully fetched members'}), status_codes.status_ok_code
        else:
            return jsonify({'status': False,
                            'message': 'user does not have any membership plan'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    async def is_member_off_async(self, organization_id: Optional[str], uid: Optional[str]) -> tuple:

        ***REMOVED***
            **is_member_off_async**
                returns user membership details - membership details will be returned on payload 
                as a dict -- see Memberships for full documentations on parameters

            **Note**
                response format json {'status': True/False, 'payload': dict, 'message': '**what happened**'}

            :param organization_id -> string 
            :param uid -> string
            :return -> tuple response, status_code : 
        ***REMOVED***
        if not isinstance(organization_id, str) or bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        member_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                         Memberships.uid == uid).get_async().get_result()

        if isinstance(member_instance, Memberships):
            return jsonify(
                {'status': True, 'payload': member_instance.to_dict(),
                 'message': 'successfully fetched members'}), status_codes.status_ok_code
        else:
            message: str = 'user does not have any membership plan'
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    def payment_amount(self, organization_id: Optional[str], uid: Optional[str]) -> tuple:
        ***REMOVED***
            **payment_amount**
                for a specific user return payment amount - dict from AmountMixin

            **NOTE**
                response is dict in json format 
                the dict contains amount_data -- see AmountMixin for parameters

            **PARAMETERS**
                :param organization_id: -> str
                :param uid -> string
                :return tuple -> as response, status_code 
        ***REMOVED***
        if not isinstance(organization_id, str) or bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                             Memberships.uid == uid).get()

        if isinstance(membership_instance, Memberships):
            plan_id: str = membership_instance.plan_id
            membership_plan_instance: MembershipPlans = MembershipPlansView()._get_plan(
                organization_id=organization_id, plan_id=plan_id)

            if not bool(membership_plan_instance):
                message: str = 'could not find plan associate with the plan_id'
                return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

            if bool(membership_plan_instance.term_payment_amount) and bool(
                    membership_plan_instance.registration_amount):
                amount_data: dict = {
                    'term_payment_amount': membership_plan_instance.term_payment_amount.to_dict(),
                    'registration_amount': membership_plan_instance.registration_amount.to_dict()}
                message: str = 'successfully returned payment details'
                return jsonify({'status': True, 'payload': amount_data,
                                'message': message}), status_codes.status_ok_code

        message: str = 'unable to locate membership details'
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    async def payment_amount_async(self, organization_id: Optional[str], uid: Optional[str]) -> tuple:

        ***REMOVED***
            **payment_amount_async**
                for a specific user return payment amount
            **NOTE**
                response is dict in json format 
                the dict contains amount_data -- see AmountMixin for parameters

            **PARAMETERS**
                :param organization_id:
                :param uid: -> string
                :return tuple: -> as response, status_code
        ***REMOVED***
        if not isinstance(organization_id, str) or bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                             Memberships.uid == uid).get_async().get_result()

        if isinstance(membership_instance, Memberships):
            plan_id: str = membership_instance.plan_id
            membership_plan_instance: MembershipPlans = await MembershipPlansView()._get_plan_async(
                organization_id=organization_id, plan_id=plan_id)

            if not bool(membership_plan_instance):
                message: str = 'could not find plan associate with the plan_id'
                return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

            if bool(membership_plan_instance.term_payment_amount) and bool(
                    membership_plan_instance.registration_amount):
                amount_data: dict = {
                    'term_payment_amount': membership_plan_instance.term_payment_amount.to_dict(),
                    'registration_amount': membership_plan_instance.registration_amount.to_dict()}
                message: str = 'successfully returned payment details'
                return jsonify(
                    {'status': True, 'payload': amount_data, 'message': message}), status_codes.status_ok_code

        message: str = 'unable to locate membership details'
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def un_subscribe(self, organization_id: Optional[str], uid: Optional[str], plan_id: Optional[str]) -> tuple:
        ***REMOVED***
            **un_subscribe**
                enables the client to un-subscribe from a plan
            
            **NOTE**
                when successful the payload dict will contain contents of Memberships 
                see Memberships Class for parameters
            
            **PARAMETERS**
                :param organization_id:
                :param uid:
                :param plan_id:
                :return: tuple -> as response, status_code 
        ***REMOVED***
        if not isinstance(organization_id, str) or bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(plan_id, str) or not bool(plan_id.strip()):
            message: str = "plan_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                             Memberships.uid == uid).get()
        if isinstance(membership_instance, Memberships):
            membership_instance.is_active_subscription = False
            key: Optional[ndb.Key] = membership_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "Database Error: Unable to un-subscribe please try again later"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            # TODO please update cache
            message: str = "Successfully un-subscribed from your membership plan"
            # TODO important please also un-subscribe from paypal services
            return jsonify({'status': True,
                            'payload': membership_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = "Data Error: Unable to find membership record"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code


def plan_data_wrapper(func):
    ***REMOVED***
        **plan_data_wrapper**
            --use on membership_plans only--
            wraps add plan in order to check validity of the input data,
            throws InputError in-case of an error in Input
        **PARAMETERS**
            :param func:
            :return: func with correct variables
    ***REMOVED***

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        membership_plan_data: Optional[dict] = kwargs.get('membership_plan_data')
        if not bool(membership_plan_data):
            message: str = "Input is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        plan_name: Optional[str] = membership_plan_data.get('plan_name')
        if not isinstance(plan_name, str) or not bool(plan_name.strip()):
            message: str = "plan name is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        description: Optional[str] = membership_plan_data.get('description')
        if not isinstance(description, str) or not bool(description.strip()):
            message: str = "description is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        # Note if scheduled day is not supplied it will be zero or None
        schedule_day: Optional[int] = int(membership_plan_data.get('schedule_day', 0))
        # NOTE: if schedule_day is None or Zero then this is an Error
        if not bool(schedule_day):
            message: str = "schedule_day is required and cannot be zero or Null"
            raise InputError(status=error_codes.input_error_code, description=message)

        schedule_term: Optional[str] = membership_plan_data.get('schedule_term')
        if not isinstance(schedule_term, str) or not bool(schedule_term.strip()):
            message: str = "schedule term is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        # int(None) avoiding this
        term_payment: int = int(membership_plan_data.get('term_payment', 0))
        registration_amount: int = int(membership_plan_data.get('registration_amount', 0))

        currency: Optional[str] = membership_plan_data.get('currency')
        if not isinstance(currency, str) or not bool(currency.strip()):
            message: str = "currency is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_id: Optional[str] = membership_plan_data.get('organization_id')
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        service_id: Optional[str] = membership_plan_data.get('service_id')
        if not isinstance(service_id, str) or not bool(service_id.strip()):
            message: str = "service or product must be created first before payment plans are created"
            raise InputError(status=error_codes.input_error_code, description=message)

        return func(organization_id=organization_id, service_id=service_id, plan_name=plan_name,
                    description=description, schedule_day=schedule_day,
                    schedule_term=schedule_term, term_payment=term_payment, registration_amount=registration_amount,
                    currency=currency, *args)

    return wrapper


# noinspection DuplicatedCode
class MembershipPlansView(Validators):
    ***REMOVED***
        **Class MembershipPlansView**
            this class controls access to membership plans database
            also checks for input data validity
    ***REMOVED***

    def __init__(self):
        super(MembershipPlansView, self).__init__()

    # TODO - add Membership Plans Validators

    @staticmethod
    def create_plan_in_paypal_services(organization_id: str, service_id: str, plan_name: str, description: str,
                                       schedule_day: int, schedule_term: str, term_payment: int,
                                       registration_amount: int, currency: str) -> Optional[str]:
        ***REMOVED***
            **create_plan_in_paypal_services**
                creates this plan in paypal services first

            **PARAMETERS**
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
            **add_plan**
                checks to see if the plan actually exists and the new plan name wont cause a conflict with
                an existing name
                 plan_name: str, description: str, schedule_day: int, schedule_term: str,
                     term_payment: int, registration_amount: int, currency: str, is_active: bool) -> tuple:
            **NOTE**
                plan_id: will be created by paypal subscriptions
                service_id: has already been created from paypal

            The Client chooses an option to create a new payment plan from a list of available services
        ***REMOVED***

        is_active = True
        # Note: Creating the payment plan in PayPal Services Note: this means the product for the
        #  payment plan is already created

        plan_id: Optional[str] = self.create_plan_in_paypal_services(
            organization_id=organization_id, service_id=service_id, plan_name=plan_name, description=description,
            schedule_day=schedule_day,
            schedule_term=schedule_term, term_payment=term_payment, registration_amount=registration_amount,
            currency=currency)

        if not bool(plan_id):
            message: str = "Unable to create Payment Plan check your service_id or inform admin"
            raise RequestError(status=error_codes.input_error_code, description=message)

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

            key: Optional[ndb.Key] = plan_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = 'Database Error: error creating plan please try again later'
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            return jsonify({'status': True, 'message': 'successfully created new membership plan',
                            'payload': plan_instance.to_dict()}), status_codes.status_ok_code

        # TODO refactor other forbidden errors
        message: str = 'Operation Denied: Unable to create plan'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

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

        plan_id: Optional[str] = self.create_plan_in_paypal_services(
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

            key: Optional[ndb.Key] = plan_instance.put_async(retries=self._max_retries,
                                                             timeout=self._max_timeout).get_result()
            if not bool(key):
                message: str = 'for some reason we are unable to create a new plan'
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            return jsonify({'status': True, 'message': 'successfully created new membership plan',
                            'payload': plan_instance.to_dict()}), status_codes.successfully_updated_code

        message: str = "Operation Denied: Unable to create new  membership plan"
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    # noinspection DuplicatedCode
    @use_context
    @handle_view_errors
    def update_plan(self, organization_id: Optional[str], plan_id: str, plan_name: str, description: str,
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

                key: Optional[ndb.Key] = membership_plans_instance.put(retries=self._max_retries,
                                                                       timeout=self._max_timeout)

                if not bool(key):
                    message: str = 'for some reason we are unable to create a new plan'
                    raise DataServiceError(status=error_codes.data_service_error_code, description=message)

                return jsonify({'status': True, 'message': 'successfully created new membership plan',
                                'payload': membership_plans_instance.to_dict()}), status_codes.status_ok_code

            message: str = 'Membership plan not found'
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

        message: str = 'Operation Denied: Conditions to update plan not satisfied'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    # noinspection DuplicatedCode
    @use_context
    @handle_view_errors
    async def update_plan_async(self, organization_id: Optional[str], plan_id: str, plan_name: str,
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

        if await self.can_update_plan_async(organization_id=organization_id, plan_id=plan_id, plan_name=plan_name):
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
                key: Optional[ndb.Key] = membership_plans_instance.put_async(retries=self._max_retries,
                                                                             timeout=self._max_timeout).get_result()
                if not bool(key):
                    message: str = 'for some reason we are unable to create a new plan'
                    raise DataServiceError(status=error_codes.data_service_error_code, description=message)
                return jsonify({'status': True, 'message': 'successfully created new membership plan',
                                'payload': membership_plans_instance.to_dict()}), status_codes.status_ok_code

            message: str = 'Membership plan not found'
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

        message: str = 'Operation Denied: Conditions to update plan not satisfied'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    @use_context
    @handle_view_errors
    def set_is_active(self, organization_id: Optional[str], plan_id: Optional[str],
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
            key: Optional[ndb.Key] = membership_plans_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = 'for some reason we are unable to create a new plan'
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            message: str = 'successfully update membership plan status'
            return jsonify({'status': True, 'message': message,
                            'payload': membership_plans_instance.to_dict()}), status_codes.status_ok_code

        message: str = 'Membership plan not found'
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    async def set_is_active_async(self, organization_id: Optional[str], plan_id: Optional[str],
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
            key: Optional[ndb.Key] = membership_plans_instance.put_async(retries=self._max_retries,
                                                                         timeout=self._max_timeout).get_result()
            if not bool(key):
                message: str = 'for some reason we are unable to create a new plan'
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
            return jsonify({'status': True, 'message': 'successfully update membership plan status',
                            'payload': membership_plans_instance.to_dict()}), status_codes.status_ok_code

        message: str = 'Membership plan not found'
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    def return_plans_by_schedule_term(self, organization_id: Optional[str], schedule_term: str) -> tuple:
        ***REMOVED***
            returns plan schedules - this is a payment schedule for the plan
        :param organization_id:
        :param schedule_term:
        :return:
        ***REMOVED***

        membership_plan_list: List[MembershipPlans] = MembershipPlans.query(
            MembershipPlans.organization_id == organization_id, MembershipPlans.schedule_term == schedule_term).fetch()

        payload: List[dict] = [membership.to_dict() for membership in membership_plan_list]
        if len(payload):
            return jsonify({'status': True, 'payload': payload,
                            'message': 'successfully retrieved monthly plans'}), status_codes.status_ok_code

        message: str = "Unable to find plans by schedule term"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    async def return_plans_by_schedule_term_async(self, organization_id: Optional[str], schedule_term: str) -> tuple:
        ***REMOVED***
            returns plan schedules - this is a payment schedule for the plan
        :param organization_id:
        :param schedule_term:
        :return:
        ***REMOVED***

        membership_plan_list: List[MembershipPlans] = MembershipPlans.query(
            MembershipPlans.organization_id == organization_id,
            MembershipPlans.schedule_term == schedule_term).fetch_async().get_result()

        payload: List[dict] = [membership.to_dict() for membership in membership_plan_list]

        if len(payload):
            return jsonify({'status': True, 'payload': payload,
                            'message': 'successfully retrieved monthly plans'}), status_codes.status_ok_code

        message: str = "Unable to find plans by schedule term"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @staticmethod
    @handle_store_errors
    def _get_plan(organization_id: str, plan_id: str) -> Optional[MembershipPlans]:
        ***REMOVED***
            **_get_plan_async**
                this utility will be used by other views to obtain information about membershipPlans

            **NOTE**
                do not directly call this function

        :param organization_id:
        :param plan_id:
        :return:
        ***REMOVED***
        if isinstance(plan_id, str) and bool(plan_id.strip()):
            membership_plan_instance: MembershipPlans = MembershipPlans.query(
                Memberships.organization_id == organization_id, MembershipPlans.plan_id == plan_id.strip()).get()

            if isinstance(membership_plan_instance, MembershipPlans):
                return membership_plan_instance
        return None

    @staticmethod
    @handle_store_errors
    async def _get_plan_async(organization_id: str, plan_id: str) -> Optional[MembershipPlans]:
        ***REMOVED***
            **_get_plan_async**

                this utility will be used by other views to obtain information about membershipPlans
            **NOTE**
                do not directly call this function

        :param organization_id:
        :param plan_id:
        :return:
        ***REMOVED***
        if isinstance(plan_id, str):
            membership_plan_instance: MembershipPlans = MembershipPlans.query(
                MembershipPlans.organization_id == organization_id,
                MembershipPlans.plan_id == plan_id).get_async().get_result()

            if isinstance(membership_plan_instance, MembershipPlans):
                return membership_plan_instance
        return None

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    def return_plan(self, organization_id: str, plan_id: str) -> tuple:
        ***REMOVED***
            return a specific membership plan
        :param organization_id:
        :param plan_id: the id of the plan to return - Note: this plan id is the same as the plan id / product id in PayPal
        :return: plan details
        ***REMOVED***

        plan_instance = self._get_plan(organization_id=organization_id, plan_id=plan_id)
        if bool(plan_instance):
            message: str = "successfully fetched plan"
            return jsonify({'status': True, 'payload': plan_instance.to_dict(),
                            'message': message}), status_codes.status_ok_code

        return jsonify({'status': False, 'message': 'Unable to get plan'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    async def return_plan_async(self, organization_id: str, plan_id: str) -> tuple:
        ***REMOVED***
            return a specific membership plan
        :param organization_id:
        :param plan_id: the id of the plan to return - Note: this plan id is the same as the plan id / product id in PayPal
        :return: plan details
        ***REMOVED***

        plan_instance = await self._get_plan_async(organization_id=organization_id, plan_id=plan_id)
        if bool(plan_instance):
            message: str = "successfully fetched plan"
            return jsonify({'status': True, 'payload': plan_instance.to_dict(),
                            'message': message}), status_codes.status_ok_code

        return jsonify({'status': False,
                        'message': 'Unable to get plan'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    def return_plan_by_uid(self, organization_id: str, uid: str) -> tuple:
        ***REMOVED***
            return membership plan details for a specific user
        :param uid: user uid
        :param organization_id: organization uid
        :return: plan details
        ***REMOVED***

        membership_instance: Memberships = Memberships.query(Memberships.organization_id == organization_id,
                                                             Memberships.uid == uid).get()

        if bool(membership_instance):
            plan_instance = self._get_plan(organization_id=organization_id, plan_id=membership_instance.plan_id)
            message: str = "successfully fetched user plan"
            return jsonify({'status': True, 'payload': plan_instance.to_dict(),
                            'message': message}), status_codes.status_ok_code

        return jsonify({'status': False,
                        'message': 'Unable to get plan'}), status_codes.data_not_found_code

    @staticmethod
    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    def return_all_plans(organization_id: str) -> tuple:
        ***REMOVED***
            returns all memberships plans, Note that some more details on membership plans are located in PayPal
            :param organization_id:
            :return: memberships plans
        ***REMOVED***

        membership_plan_list: List[MembershipPlans] = MembershipPlans.query(
            MembershipPlans.organization_id == organization_id).fetch()

        plan_list: List[dict] = [plan.to_dict() for plan in membership_plan_list]

        if len(plan_list):
            return jsonify({'status': True, 'payload': plan_list,
                            'message': 'successfully fetched all memberships'}), status_codes.status_ok_code

        message: str = "Unable to find membership plans"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @staticmethod
    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    async def return_all_plans_async(organization_id: str) -> tuple:
        ***REMOVED***
            returns all memberships plans, Note that some more details on membership plans are located in PayPal
            :param organization_id:
            :return: memberships plans
        ***REMOVED***

        membership_plan_list: List[MembershipPlans] = MembershipPlans.query(
            MembershipPlans.organization_id == organization_id).fetch_async().get_result()

        plan_list: List[dict] = [plan.to_dict() for plan in membership_plan_list]
        if len(plan_list):
            return jsonify({'status': True, 'payload': plan_list,
                            'message': 'successfully fetched all memberships'}), status_codes.status_ok_code

        message: str = "Unable to find membership plans"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code


class AccessRightsView:
    ***REMOVED***
        manage the view for AccessRights
    ***REMOVED***

    def __init__(self):
        pass

    @use_context
    def get_access_rights(self, organization_id: str, plan_id: str) -> Optional[AccessRights]:
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
    async def get_access_rights_async(self, organization_id: str, plan_id: str) -> Optional[AccessRights]:
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
        coupon_data: Optional[dict] = kwargs.get('coupon_data')
        # either its dict in which case it may contain our data and we will find out below
        # or coupon_data is Null in which case it will raise an InputError
        if not bool(coupon_data):
            message: str = "Input is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        code: Optional[str] = coupon_data.get('code')
        if not isinstance(code, str) or not bool(code.strip()):
            message: str = "coupon code is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        # Note: this means discount will be zero if not supplied or discount is zero
        # either zero is an error
        discount: Optional[int] = int(coupon_data.get('discount') or 0)
        if not bool(discount):
            message: str = "discount is required and cannot be Zero"
            raise InputError(status=error_codes.input_error_code, description=message)

        # Note: This effectively means if expiration_time is not submitted it will equal zero
        expiration_time: Optional[int] = int(coupon_data.get('expiration_time') or 0)
        if not bool(expiration_time):
            message: str = "Expiration time cannot be Null or Zero"
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_id: Optional[str] = coupon_data.get("organization_id")
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
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
    def add_coupon(self, organization_id: Optional[str], code: Optional[str], discount: Optional[int],
                   expiration_time: Optional[int]) -> tuple:
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

            key: Optional[ndb.Key] = coupons_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "an error occurred while creating coupon"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            return jsonify({'status': True, 'message': 'successfully created coupon code',
                            'payload': coupons_instance.to_dict()}), status_codes.successfully_updated_code

        message: str = 'Unable to add coupon, please check expiration time or coupon code'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    @get_coupon_data
    @use_context
    @handle_view_errors
    async def add_coupon_async(self, organization_id: Optional[str], code: Optional[str], discount: Optional[int],
                               expiration_time: Optional[int]) -> tuple:
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

            key: Optional[ndb.Key] = coupons_instance.put_async(retries=self._max_retries,
                                                                timeout=self._max_timeout).get_result()
            if not bool(key):
                message: str = "an error occurred while creating coupon"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            return jsonify({'status': True, 'message': 'successfully created coupon code',
                            'payload': coupons_instance.to_dict()}), status_codes.successfully_updated_code
        message: str = 'Unable to add coupon, please check expiration time or coupon code'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    @get_coupon_data
    @use_context
    @handle_view_errors
    def update_coupon(self, organization_id: Optional[str], code: str, discount: int, expiration_time: int) -> tuple:
        ***REMOVED***
            update coupons asynchronously
            :param organization_id:
            :param code: code relating to the coupon - this field must not be updated - used to locate coupon_instance
            :param discount: up-datable a percentage indicating how much of the original amount should be discountable
            :param expiration_time: up-datable value indicates the time the coupon code will expire
            :return:  updated coupon
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(code, str) or not bool(code.strip()):
            message: str = "code is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(expiration_time, int):
            message: str = "expiration_time is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if self.can_update_coupon(code=code, expiration_time=expiration_time, discount=discount):
            coupon_instance: Coupons = Coupons.query(Coupons.organization_id == organization_id,
                                                     Coupons.code == code).get()
            # Discounted amount in percent
            coupon_instance.discount_percent = discount
            # timestamp indicating the time the coupon will expire
            coupon_instance.expiration_time = expiration_time
            key: Optional[ndb.Key] = coupon_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "Error updating coupon"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            return jsonify({'status': True,
                            'payload': coupon_instance.to_dict(),
                            'message': 'successfully updated coupon'}), status_codes.successfully_updated_code

        message: str = "You are not authorized to update coupon codes"
        return jsonify({'status': False, 'message': message}), error_codes.un_auth_error_code

    @get_coupon_data
    @use_context
    @handle_view_errors
    async def update_coupon_async(self, organization_id: Optional[str], code: str, discount: int,
                                  expiration_time: Optional[int] = None) -> tuple:
        ***REMOVED***
            update coupons asynchronously
            :param organization_id:
            :param code: code relating to the coupon - this field must not be updated - used to locate coupon_instance
            :param discount: up-datable a percentage indicating how much of the original amount should be discountable
            :param expiration_time: up-datable value for coupons
            :return:  updated coupon
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(code, str) or not bool(code.strip()):
            message: str = "code is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(expiration_time, int) or expiration_time < timestamp():
            message: str = "expiration_time is required and can only be a timestamp greater than now"
            raise InputError(status=error_codes.input_error_code, description=message)

        if await self.can_update_coupon_async(organization_id=organization_id, code=code,
                                              expiration_time=expiration_time, discount=discount) is True:

            coupon_instance: Coupons = Coupons.query(
                Coupons.organization_id == organization_id, Coupons.code == code).get_async().get_result()

            # Discount a percentage indicating how much of the original price should be knocked off
            coupon_instance.discount_percent = discount
            coupon_instance.expiration_time = expiration_time
            key: Optional[ndb.Key] = coupon_instance.put_async(retries=self._max_retries,
                                                               timeout=self._max_timeout).get_result()
            if not bool(key):
                message: str = "Database Error: Error updating coupon"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            return jsonify({'status': True,
                            'payload': coupon_instance.to_dict(),
                            'message': 'successfully updated coupon'}), status_codes.status_ok_code

        message: str = "You are not authorized to update coupon codes"
        return jsonify({'status': False, 'message': message}), error_codes.un_auth_error_code

    @use_context
    @handle_view_errors
    def cancel_coupon(self, coupon_data: dict) -> tuple:
        ***REMOVED***
            cancels coupon code require organization_id and coupon_data
        :param coupon_data: contains coupon code and organization_id
        :return: cancelled coupon code
        ***REMOVED***
        code: Optional[str] = coupon_data.get("code")
        organization_id: Optional[str] = coupon_data.get('organization_id')
        if not isinstance(code, str) or not bool(code.strip()):
            message: str = "coupon code is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        coupon_instance: Coupons = Coupons.query(Coupons.organization_id == organization_id,
                                                 Coupons.code == code).get()

        if isinstance(coupon_instance, Coupons):
            coupon_instance.is_valid = False
            key: Optional[ndb.Key] = coupon_instance.put(retries=self._max_retries, timeout=self._max_timeout)

            if not bool(key):
                message: str = "Unable to cancel coupon"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            return jsonify({'status': True,
                            'payload': coupon_instance.to_dict(),
                            'message': 'successfully cancelled coupon code'}), status_codes.successfully_updated_code

        message: str = "coupon not found: unable to cancel coupon code"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    async def cancel_coupon_async(self, coupon_data: dict) -> tuple:
        ***REMOVED***
            cancels coupon code
        :param coupon_data: contains coupon code and organization_id
        :return:
        ***REMOVED***
        code: Optional[str] = coupon_data.get("code")
        organization_id: Optional[str] = coupon_data.get('organization_id')

        if not isinstance(code, str) or not bool(code.strip()):
            message: str = "coupon code is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        coupon_instance: Coupons = Coupons.query(Coupons.organization_id == organization_id,
                                                 Coupons.code == code).get_async().get_result()

        if isinstance(coupon_instance, Coupons):
            coupon_instance.is_valid = False
            key: Optional[ndb.Key] = coupon_instance.put_async(retries=self._max_retries,
                                                               timeout=self._max_timeout).get_result()
            if not bool(key):
                message: str = "Unable to cancel coupon"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
            return jsonify({'status': True,
                            'payload': coupon_instance.to_dict(),
                            'message': 'successfully cancelled coupon code'}), status_codes.successfully_updated_code

        message: str = "coupon not found: unable to cancel coupon code"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    def get_all_coupons(self, organization_id: Optional[str]) -> tuple:
        ***REMOVED***
            returns a list of all coupons
        :param organization_id:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        coupons_list: List[Coupons] = Coupons.query(Coupons.organization_id == organization_id).fetch()

        payload: List[dict] = [coupon.to_dict() for coupon in coupons_list]
        if len(payload):
            message: str = "coupons successfully created"
            return jsonify({'status': True, 'payload': payload,
                            'message': message}), status_codes.status_ok_code

        message: str = "coupons not found"
        return jsonify({'status': True, 'payload': payload,
                        'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    async def get_all_coupons_async(self, organization_id: Optional[str]) -> tuple:
        ***REMOVED***
            retrieve all coupons
        :param organization_id:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        coupons_list: List[Coupons] = Coupons.query(
            Coupons.organization_id == organization_id).fetch_async().get_result()
        payload: List[dict] = [coupon.to_dict() for coupon in coupons_list]
        if len(payload):
            message: str = "coupons successfully retrieved"
            return jsonify({'status': True, 'payload': payload,
                            'message': message}), status_codes.status_ok_code

        message: str = "coupons not found"
        return jsonify({'status': True, 'payload': payload,
                        'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    def get_valid_coupons(self, organization_id: Optional[str]) -> tuple:
        ***REMOVED***
            returns a list of expired coupon codes
        :param organization_id:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        coupons_list: List[Coupons] = Coupons.query(
            Coupons.organization_id == organization_id, Coupons.is_valid == True).fetch()
        payload: List[dict] = [coupon.to_dict() for coupon in coupons_list]

        if len(payload):
            message: str = "valid successfully retrieved"
            return jsonify({'status': True, 'payload': payload,
                            'message': message}), status_codes.status_ok_code

        message: str = "valid coupon codes not found"
        return jsonify({'status': True, 'payload': payload,
                        'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    async def get_valid_coupons_async(self, organization_id: Optional[str]) -> tuple:
        ***REMOVED***
            returns a list of valid coupon codes
        :param organization_id:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        coupons_list: List[Coupons] = Coupons.query(Coupons.organization_id == organization_id,
                                                    Coupons.is_valid == True).fetch_async().get_result()

        payload: List[dict] = [coupon.to_dict() for coupon in coupons_list]
        if len(payload):
            message: str = "coupons successfully retrieved"
            return jsonify({'status': True, 'payload': payload,
                            'message': message}), status_codes.status_ok_code

        message: str = "coupons not found"
        return jsonify({'status': True, 'payload': payload,
                        'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    def get_expired_coupons(self, organization_id: Optional[str]) -> tuple:
        ***REMOVED***
            returns a list of expired coupon codes
        :param organization_id:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        coupons_list: List[Coupons] = Coupons.query(Coupons.organization_id == organization_id,
                                                    Coupons.expiration_time < timestamp()).fetch()

        payload: List[dict] = [coupon.to_dict() for coupon in coupons_list]
        if len(payload):
            message: str = "expired coupons successfully retrieved"
            return jsonify({'status': True, 'payload': payload,
                            'message': message}), status_codes.status_ok_code

        message: str = "expired coupons not found"
        return jsonify({'status': True, 'payload': payload,
                        'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    async def get_expired_coupons_async(self, organization_id: Optional[str]) -> tuple:
        ***REMOVED***
            returns a list of expired coupon codes
        :param organization_id:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        coupons_list: List[Coupons] = Coupons.query(
            Coupons.organization_id == organization_id,
            Coupons.expiration_time < timestamp()).fetch_async().get_result()

        payload: List[dict] = [coupon.to_dict() for coupon in coupons_list]
        if len(payload):
            message: str = "successfully fetched expired coupon codes"
            return jsonify({'status': True, 'payload': payload,
                            'message': message}), status_codes.status_ok_code

        message: str = "expired coupons not found"
        return jsonify({'status': True, 'payload': payload,
                        'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    def get_coupon(self, coupon_data: dict) -> tuple:
        ***REMOVED***
            returns coupon code data required parameters are organization_id and coupon_id
        :param coupon_data: dict containing code and organization_id as required parameters
        :return: coupon_data
        ***REMOVED***
        code: Optional[str] = coupon_data.get("code")

        if not isinstance(code, str) or not bool(code.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_id: Optional[str] = coupon_data.get('organization_id')
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        coupon_instance: Coupons = Coupons.query(Coupons.organization_id == organization_id,
                                                 Coupons.code == code).get()

        if isinstance(coupon_instance, Coupons):
            message: str = "Coupon has been found"
            return jsonify({'status': True, 'message': message,
                            'payload': coupon_instance.to_dict()}), status_codes.status_ok_code

        message: str = "Invalid Coupon Code - Or Coupon not found"
        return jsonify({'status': True, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    async def get_coupon_async(self, coupon_data: dict) -> tuple:
        code: Optional[str] = coupon_data.get("code")

        if not bool(code):
            message: str = "Coupon Code is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_id: Optional[str] = coupon_data.get('organization_id')
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        coupon_instance: Coupons = Coupons.query(Coupons.organization_id == organization_id,
                                                 Coupons.code == code).get_async().get_result()

        if isinstance(coupon_instance, Coupons):
            message: str = "Coupon found"
            return jsonify({'status': True,
                            'message': message,
                            'payload': coupon_instance.to_dict()}), status_codes.status_ok_code

        message: str = "Invalid Coupon Code - Or Coupon Code not found"
        return jsonify({'status': True, 'message': message}), status_codes.data_not_found_code

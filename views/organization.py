"""
** Module - Organization View Controller **
    enables users to add , update Organization Accounts
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from typing import Optional, List
import requests
from flask import current_app, jsonify
from google.cloud import ndb
from _sdk._email import Mailgun
from config.exception_handlers import handle_view_errors, handle_store_errors, handle_requests_errors
from config.exceptions import (InputError, DataServiceError, error_codes, status_codes, UnAuthenticatedError,
                               RequestError)
from config.use_context import use_context
from database.mixins import AmountMixin
from database.organization import Organization, OrgValidators
# TODO finish up organization  view

from utils.utils import create_id, return_ttl
from cache.cache_manager import app_cache


class OrganizationEmails(Mailgun):
    """
        **Class OrganizationEmails**
            class Used to send Emails and Notifications related to Organizations
    """

    def __init__(self):
        super(OrganizationEmails, self).__init__()

    # noinspection DuplicatedCode
    def send_successfully_created_organization(self, organization_id: str, uid: str) -> None:
        """
            **send_successfully_created_organization**
                once an organization is created send an email of this to the end user explaining the steps
                they need to perform in order to complete the transaction

            :param organization_id:
            :param uid:
            :return:
        """
        user_data, organization_data = self.return_organization_user(organization_id=organization_id, uid=uid)
        email_verified: bool = user_data.get('email_verified')
        subject: str = f"{organization_data.get('organization_name')} Organization was created successfully"

        text: str = f'''
        Hi {user_data.get('names', " ")} {user_data.get('surname', " ")}
        
        Organization has been successfully created : {organization_data.get('organization_name')}
        
            Organization Name: {organization_data.get('organization_name')}
            Description: {organization_data.get('description')}
            Website Home: {organization_data.get('home_url')}
            Login Callback URL : {organization_data.get('login_callback_url')}
            Password Recovery Callback URL : {organization_data.get('recovery_callback_url')}
         
        
        Thank you
        {current_app.config.get('APP_NAME')}                
        '''
        html: str = f'''
        <h3>Hi {user_data.get('names', " ")} {user_data.get('surname', " ")}</h3>
        
        <p>Organization has been successfully created : {organization_data.get('organization_name')}</p>
        
        <ol>
            <li>Organization Name: {organization_data.get('organization_name')}</li>
            <li>Description: {organization_data.get('description')}</li>
            <li>Website Home: {organization_data.get('home_url')}</li>
            <li>Login Callback URL : {organization_data.get('login_callback_url')}</li>
            <li>Password Recovery Callback URL : {organization_data.get('recovery_callback_url')}</li>
        </ol>
                
        <h4>Thank you</h4>
        <strong>{current_app.config.get('APP_NAME')}</strong>                            
        '''
        email: Optional[str] = user_data.get('email')
        if email_verified and bool(email):
            self._do_schedule_mail(to_email=email, subject=subject, text=text, html=html)

        message: str = "Bad Request Error: Email not verified please verify your account"
        raise RequestError(status=error_codes.bad_request_error_code, description=message)

    def send_organization_wallet_created_email(self, organization_id: str, uid: str) -> None:
        """
            **organization_wallet_created**
                send an email when an organization wallet has been created
        :param organization_id:
        :param uid:
        :return:
        """
        user_data, organization_data = self.return_organization_user(organization_id=organization_id, uid=uid)
        email_verified: bool = user_data.get('email_verified')
        subject: str = f"{organization_data.get('organization_name')} Organization Wallet created successfully"

        # TODO - obtain wallet details

        text: str = f'''
        Hi {user_data.get('names', " ")} {user_data.get('surname', " ")}

        organization Wallet has been successfully created : {organization_data.get('organization_name')}

        Thank you
        {current_app.config.get('APP_NAME')}                
        '''
        html: str = f'''
        <h3>Hi {user_data.get('names', " ")} {user_data.get('surname', " ")}</h3>

        <p>Organization Wallet has been successfully created : {organization_data.get('organization_name')}</p>

        <h4>Thank you</h4>
        <strong>{current_app.config.get('APP_NAME')}</strong>                            
        '''
        email: Optional[str] = user_data.get('email')
        if email_verified and bool(email):
            self._do_schedule_mail(to_email=email, subject=subject, text=text, html=html)

        message: str = "Bad Request Error: Email not verified please verify your account"
        raise RequestError(status=error_codes.bad_request_error_code, description=message)

    # noinspection DuplicatedCode
    def send_organization_updated_email(self, organization_id: str, uid: str) -> None:
        """

        :param organization_id:
        :param uid:
        :return:
        """
        user_data, organization_data = self.return_organization_user(organization_id=organization_id, uid=uid)
        email_verified: bool = user_data.get('email_verified')
        subject: str = f"{organization_data.get('organization_name')} Successfully updated"

        text: str = f'''
            Hi {user_data.get('names', " ")} {user_data.get('surname', " ")}
    
            Organization : {organization_data.get('organization_name')} has been updated successfully. 
    
                Organization Name: {organization_data.get('organization_name')}
                Description: {organization_data.get('description')}
                Website Home: {organization_data.get('home_url')}
                Login Callback URL : {organization_data.get('login_callback_url')}
                Password Recovery Callback URL : {organization_data.get('recovery_callback_url')}
    
    
            Thank you
            {current_app.config.get('APP_NAME')}                
        '''
        html: str = f'''
            <h3>Hi {user_data.get('names', " ")} {user_data.get('surname', " ")}</h3>
    
            <p>Organization : {organization_data.get('organization_name')} has been updated successfully.</p> 
    
            <ol>
                <li>Organization Name: {organization_data.get('organization_name')}</li>
                <li>Description: {organization_data.get('description')}</li>
                <li>Website Home: {organization_data.get('home_url')}</li>
                <li>Login Callback URL : {organization_data.get('login_callback_url')}</li>
                <li>Password Recovery Callback URL : {organization_data.get('recovery_callback_url')}</li>
            </ol>
    
            <h4>Thank you</h4>
            <strong>{current_app.config.get('APP_NAME')}</strong>                            
        '''
        email: Optional[str] = user_data.get('email')
        if email_verified and bool(email):
            self._do_schedule_mail(to_email=email, subject=subject, text=text, html=html)

        message: str = "Bad Request Error: Email not verified please verify your account"
        raise RequestError(status=error_codes.bad_request_error_code, description=message)

    def send_organization_stats_email(self, organization_id: str, uid: str) -> None:
        """
            **send_organization_stats_email**
                sends organizational statistics email to organization owner

        :param self:
        :param organization_id:
        :param uid:
        :return:
        """
        user_data, organization_data = self.return_organization_user(organization_id=organization_id, uid=uid)
        email_verified = user_data.get('email_verified')
        subject: str = f"User Statistics for {organization_data.get('organization_name')}"

        text: str = f'''
            hi {user_data.get('names', " ")} {user_data.get('surname', " ")}
            
            Here are your organization statistics for {organization_data.get('organization_name')}
            
            User Statistics
            
            Total Affiliates : {organization_data.get('total_affiliates')}
            Total Subscriptions : {organization_data.get('total_members')}
            Total Users: {organization_data.get('total_users')}
            
            
            Income Statistics        
    
            Total Memberships Payments: {organization_data.get('total_membership_payments')}
            Total Paid : {organization_data.get('total_paid')}
            Balance: {organization_data.get('balance')}
            
            Thank you
            {current_app.config.get('APP_NAME')}        
        
        '''

        html: str = f'''
            <h3>hi {user_data.get('names', " ")} {user_data.get('surname', " ")}</h3>
            
            <p>Here are your organization statistics for {organization_data.get('organization_name')}</p>
            
            <h3>User Statistics</h3>
            <ol>
                <li>Total Affiliates : {organization_data.get('total_affiliates')}</li>
                <li>Total Subscriptions : {organization_data.get('total_members')}</li>
                <li>Total Users: {organization_data.get('total_users')}</li>
            </ol>                    
            <h3>Income Statistics</h3>                    
            <ol>    
                <li>Total Memberships Payments: {organization_data.get('total_membership_payments')}</li>
                <li>Total Paid : {organization_data.get('total_paid')}</li>
                <li>Balance: {organization_data.get('balance')}</li>
            </ol>
            
            <h4>Thank you</h4>
            <strong>{current_app.config.get('APP_NAME')}</strong>                
        '''

        email: str = user_data.get('email')
        if email_verified and bool(email):
            self._do_schedule_mail(to_email=email, subject=subject, text=text, html=html)

        message: str = "Bad Request Error: Email not verified please verify your account"
        raise RequestError(status=error_codes.bad_request_error_code, description=message)


class Validators(OrgValidators, OrganizationEmails):
    """
    **Class Validators**
    validation methods & Utils  for organizations
    """
    # TODO Finish this methods up
    def __init__(self) -> None:
        super(Validators, self).__init__()

    def _can_view_organization(self, organization_id: str, uid: str) -> bool:
        """

        :param organization_id:
        :param uid:
        :return:
        """
        pass

    def _can_create_organization(self, uid: Optional[str], organization_name: Optional[str]) -> bool:
        """
            **_can_create_organization**
                check if user has registered, and is a paying user... or created an account.
                Note: also Insures that the user does not have an organization already.

        :param uid: user id of the user performing the action --
        :param organization_name: the name of the organization to of which we should check if we can create
        :return: a boolean indicating if we can create the organization
        """
        # TODO - complete can create organization account
        pass

    def _can_update_organization(self, uid: Optional[str], organization_id: Optional[str]) -> bool:
        """
            **_can_update_organization**
                check if user has administrator rights on organization and if organization exist

            :param uid: the user performing this action
            :param organization_id: the organization_id of the organization to be updated
            :return: returns a response , status code tuple
        """
        # TODO - complete _can_update_organization organization account
        pass

    @handle_store_errors
    def _create_org_id(self) -> str:
        """
            **_create_org_id**
                create a valid organization_id if theres a conflict it creates another one and checks again if there is no
                conflict it returns the organization_id

        :return: organization_id
        """
        organization_id: str = create_id()
        org_instance: Optional[Organization] = Organization.query(Organization.organization_id == organization_id).get()
        # NOTE: Calling the function again to create a new key if present key is being used or return un-used key
        _not_organization: bool = not isinstance(org_instance, Organization) or not bool(org_instance)
        return organization_id if _not_organization else self._create_org_id()

    @staticmethod
    @handle_requests_errors
    def _create_org_wallet(organization_id: Optional[str], uid: Optional[str], currency: Optional[str],
                           paypal_address: Optional[str]) -> str:
        """
            _private function to facilitate the create of organizational wallet
            :param organization_id: id of the organization to create organization wallet
            :return: the wallet key of the created organization wallet

            send request to : /api/v1/wallet/organization
            with organization_id and uid on json body

        """
        _endpoint: str = '_api/v1/internal/wallet/organization'
        base_url: str = current_app.config.get('BASE_URL')
        request_url: str = f'{base_url}{_endpoint}'

        json_body = dict(organization_id=organization_id, uid=uid, currency=currency, paypal_address=paypal_address)

        response, _ = requests.post(url=request_url, json=json_body)
        # NOTE no need to check status if the method continues execution wallet is created
        payload: dict = response.json().get('payload')
        return payload.get('wallet_id')


class OrganizationView(Validators):
    """
        **Class OrganizationView**
            Utilities to validate UserInput Data and also validate access rights of those using the API, While
            accessing and manipulating information related to Client Organization.
    """
    def __init__(self) -> None:
        super(OrganizationView, self).__init__()
        self._max_retries: int = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout: int = current_app.config.get('DATASTORE_TIMEOUT')

    def __add_schedules(self, organization_id, uid):
        # NOTE: scheduling cache deletions
        _kwargs: dict = dict(org_view=OrganizationView, organization_id=organization_id)
        app_cache._schedule_cache_deletion(func=app_cache._delete_organization_cache, kwargs=_kwargs)
        _schedule_kwargs: dict = dict(organization_id=organization_id, uid=uid)
        self._base_email_scheduler(func=self.send_organization_updated_email, kwargs=_schedule_kwargs)

    @use_context
    @handle_view_errors
    def create_organization(self, uid: Optional[str], organization_name: Optional[str], description: Optional[str],
                            currency: Optional[str], paypal_address: Optional[str], home_url: Optional[str],
                            login_callback_url: Optional[str], recovery_callback_url: Optional[str]) -> tuple:
        """

            :param recovery_callback_url:
            :param login_callback_url:
            :param home_url:
            :param paypal_address:
            :param currency:
            :param uid: user_id of the user creating the organization
            :param organization_name: the name of the organization being created
            :param description: the description of the organization to be created
        :return: tuple containing response object and status code
        """
        # Note: insures that a valid organization id is created
        organization_id: Optional[str] = self._create_org_id()

        # if organization_id == None
        if not bool(organization_id):
            message: str = "unable to create a valid organization_id - please try again later"
            raise InputError(status=error_codes.input_error_code, description=message)

        wallet_id: Optional[str] = self._create_org_wallet(organization_id=organization_id, uid=uid, currency=currency,
                                                           paypal_address=paypal_address)

        # if wallet_id is None
        if not bool(wallet_id):
            message: str = "Unable to create a organization wallet - please try again later"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        if not isinstance(description, str) or not bool(description.strip()):
            message: str = "description is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if self._can_create_organization(uid, organization_name) is True:
            organization_instance: Organization = Organization(owner_uid=uid,
                                                               organization_id=organization_id,
                                                               wallet_id=wallet_id,
                                                               organization_name=organization_name,
                                                               description=description,
                                                               total_affiliates=0,
                                                               total_paid=AmountMixin(amount=0),
                                                               total_members=0,
                                                               projected_membership_payments=AmountMixin(amount=0),
                                                               total_membership_payments=AmountMixin(amount=0),
                                                               home_url=home_url, login_callback_url=login_callback_url,
                                                               recovery_callback_url=recovery_callback_url)

            key: Optional[ndb.Key] = organization_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not isinstance(key, ndb.Key):
                message: str = "Database Error: could not create or update organization - please inform Admin"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            self.__add_schedules(organization_id, uid)

            message: str = "Successfully created Organization"
            return jsonify(dict(status=True,
                                payload=organization_instance.to_dict(),
                                message=message)), status_codes.successfully_updated_code

        message: str = "Operation Denied: Unable to create organization"
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    @use_context
    @handle_view_errors
    def update_organization(self, uid: Optional[str], organization_id: Optional[str],
                            organization_name: Optional[str], description: Optional[str], home_url: Optional[str],
                            login_callback_url: Optional[str], recovery_callback_url:  Optional[str]) -> tuple:
        """
            **update_organization**
                function used to update the name and description of an organization.

            :param recovery_callback_url:
            :param login_callback_url:
            :param home_url:
            :param uid: user id of the user updating the organization
            :param organization_id: the id of the organization being updated, this id has to exist first
            :param organization_name: the name the organization will be updated to
            :param description: the description the organization will be updated to
            :return: tuple containing response and status code
        """
        if not isinstance(description, str) or not bool(description.strip()):
            message: str = "description is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(organization_name, str) or not bool(organization_name.strip()):
            message: str = "organization_name is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        # NOTE: returns true if user has sufficient rights to update organization.
        if not self._can_update_organization(uid=uid, organization_id=organization_id):
            message: str = "You are not allowed to edit that organization please contact administrator"
            raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

        organization_instance: Optional[Organization] = Organization.query(
            Organization.organization_id == organization_id).get()

        if not isinstance(organization_instance, Organization) and bool(organization_instance):
            message: str = "Organization not found: Unable to update Organization"
            return jsonify(dict(status=False, message=message)),  status_codes.data_not_found_code

        organization_instance.organization_name = organization_name
        organization_instance.description = description
        organization_instance.home_url = home_url
        organization_instance.login_callback_url = login_callback_url
        organization_instance.recovery_callback_url = recovery_callback_url

        key: Optional[ndb.Key] = organization_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not isinstance(key, ndb.Key):
            message: str = "Database Error: could not create or update organization - please inform Admin"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        self.__add_schedules(organization_id, uid)

        message: str = "Successfully updated organization"
        return jsonify(dict(status=True,
                            payload=organization_instance.to_dict(),
                            message=message)), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def get_organization(self, organization_id: Optional[str], uid: Optional[str]) -> tuple:
        """
            **get_organization**
                function used to return the details of user organization,
            :param uid:
            :param organization_id: required: the id of the organization to return
            :return: response object and status code, response contains ,
            response json {'status': True, 'payload': '{Organization}', 'message' : 'success'}, 200
        """
        # NOTE: may not need to check if user can access organization details if the function is being called on behalf
        # of the system

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not self._can_view_organization(organization_id=organization_id, uid=uid):
            message: str = "Authentication Error: you are not authorized to view or edit this organization"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        organization_instance: Optional[Organization] = Organization.query(
            Organization.organization_id == organization_id, Organization.uid == uid).get()

        if not isinstance(organization_instance, Organization) or not bool(organization_instance):
            message: str = "Unable to retrieve organization"
            return jsonify(dict(status=False, message=message)),  status_codes.data_not_found_code

        message: str = 'successfully fetched organization'
        return jsonify(dict(status=True,
                            payload=organization_instance.to_dict(),
                            message=message)), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def _return_all_organizations(self) -> tuple:
        """
            **_return_all_organizations**
                _private (can be used by system or system admin) function to retrieve all
                organization details used by system and Application Administrator

            :return: a list containing all organization details
        """
        organizations_list: List[dict] = [org.to_dict() for org in Organization.query().fetch()]
        if organizations_list:
            message: str = 'successfully retrieved organizations'
            return jsonify(dict(status=True, payload=organizations_list, message=message)), status_codes.status_ok_code

        message: str = 'Data Not found: there are presently no organizations defined'
        return jsonify(dict(status=True, message=message)), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def _get_organizations(self, organization_id: Optional[str]) -> tuple:
        """
            **_return_all_organizations**
                _private (can only be used by system and system admin)
                retrieve a specific organization detail

            :return: a list containing all organization details
        """
        organization_instance: Optional[Organization] = Organization.query(
            Organization.organization_id == organization_id).get()

        if isinstance(organization_instance, Organization) and bool(organization_instance):
            message: str = 'successfully retrieved organizations'
            return jsonify(dict(status=True,
                                payload=organization_instance.to_dict(),
                                message=message)), status_codes.successfully_updated_code

        message: str = 'successfully fetched organization'
        return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def _update_affiliate_count(self, organization_id: Optional[str], add: Optional[int] = None,
                                subtract: Optional[int] = None) -> tuple:
        """
            **_update_affiliate_count**
                Private Function: this function will never be called externally or by the user.

                a function to update the affiliate count of organization instance, must be called each time there is a change_membership
                in the total number of affiliates belonging to an organization.

            :param organization_id: the id of the organization of which the total affiliates has to be updated.
            :param add: Optional amount to add, if you want to subtract pass None to this value and integer to sub
            :param subtract: Optional amount to subtract, if you want to add pass None to this value and integer to add
            :return: tuple containing response and status code.
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_instance: Optional[Organization] = Organization.query(
            Organization.organization_id == organization_id).get()

        if not isinstance(organization_instance, Organization) or not bool(organization_instance):
            message: str = "data not found : cannot update affiliate count"
            return jsonify(dict(status=False, message=message)),  status_codes.data_not_found_code

        if isinstance(subtract, int):
            organization_instance.total_affiliates -= subtract
        elif isinstance(add, int):
            organization_instance.total_affiliates += add
        else:
            message: str = "Please either enter the amount to subtract or add"
            raise InputError(status=error_codes.input_error_code, description=message)

        key: Optional[ndb.Key] = organization_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not isinstance(key, ndb.Key):
            message: str = "An Unspecified error occurred while adding to or subtract from affiliate count"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)
        # NOTE: scheduling cache deletions
        _kwargs: dict = dict(org_view=OrganizationView, organization_id=organization_id)
        app_cache._schedule_cache_deletion(func=app_cache._delete_organization_cache, kwargs=_kwargs)

        message: str = "Successfully updated affiliate count"
        return jsonify(dict(status=True,
                            payload=organization_instance.to_dict(),
                            message=message)), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def _update_total_paid(self, organization_id: Optional[str],
                           add_amount: Optional[AmountMixin] = None,
                           subtract_amount: Optional[AmountMixin] = None) -> tuple:
        """
            **_update_total_paid**
                Private function to update the total amount paid by the organization.

                Supply either add_amount or sub_amount but not both, amounts shall be a class of AmountMixin and of the
                same currency

            :param organization_id: the id of the organization of which the add operation shall be performed
            :param add_amount: Optional pass add_amount <AmountMixin> to add or None otherwise
            :param subtract_amount: Optional pass sub_amount as <AmountMixin> to subtract or None otherwise

            :return: tuple containing response and status code

        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_instance: Optional[Organization] = Organization.query(Organization.organization_id == organization_id).get()

        if not (isinstance(organization_instance, Organization) and bool(organization_instance)):
            message: str = "Organization not found: cannot update total_paid"
            return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

        calculated: bool = False
        if isinstance(add_amount, AmountMixin):
            organization_instance.total_paid.__add__(add_amount)
            calculated = True
        if isinstance(subtract_amount, AmountMixin):
            organization_instance.total_paid.__sub__(subtract_amount)
            calculated = True
        if not calculated:
            message: str = "Please enter either the amount to add or subtract"
            raise InputError(status=error_codes.input_error_code, description=message)

        key: Optional[ndb.Key] = organization_instance.put(retries=self._max_retries, timeout=self._max_timeout)

        if not isinstance(key, ndb.Key):
            message: str = 'for some reason we are unable to add to total_amount'
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        # NOTE: scheduling cache deletions
        _kwargs: dict = dict(org_view=OrganizationView, organization_id=organization_id)
        app_cache._schedule_cache_deletion(func=app_cache._delete_organization_cache, kwargs=_kwargs)

        message: str = "Successfully updated total paid amount on Organization"
        return jsonify(dict(status=True,
                            payload=organization_instance.to_dict(),
                            message=message)), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def _update_total_members(self, organization_id: Optional[str], add: Optional[int] = None,
                              subtract: Optional[int] = None) -> tuple:
        """
            **_update_total_members**
                supply either the amount to add to total members or the amount to subtract
                Amounts should be integers

            :param organization_id:
            :param add: Optional > amount to add <int> or else pass None
            :param subtract: Optional > amount to subtract <int> or else pass None
            :return: tuple containing response code and status
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_instance: Optional[Organization] = Organization.query(
            Organization.organization_id == organization_id).get()

        if not isinstance(organization_instance, Organization) or not bool(organization_instance):
            message: str = "Unable to update organization"
            return jsonify(dict(status=False, message=message)),  status_codes.data_not_found_code

        if subtract:
            organization_instance.total_members -= subtract
        elif add:
            organization_instance.total_members += add
        else:
            raise InputError(status=error_codes.input_error_code,
                             description="Please Enter either the amount to add or subtract")

        # NOTE: scheduling cache deletions
        _kwargs: dict = dict(org_view=OrganizationView, organization_id=organization_id)
        app_cache._schedule_cache_deletion(func=app_cache._delete_organization_cache, kwargs=_kwargs)

        message: str = "Successfully updated total members on organization"
        return jsonify(dict(status=True,
                            payload=organization_instance.to_dict(),
                            message=message)), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def _update_projected_membership_payments(self, organization_id: Optional[str],
                                              add_payment: Optional[str] = None,
                                              subtract_payment: Optional[str] = None) -> tuple:

        """
            # TODO update projected memberships payments may need revision - or can be implemented as a property

            **_update_projected_membership_payments**
                to update projected_membership_payments supply either the amount to add or subtract but not both

            :param organization_id:
            :param add_payment: Optional payment amount to Add type <AmountMixin> or pass None
            :param subtract_payment: Optional payment amount to Subtract <AmountMixin>, or Pass None
            :return: tuple
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_instance: Optional[Organization] = Organization.query(
            Organization.organization_id == organization_id).get()

        if not isinstance(organization_instance, Organization) or not bool(organization_instance):
            message: str = 'Unable to update projected_membership_payments'
            return jsonify(dict(status=False, message=message)),  status_codes.data_not_found_code

        if isinstance(add_payment, AmountMixin):
            organization_instance.projected_membership_payments.__add__(add_payment)
        elif isinstance(subtract_payment, AmountMixin):
            organization_instance.projected_membership_payments.__sub__(subtract_payment)
        else:
            message: str = "Please enter either the amount to add or subtract"
            raise InputError(status=error_codes.input_error_code, description=message)

        # NOTE: scheduling cache deletions
        _kwargs: dict = dict(org_view=OrganizationView, organization_id=organization_id)
        app_cache._schedule_cache_deletion(func=app_cache._delete_organization_cache, kwargs=_kwargs)

        message: str = "Successfully updated projected_membership_payments"
        return jsonify(dict(status=True,
                            payload=organization_instance.to_dict(),
                            message=message)), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def _update_total_membership_payments(self, organization_id: Optional[str],
                                          subtract_total_membership_payment: Optional[AmountMixin] = None,
                                          add_total_membership_amount: Optional[AmountMixin] = None) -> tuple:
        """
            **_update_total_membership_payments**
                update overall total_membership_payments for organization, supply either the amount to add or substract
                but not both

            :param organization_id: the id of the organization to update the total memberships
            :param subtract_total_membership_payment: amount to subtract
            :param add_total_membership_amount: amount to add
            :return: react a response and status code tuple
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_instance: Optional[Organization] = Organization.query(
            Organization.organization_id == organization_id).get()

        if not isinstance(organization_instance, Organization) or not bool(organization_instance):
            message: str = "Organization Not Found: Unable to update total membership payments"
            return jsonify(dict(status=False, message=message)),  status_codes.data_not_found_code

        if isinstance(subtract_total_membership_payment, AmountMixin):
            organization_instance.total_membership_payments.__sub__(subtract_total_membership_payment)
        elif isinstance(add_total_membership_amount, AmountMixin):
            organization_instance.total_membership_payments.__add__(add_total_membership_amount)
        else:
            message: str = "Input Error: Please enter either the amount to add or subtract"
            raise InputError(status=error_codes.input_error_code,
                             description=message)

        # NOTE: scheduling cache deletions
        _kwargs: dict = dict(org_view=OrganizationView, organization_id=organization_id)
        app_cache._schedule_cache_deletion(func=app_cache._delete_organization_cache, kwargs=_kwargs)

        message: str = "Successfully updated total_membership_payments"
        return jsonify(dict(status=True,
                            payload=organization_instance.to_dict(),
                            message=message)), status_codes.successfully_updated_code

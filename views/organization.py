***REMOVED***
** Module - Organization View Controller **
    enables users to add , update Organization Accounts
***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import json
import typing
from typing import Optional
import requests
from flask import current_app, jsonify
from _sdk._email import Mailgun
from config.exception_handlers import handle_view_errors, handle_store_errors
from config.exceptions import InputError, DataServiceError, error_codes, status_codes, UnAuthenticatedError
from config.use_context import use_context
from database.mixins import AmountMixin
from database.organization import Organization, OrgValidators
# TODO finish up organization  view
from main import app_cache
from utils.utils import create_id, return_ttl
from views.cache_manager import CacheManager


class OrganizationEmails(Mailgun):
    ***REMOVED***
        **Class OrganizationEmails**
            class Used to send Emails and Notifications related to Organizations
    ***REMOVED***

    def __init__(self):
        super(OrganizationEmails, self).__init__()

    def __do_send_mail(self, to_email: str, subject: str, text: str, html: str) -> None:
        ***REMOVED***
            **__do_send_mail**
                If possible this method should be run asynchronously
                a method to actually send email

            :param to_email: email address to send the email to
            :param subject: subject of the email
            :param text: body in text format
            :param html: body in html format
            :return: does not return anything
        ***REMOVED***
        self.__send_with_mailgun_rest_api(to_list=[to_email], subject=subject, text=text, html=html)

    def send_successfully_created_organization(self, organization_id: str, uid: str) -> None:
        ***REMOVED***
            **send_successfully_created_organization**
                once an organization is created send an email of this to the end user explaining the steps
                they need to perform in order to complete the transaction

            :param organization_id:
            :param uid:
            :return:
        ***REMOVED***
        pass

    def send_organization_wallet_created_email(self, organization_id: str, uid: str) -> None:
        ***REMOVED***
            **organization_wallet_created**
                send an email when an organization wallet has been created
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        pass


class OrganizationView(OrgValidators, OrganizationEmails, CacheManager):
    ***REMOVED***
        **OrganizationView**
            Utilities to validate UserInput Data and also validate access rights of those using the API, While
            accessing and manipulating information related to Client Organization.
    ***REMOVED***
    def __init__(self):
        super(OrganizationView, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    def can_create_organization(self, uid: Optional[str], organization_name: Optional[str]) -> bool:
        ***REMOVED***
            **can_create_organization**
                check if user has registered, and is a paying user... or created an account.
                Note: also Insures that the user does not have an organization already.

        :param uid: user id of the user performing the action
        :param organization_name: the name of the organization to of which we should check if we can create
        :return: a boolean indicating if we can create the organization
        ***REMOVED***
        # TODO - complete can create organization account
        pass

    def can_update_organization(self, uid: Optional[str], organization_id: Optional[str]) -> bool:
        ***REMOVED***
            **can_update_organization**
                check if user has administrator rights on organization and if organization exist

            :param uid: the user performing this action
            :param organization_id: the organization_id of the organization to be updated
            :return: returns a response , status code tuple
        ***REMOVED***
        # TODO - complete can_update_organization organization account
        pass

    @handle_store_errors
    def _create_org_id(self) -> str:
        ***REMOVED***
            **_create_org_id**
                create a valid organization_id if theres a conflict it creates another one and checks again if there is no
                conflict it returns the organization_id

        :return: organization_id
        ***REMOVED***
        organization_id: str = create_id()
        org_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()
        if isinstance(org_instance, Organization):
            # NOTE: Calling the function again to create a new key the present key is being used
            self._create_org_id()
        return organization_id

    @staticmethod
    def _create_org_wallet(organization_id: Optional[str], uid: Optional[str], currency: Optional[str],
                           paypal_address: Optional[str]) -> str:
        ***REMOVED***
            _private function to facilitate the create of organizational wallet
            :param organization_id: id of the organization to create organization wallet
            :return: the wallet key of the created organization wallet

            send request to : /api/v1/wallet/organization
            with organization_id and uid on json body

        ***REMOVED***
        _endpoint: str = 'api/v1/wallet/organization'
        base_url: str = current_app.config.get('BASE_URL')
        request_url: str = "{}{}".format(base_url, _endpoint)

        json_body = json.dumps(dict(organization_id=organization_id, uid=uid, currency=currency,
                                    paypal_address=paypal_address))

        response, _ = requests.post(url=request_url, json=json_body)
        # NOTE no need to check status if the method continues execution wallet is created
        return response.to_dict().get('payload')('wallet_id')

    @use_context
    @handle_view_errors
    def create_organization(self, uid: Optional[str], organization_name: Optional[str], description: Optional[str],
                            currency: Optional[str], paypal_address: Optional[str], home_url: Optional[str],
                            login_callback_url: Optional[str], recovery_callback_url: Optional[str]) -> tuple:
        ***REMOVED***

            :param recovery_callback_url:
            :param login_callback_url:
            :param home_url:
            :param paypal_address:
            :param currency:
            :param uid: user_id of the user creating the organization
            :param organization_name: the name of the organization being created
            :param description: the description of the organization to be created
        :return: tuple containing response object and status code
        ***REMOVED***
        # Note: insures that a valid organization id is created
        organization_id: Optional[str] = self._create_org_id()

        # if organization_id == None
        if not bool(organization_id):
            message: str = "unable to create a valid organization_id - please try again later"
            raise InputError(status=error_codes.input_error_code, description=message)

        # TODO- this function needs to be completed
        wallet_id: Optional[str] = self._create_org_wallet(organization_id=organization_id, uid=uid, currency=currency,
                                                           paypal_address=paypal_address)

        # if wallet_id is None
        if not bool(wallet_id):
            message: str = "unable to create a valid wallet_id - please try again later"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(description, str) or not bool(description.strip()):
            message: str = "description is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if self.can_create_organization(uid, organization_name) is True:
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

            key: Optional[str] = organization_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "An Unspecified Error has occurred creating database"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            self.__delete_organization_cache(org_view=OrganizationView, organization_id=organization_id)

            message: str = "Successfully created Organization"
            return jsonify({'status': True, 'payload': organization_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = "Operation Denied: Unable to create organization"
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    @use_context
    @handle_view_errors
    def update_organization(self, uid: Optional[str], organization_id: Optional[str],
                            organization_name: Optional[str], description: Optional[str], home_url: Optional[str],
                            login_callback_url: Optional[str], recovery_callback_url:  Optional[str]) -> tuple:
        ***REMOVED***
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
        ***REMOVED***
        if not isinstance(description, str) or not bool(description.strip()):
            message: str = "description is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(organization_name, str) or not bool(organization_name.strip()):
            message: str = "organization_name is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        # NOTE: returns true if user has sufficient rights to update organization.
        if self.can_update_organization(uid=uid, organization_id=organization_id):

            org_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()
            if isinstance(org_instance, Organization):
                org_instance.organization_name = organization_name
                org_instance.description = description
                org_instance.home_url = home_url
                org_instance.login_callback_url = login_callback_url
                org_instance.recovery_callback_url = recovery_callback_url

                key = org_instance.put(retries=self._max_retries, timeout=self._max_timeout)
                if not bool(key):
                    message: str = "An Unspecified Error has occurred"
                    raise DataServiceError(status=error_codes.data_service_error_code, description=message)

                # Delete Return all organizations
                self.__delete_organization_cache(org_view=OrganizationView, organization_id=organization_id)

                message: str = "Successfully updated organization"
                return jsonify({'status': True, 'payload': org_instance.to_dict(),
                                'message': message}), status_codes.successfully_updated_code

            message: str = "Organization not found: Unable to update Organization"
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

        message: str = "You are not allowed to edit that organization please contact administrator"
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    def get_organization(self, organization_id: Optional[str], uid: Optional[str]) -> tuple:
        ***REMOVED***
            **get_organization**
                function used to return the details of user organization,
            :param uid:
            :param organization_id: required: the id of the organization to return
            :return: response object and status code, response contains ,
            response json {'status': True, 'payload': '{Organization}', 'message' : 'success'}, 200
        ***REMOVED***
        # NOTE: may not need to check if user can access organization details if the function is being called on behalf
        # of the system
        # TODO find out how i can authenticate this call for instance i need to ensure that the user is
        #  authorized to view organization details, using uid

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_instance: Organization = Organization.query(Organization.organization_id == organization_id,
                                                                 Organization.uid == uid).get()
        if isinstance(organization_instance, Organization):
            message: str = 'successfully fetched organization'
            return jsonify({'status': True,
                            'payload': organization_instance.to_dict(),
                            'message': message}), status_codes.status_ok_code

        message: str = "Unable to retrieve organization"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    def _return_all_organizations(self) -> tuple:
        ***REMOVED***
            **_return_all_organizations**
                _private (can be used by system or system admin) function to retrieve all
                organization details used by system and Application Administrator

            :return: a list containing all organization details
        ***REMOVED***
        organizations_list: typing.List[dict] = [org.to_dict() for org in Organization.query().fetch()]
        if len(organizations_list):
            message: str = 'successfully retrieved organizations'
            return jsonify({'status': True,
                            'payload': organizations_list, 'message': message}), status_codes.status_ok_code

        message: str = 'successfully retrieved organizations'
        return jsonify({'status': True, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    def _get_organizations(self, organization_id: Optional[str]) -> tuple:
        ***REMOVED***
            **_return_all_organizations**
                _private (can only be used by system and system admin)
                retrieve a specific organization detail

            :return: a list containing all organization details
        ***REMOVED***
        organization_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()
        if isinstance(organization_instance, Organization):
            message: str = 'successfully retrieved organizations'
            return jsonify({'status': True,
                            'payload': organization_instance.to_dict(),
                            'message': message}), status_codes.status_ok_code

        message: str = 'successfully fetched organization'
        return jsonify({'status': True, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def _update_affiliate_count(self, organization_id: Optional[str], add: Optional[int] = None,
                                sub: Optional[int] = None) -> tuple:
        ***REMOVED***
            **_update_affiliate_count**
                Private Function: this function will never be called externally or by the user.

                a function to update the affiliate count of organization instance, must be called each time there is a change_membership
                in the total number of affiliates belonging to an organization.

            :param organization_id: the id of the organization of which the total affiliates has to be updated.
            :param add: Optional amount to add, if you want to subtract pass None to this value and integer to sub
            :param sub: Optional amount to subtract, if you want to add pass None to this value and integer to add
            :return: tuple containing response and status code.
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()
        if isinstance(organization_instance, Organization):
            if isinstance(sub, int):
                organization_instance.total_affiliates -= sub
            elif isinstance(add, int):
                organization_instance.total_affiliates += add
            else:
                raise InputError(status=500, description="Please either enter the amount to subtract or add")

            key: Optional[str] = organization_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "An Unspecified error occurred while adding to or subtract from affiliate count"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            self.__delete_organization_cache(org_view=OrganizationView, organization_id=organization_id)

            message: str = "Successfully updated affiliate count"
            return jsonify({'status': False,
                            'payload': organization_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = "data not found : cannot update affiliate count"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def _update_total_paid(self, organization_id: Optional[str],
                           add_amount: Optional[AmountMixin] = None,
                           sub_amount: Optional[AmountMixin] = None) -> tuple:
        ***REMOVED***
            **_update_total_paid**
                Private function to update the total amount paid by the organization.

                Supply either add_amount or sub_amount but not both, amounts shall be a class of AmountMixin and of the
                same currency

            :param organization_id: the id of the organization of which the add operation shall be performed
            :param add_amount: Optional pass add_amount <AmountMixin> to add or None otherwise
            :param sub_amount: Optional pass sub_amount as <AmountMixin> to subtract or None otherwise

            :return: tuple containing response and status code

        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()

        if isinstance(organization_instance, Organization):
            calculated: bool = False
            if isinstance(add_amount, AmountMixin):
                organization_instance.total_paid += add_amount
                calculated = True
            if isinstance(sub_amount, AmountMixin):
                organization_instance.total_paid -= sub_amount
                calculated = True
            if not calculated:
                raise InputError(status=500, description="Please enter either the amount to add or subtract")

            key: Optional[str] = organization_instance.put(retries=self._max_retries, timeout=self._max_timeout)

            if not bool(key):
                message: str = 'for some reason we are unable to add to total_amount'
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            self.__delete_organization_cache(org_view=OrganizationView, organization_id=organization_id)

            message: str = "Successfully updated total paid amount on Organization"
            return jsonify({'status': True,
                            'payload': organization_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = "Organization not found: cannot update total_paid"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def _update_total_members(self, organization_id: Optional[str], add: Optional[int] = None,
                              sub: Optional[int] = None) -> tuple:
        ***REMOVED***
            **_update_total_members**
                supply either the amount to add to total members or the amount to subtract
                Amounts should be integers

            :param organization_id:
            :param add: Optional > amount to add <int> or else pass None
            :param sub: Optional > amount to subtract <int> or else pass None
            :return: tuple containing response code and status
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()

        if isinstance(organization_instance, Organization):
            if sub:
                organization_instance.total_members += sub
            elif add:
                organization_instance.total_members -= add
            else:
                raise InputError(status=error_codes.input_error_code,
                                 description="Please Enter either the amount to add or subtract")

            self.__delete_organization_cache(org_view=OrganizationView, organization_id=organization_id)

            message: str = "Successfully updated total members on organization"
            return jsonify({'status': True,
                            'payload': organization_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = "Unable to update organization"
        return jsonify({'status': True, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def _update_projected_membership_payments(self, organization_id: Optional[str],
                                              add_payment: Optional[str] = None,
                                              sub_payment: Optional[str] = None) -> tuple:

        ***REMOVED***
            # TODO update projected memberships payments may need revision - or can be implemented as a property

            **_update_projected_membership_payments**
                to update projected_membership_payments supply either the amount to add or subtract but not both

            :param organization_id:
            :param add_payment: Optional payment amount to Add type <AmountMixin> or pass None
            :param sub_payment: Optional payment amount to Subtract <AmountMixin>, or Pass None
            :return: tuple
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()

        if isinstance(organization_instance, Organization):
            if isinstance(add_payment, AmountMixin):
                organization_instance.projected_membership_payments += add_payment
            elif isinstance(sub_payment, AmountMixin):
                organization_instance.projected_membership_payments -= sub_payment
            else:
                message: str = "Please enter either the amount to add or subtract"
                raise InputError(status=error_codes.input_error_code, description=message)

            self.__delete_organization_cache(org_view=OrganizationView, organization_id=organization_id)

            message: str = "Successfully updated projected_membership_payments"
            return jsonify({'status': True,
                            'payload': organization_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = 'Unable to update projected_membership_payments'
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def _update_total_membership_payments(self, organization_id: Optional[str],
                                          sub_total_membership_payment: Optional[AmountMixin] = None,
                                          add_total_membership_amount: Optional[AmountMixin] = None) -> tuple:
        ***REMOVED***
            **_update_total_membership_payments**
                update overall total_membership_payments for organization, supply either the amount to add or substract
                but not both

            :param organization_id: the id of the organization to update the total memberships
            :param sub_total_membership_payment: amount to subtract
            :param add_total_membership_amount: amount to add
            :return: react a response and status code tuple
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()

        if isinstance(organization_instance, Organization):
            if isinstance(sub_total_membership_payment, AmountMixin):
                organization_instance.total_membership_payments += sub_total_membership_payment
            elif isinstance(add_total_membership_amount, AmountMixin):
                organization_instance.total_membership_payments += add_total_membership_amount
            else:
                message: str = "Input Error: Please enter either the amount to add or subtract"
                raise InputError(status=error_codes.input_error_code,
                                 description=message)

            self.__delete_organization_cache(org_view=OrganizationView, organization_id=organization_id)

            message: str = "Successfully updated total_membership_payments"
            return jsonify({'status': True,
                            'payload': organization_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = "Organization Not Found: Unable to update total membership payments"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

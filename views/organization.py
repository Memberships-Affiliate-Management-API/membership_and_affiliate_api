***REMOVED***
organization view
    enables users to add , update Organization Accounts
***REMOVED***
import typing
from flask import current_app, jsonify
from _sdk._email import Mailgun
from config.exception_handlers import handle_view_errors
from config.exceptions import InputError, DataServiceError, error_codes, status_codes, UnAuthenticatedError
from config.use_context import use_context
from database.mixins import AmountMixin
from database.organization import Organization, OrgValidators
# TODO finish up organization  view
from main import app_cache
from utils.utils import create_id, return_ttl, can_cache


class OrganizationEmails(Mailgun):
    ***REMOVED***
        class Used to send Emails and Notifications related to Organizations
    ***REMOVED***

    def __init__(self):
        super(OrganizationEmails, self).__init__()

    def __do_send_mail(self, to_email: str, subject: str, text: str, html: str) -> None:
        ***REMOVED***
              **If possible this method should be run asynchronously**
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
            once an organization is created send an email of this to the end user explaining the steps
            they need to perform in order to complete the transaction
            :param organization_id:
            :param uid:
            :return:
        ***REMOVED***
        pass

    def organization_wallet_created(self, organization_id: str, uid: str) -> None:
        ***REMOVED***
            send an email when an organization wallet has been created
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        pass


class OrganizationView(OrgValidators, OrganizationEmails):
    ***REMOVED***
     Utilities to validate UserInput Data and also validate access rights of those using the API, While
     accessing and manipulating information related to Client Organization.
    ***REMOVED***
    def __init__(self):
        super(OrganizationView, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    def can_create_organization(self, uid: typing.Union[str, None],
                                organization_name: typing.Union[str, None]) -> bool:
        ***REMOVED***
            NOTE: check if user has registered, and is a paying user... or created an account.
            # Note: also Insures that the user does not have an organization already.
        :param uid: user id of the user performing the action
        :param organization_name: the name of the organization to of which we should check if we can create
        :return: a boolean indicating if we can create the organization
        ***REMOVED***
        # TODO - complete can create organization account
        pass

    def can_update_organization(self, uid: typing.Union[str, None], organization_id: typing.Union[str, None]) -> bool:
        ***REMOVED***
            check if user has administrator rights on organization and if organization exist
            :param uid: the user performing this action
            :param organization_id: the organization_id of the organization to be updated
        :return: returns a response , status code tuple
        ***REMOVED***
        # TODO - complete can_update_organization organization account
        pass

    def _create_org_id(self) -> str:
        ***REMOVED***
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

    def _create_org_wallet(self, organization_id: typing.Union[str, None]) -> str:
        ***REMOVED***
            _private function to facilitate the create of organizational wallet
            :param organization_id: id of the organization to create organization wallet
            :return: the wallet key of the created organization wallet
        ***REMOVED***
        # TODO this function must call the wallet API to create organization wallet
        pass

    @use_context
    @handle_view_errors
    def create_organization(self, uid: typing.Union[str, None], organization_name: typing.Union[str, None],
                            description: typing.Union[str, None]) -> tuple:
        ***REMOVED***

            :param uid: user_id of the user creating the organization
            :param organization_name: the name of the organization being created
            :param description: the description of the organization to be created
        :return: tuple containing response object and status code
        ***REMOVED***
        # Note: insures that a valid organization id is created
        organization_id: str = self._create_org_id()
        # TODO- this function needs to be completed
        wallet_id: str = self._create_org_wallet(organization_id=organization_id)

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
                                                               total_membership_payments=AmountMixin(amount=0))

            key: typing.Union[str, None] = organization_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "An Unspecified Error has occurred creating database"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            message: str = "Successfully created Organization"
            return jsonify({'status': True, 'payload': organization_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = "Operation Denied: Unable to create organization"
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    @use_context
    @handle_view_errors
    def update_organization(self, uid: typing.Union[str, None], organization_id: typing.Union[str, None],
                            organization_name: typing.Union[str, None], description: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            function used to update the name and description of an organization.

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
        if self.can_update_organization(uid=uid, organization_id=organization_id) is True:

            org_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()
            if isinstance(org_instance, Organization):
                org_instance.organization_name = organization_name
                org_instance.description = description
                key = org_instance.put(retries=self._max_retries, timeout=self._max_timeout)
                if not bool(key):
                    message: str = "An Unspecified Error has occurred"
                    raise DataServiceError(status=error_codes.data_service_error_code, description=message)

                message: str = "Successfully updated organization"
                return jsonify({'status': True, 'payload': org_instance.to_dict(),
                                'message': message}), status_codes.successfully_updated_code

            message: str = "Organization not found: Unable to update Organization"
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

        message: str = "You are not allowed to edit that organization please contact administrator"
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_organization(self, uid: typing.Union[str, None], organization_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            function used to return the details of user organization,

            :param uid: required:  user id of the user requesting organization details
            :param organization_id: required: the id of the organization to return
        :return: response object and status code, response contains ,
        response json {'status': True, 'payload': '{Organization}', 'message' : 'success'}, 200
        ***REMOVED***
        # NOTE: may not need to check if user can access organization details if the function is being called on behalf
        # of the system
        organization_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()
        if isinstance(organization_instance, Organization):
            message: str = 'successfully fetched organization'
            return jsonify({'status': True,
                            'payload': organization_instance.to_dict(),
                            'message': message}), status_codes.status_ok_code

        message: str = "Unable to retrieve organization"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def _return_all_organizations(self) -> tuple:
        ***REMOVED***
            _private function to retrieve all organization details used by system and Application Administrator
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
    def _update_affiliate_count(self, organization_id: typing.Union[str, None], add: typing.Union[int, None] = None,
                                sub: typing.Union[int, None] = None) -> tuple:
        ***REMOVED***
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

            key: typing.Union[str, None] = organization_instance.put(retries=self._max_retries,
                                                                     timeout=self._max_timeout)
            if not bool(key):
                message: str = "An Unspecified error occurred while adding to or subtract from affiliate count"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            message: str = "Successfully updated affiliate count"
            return jsonify({'status': False,
                            'payload': organization_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = "data not found : cannot update affiliate count"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def _update_total_paid(self, organization_id: typing.Union[str, None],
                           add_amount: typing.Union[AmountMixin, None] = None,
                           sub_amount: typing.Union[AmountMixin, None] = None) -> tuple:
        ***REMOVED***
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
            if isinstance(add_amount, AmountMixin):
                organization_instance.total_paid += add_amount
            elif isinstance(sub_amount, AmountMixin):
                organization_instance.total_paid -= add_amount
            else:
                raise InputError(status=500, description="Please enter either the amount to add or subtract")

            key: typing.Union[str, None] = organization_instance.put(retries=self._max_retries,
                                                                     timeout=self._max_timeout)

            if not bool(key):
                message: str = 'for some reason we are unable to add to total_amount'
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            message: str = "Successfully updated total paid amount on Organization"
            return jsonify({'status': True,
                            'payload': organization_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = "Organization not found: cannot update total_paid"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def _update_total_members(self, organization_id: typing.Union[str, None], add: typing.Union[int, None] = None,
                              sub: typing.Union[int, None] = None) -> tuple:
        ***REMOVED***
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
            if isinstance(sub, int):
                organization_instance.total_members += add
            elif isinstance(add, int):
                organization_instance.total_members -= sub
            else:
                raise InputError(status=error_codes.input_error_code,
                                 description="Please Enter either the amount to add or subtract")

            message: str = "Successfully updated total members on organization"
            return jsonify({'status': True,
                            'payload': organization_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = "Unable to update organization"
        return jsonify({'status': True, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def _update_projected_membership_payments(self, organization_id: typing.Union[str, None],
                                              add_payment: typing.Union[str, None] = None,
                                              sub_payment: typing.Union[str, None] = None) -> tuple:

        ***REMOVED***
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
                message : str = "Please enter either the amount to add or subtract"
                raise InputError(status=error_codes.input_error_code, description=message)

            message: str = "Successfully updated projected_membership_payments"
            return jsonify({'status': True,
                            'payload': organization_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = 'Unable to update projected_membership_payments'
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def _update_total_membership_payments(self, organization_id: typing.Union[str, None],
                                          sub_total_membership_payment: typing.Union[AmountMixin, None] = None,
                                          add_total_membership_amount: typing.Union[AmountMixin, None] = None) -> tuple:
        ***REMOVED***
            update overall total_membership_payments for organization, supply either the amount to add or subsctract
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

            message: str = "Successfully updated total_membership_payments"
            return jsonify({'status': True,
                            'payload': organization_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = "Organization Not Found: Unable to update total membership payments"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

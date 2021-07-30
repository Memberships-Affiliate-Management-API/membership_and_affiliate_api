***REMOVED***
organization view
    enables users to add , update Organization Accounts
***REMOVED***
import typing
from flask import current_app, jsonify
from config.exception_handlers import handle_view_errors
from config.exceptions import InputError, DataServiceError
from config.use_context import use_context
from database.mixins import AmountMixin
from database.organization import Organization, OrgValidators
# TODO finish up organization  view
from utils.utils import create_id


class OrganizationView(OrgValidators):
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
            check if user has registered, and is a paying user... or created an account.
        :param uid: user id of the user performing the action
        :param organization_name: the name of the organization to of which we should check if we can create
        :return: a boolean indicating if we can create the organization
        ***REMOVED***
        pass

    def can_update_organization(self, uid: typing.Union[str, None], organization_id: typing.Union[str, None]):
        ***REMOVED***
            check if user has administrator rights on organization and if organization exist
            :param uid: the user performing this action
            :param organization_id: the organization_id of the organization to be updated
        :return: returns a response , status code tuple
        ***REMOVED***
        pass

    def create_org_id(self) -> str:
        ***REMOVED***
            create a valid organization_id if theres a conflict it creates another one and checks again if there is no
            conflict it returns the organization_id
        :return: organization_id
        ***REMOVED***
        organization_id: str = create_id()
        org_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()
        if isinstance(org_instance, Organization):
            self.create_org_id()
        return organization_id

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
        if self.can_create_organization(uid, organization_name) is True:
            organization_instance: Organization = Organization(owner_uid=uid,
                                                               organization_id=self.create_org_id(),
                                                               organization_name=organization_name,
                                                               description=description,
                                                               total_affiliates=0,
                                                               total_paid=AmountMixin(),
                                                               total_members=0,
                                                               projected_membership_payments=AmountMixin(),
                                                               total_membership_payments=AmountMixin())

            key: typing.Union[str, None] = organization_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = "An Unspecified Error has occurred creating database"
                return jsonify({'status': False, 'message': message}), 500

            message: str = "Successfully created Organization"
            return jsonify({'status': True, 'message': message}), 200

        message: str = "Unable to create organization"
        return jsonify({'status': False, 'message': message}), 500

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
        # NOTE: returns true if user has sufficient rights to update organization.
        if self.can_update_organization(uid=uid, organization_id=organization_id) is True:

            org_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()
            if isinstance(org_instance, Organization):
                org_instance.organization_name = organization_name
                org_instance.description = description
                key = org_instance.put(retries=self._max_retries, timeout=self._max_timeout)
                if key is None:
                    message: str = "An Unspecified Error has occurred"
                    return jsonify({'status': False, 'message': message}), 500
                message: str = "Successfully updated organization"
                return jsonify({'status': True, 'message': message}), 200
            message: str = "Unable to update Organization"
            return jsonify({'status': False, 'message': message}), 500

        message: str = "You are not allowed to edit that organization please contact administrator"
        return jsonify({'status': False, 'message': message}), 200

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
            if key is None:
                message: str = "An Unspecified error occured while adding to or subtract from affiliate count"
                raise DataServiceError(status=500, description=message)

            message: str = "Successfully updated affiliate count"
            return jsonify({'status': False, 'message': message}), 200
        message: str = "You are not authorized to perform this operation"
        return jsonify({'status': False, 'message': message}), 500

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

            if key is None:
                message: str = 'for some reason we are unable to add to total_amount'
                raise DataServiceError(status=500, description=message)

            message: str = "Successfully updated total paid amount on Organization"
            return jsonify({'status': True, 'message': message}), 200

        message: str = "Organization does not exist"
        return jsonify({'status': False, 'message': message}), 500

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
        organization_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()

        if isinstance(organization_instance, Organization):
            if isinstance(sub, int):
                organization_instance.total_members += add
            elif isinstance(add, int):
                organization_instance.total_members -= sub
            else:
                raise InputError(status=500, description="Please Enter either the amount to add or subtract")

            message: str = "Successfully updated total members on organization"
            return jsonify({'status': True, 'message': message}), 200
        message: str = "Unable to update organization"
        return jsonify({'status': True, 'message': message}), 500

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
        organization_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()

        if isinstance(organization_instance, Organization):
            if isinstance(add_payment, AmountMixin):
                organization_instance.projected_membership_payments += add_payment
            elif isinstance(sub_payment, AmountMixin):
                organization_instance.projected_membership_payments -= sub_payment
            else:
                raise InputError(status=500, description="Please enter either the amount to add or subtract")

            message: str = "Successfully updated projected_membership_payments"
            return jsonify({'status': True, 'message': message}), 200

        message: str = "Unable to update projected_membership_payments"
        return jsonify({'status': False, 'message': message}), 500

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
        organization_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()

        if isinstance(organization_instance, Organization):
            if isinstance(sub_total_membership_payment, AmountMixin):
                organization_instance.total_membership_payments += sub_total_membership_payment
            elif isinstance(add_total_membership_amount, AmountMixin):
                organization_instance.total_membership_payments += add_total_membership_amount
            else:
                raise InputError(status=500, description="Please enter either the amount to add or subtract")

            message: str = "Successfully updated total_membership_payments"
            return jsonify({'status': True, 'message': message}), 200
        message: str = "Unable to update total membership payments"
        return jsonify({'status': False, 'message': message}), 500


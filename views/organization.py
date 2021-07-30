***REMOVED***
organization view
enables users to add , update and delete organizations account
***REMOVED***
import typing
from flask import current_app, jsonify
from config.exception_handlers import handle_view_errors
from config.exceptions import InputError, DataServiceError
from config.use_context import use_context
from database.mixins import AmountMixin
from database.organization import Organization, OrgAccounts, OrgValidators


# TODO finish up organization  view
from main import app_cache
from utils.utils import create_id, return_ttl, can_cache


class OrganizationView(OrgValidators):
    # NOTE: used to create an organization so users can login into organization OrgAccounts
    # or become affiliates of such organizations,
    def __init__(self):
        super(OrganizationView, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    def can_create_organization(self, uid: typing.Union[str, None], organization_name: typing.Union[str, None]) -> bool:
        ***REMOVED***
            check if user has registered, and is a paying user... or created an account.
        :param uid:
        :param organization_name:
        :return:
        ***REMOVED***
        pass

    def can_update_organization(self, uid: typing.Union[str, None], organization_id: typing.Union[str, None]):
        ***REMOVED***
            check if user has administrator rights on organization and if organization exist
        :param uid:
        :param organization_id:
        :return:
        ***REMOVED***
        pass

    def create_org_id(self) -> str:
        organization_id: str = create_id()
        org_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()
        if isinstance(org_instance, Organization):
            self.create_org_id()
        return organization_id

    @use_context
    @handle_view_errors
    def create_organization(self, uid: typing.Union[str, None], organization_name: typing.Union[str, None],
                            description: typing.Union[str, None]) -> tuple:
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

            key = organization_instance.put(retries=self._max_retries, timeout=self._max_timeout)
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
    def affiliate_count(self, organization_id: typing.Union[str, None], add: typing.Union[int, None] = None,
                        sub: typing.Union[int, None] = None) -> tuple:
        ***REMOVED***
            Affiliate Count takes either an amount to add to subtract from affiliate not both
            :param organization_id:
            :param add: Optional
            :param sub: Optional
            :return:
        ***REMOVED***

        organization_instance: Organization = Organization.query(Organization.organization_id == organization_id).get()
        if isinstance(organization_instance, Organization):
            if isinstance(sub, int):
                organization_instance.total_affiliates -= sub
            elif isinstance(add, int):
                organization_instance.total_affiliates += add
            else:
                raise InputError(status=500, description="Please either enter the amount to subtract or add")

            key: typing.Union[str, None] = organization_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = "An Unspecified error occured while adding to or subtract from affiliate count"
                raise DataServiceError(status=500, description=message)

            message: str = "Successfully updated affiliate count"
            return jsonify({'status': False, 'message': message}), 200
        message: str = "You are not authorized to perform this operation"
        return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    def total_paid(self, organization_id: typing.Union[str, None],
                   add_amount: typing.Union[AmountMixin, None] = None,
                   sub_amount: typing.Union[AmountMixin, None] = None) -> tuple:
        ***REMOVED***
                Supply either add_amount or sub_amount but not both
        :param organization_id:
        :param add_amount: Optional
        :param sub_amount: Optional
        :return:
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
    def total_members(self, organization_id: typing.Union[str, None], add: typing.Union[int, None] = None,
                      sub: typing.Union[int, None] = None) -> tuple:
        ***REMOVED***
            supply either the amount to add to total members or the amount to subtract
            :param organization_id: 
            :param add:
            :param sub:
            :return:
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





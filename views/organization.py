***REMOVED***
organization view
enables users to add , update and delete organizations account
***REMOVED***
import typing
from flask import current_app, jsonify
from config.exception_handlers import handle_view_errors
from config.use_context import use_context
from database.mixins import AmountMixin
from database.organization import Organization, OrgAccounts, OrgValidators


# TODO finish up organization  view
from utils.utils import create_id


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


    def affiliate_count(self, organization_id: typing.Union[str, None], add: int = None, sub: int = None) -> tuple:
        pass
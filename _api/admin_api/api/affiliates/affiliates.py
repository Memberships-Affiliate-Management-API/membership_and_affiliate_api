"""
    **api keys system admin module**
        controls access to api keys for system admin application
"""

__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

import hmac
from typing import Optional
from flask import Blueprint, request
from config import config_instance
from config.exceptions import UnAuthenticatedError, InputError
from security.apps_authenticator import handle_apps_authentication, verify_secret_key
from views import affiliates_view

admin_affiliates_api_bp = Blueprint("admin_affiliates_api", __name__)


@admin_affiliates_api_bp.route('/_api/v1/admin/affiliates/<string:path>', methods=["POST"])
@handle_apps_authentication
def admin_affiliates(path: str) -> tuple:
    """
    **admin_affiliates**
        get_affiliate
            
        :param path:
        :return:
    """
    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get('SECRET_KEY')
    verify_secret_key(secret_key)

    if path == "get-all":
        organization_id: str = json_data.get('organization_id')
        uid: str = json_data.get('uid')
        compare_organization: bool = hmac.compare_digest(organization_id, config_instance.ORGANIZATION_ID)
        compare_uid: bool = hmac.compare_digest(uid, config_instance.ADMIN_UID)

        if compare_organization and compare_uid:
            # NOTE: this returns the affiliates to the main application
            return affiliates_view.get_all_affiliates(organization_id=organization_id)
        message: str = "You are not authorized to access this resource"
        raise UnAuthenticatedError(description=message)
    elif path == "register-affiliate":
        """           
            **register_affiliate**
                Register new affiliate, affiliate_data must contain the uid of the affiliate
                being recruited and organization_id of the organization recruiting the affiliate.

        :param affiliate_data:
        :return: tuple with registered affiliate
        """
        return affiliates_view.register_affiliate(affiliate_data=get_affiliate_data(json_data))
    elif path == "update-total-recruits":
        """
               **total_recruits**
                    given an existing affiliate update total recruits field in the affiliate record
        """
        affiliate_data: dict = get_affiliate_data(json_data)
        try:
            add: int = int(json_data.get('add'))
        except ValueError:
            _message: str = 'add must be an integer'
            raise InputError(description=_message)
        return affiliates_view.total_recruits(affiliate_data=affiliate_data, add=add)
    elif path == "delete-affiliate":
        """
            **delete_affiliate**
                the function soft delete an affiliate record.

                affiliate_id: is the id of the affiliate to be marked as deletedItem
                organization_id: is the id of the organization from which the affiliate is to be deleted

            :param affiliate_data: dict containing affiliate_id and organization_id
            :return: tuple containing the record of the deleted affiliate    
        """
        return affiliates_view.delete_affiliate(affiliate_data=get_affiliate_data(json_data))
    elif path == "mark-active":
        """
            **mark_active**        
                    affiliate_id of the affiliate to be marked as active.
                    this action will not have an effect if the affiliate has been soft-deleted
    
            :param affiliate_data: contains affiliate_id and organization_id
            :param is_active:
            :return:
        """
        affiliate_data: dict = get_affiliate_data(json_data)
        is_active: bool = json_data.get('is_active')
        return affiliates_view.mark_active(affiliate_data=affiliate_data, is_active=is_active)
    elif path == "get-affiliate":
        """
            **get_affiliate**
                obtains a record of one affiliate from the store. given either uid or affiliate_id, organization_id
                must be valid

        :param affiliate_data: contains affiliate_id and organization_id the affiliate must belong to the organization
        :return: response contain affiliate record        
        """
        return affiliates_view.get_affiliate(affiliate_data=get_affiliate_data(json_data))
    elif path == "get-affiliates-by-active-status":
        """
            **get_active_affiliates**
                NOTE: active affiliates but not deleted
                returns a list of active affiliates in an organization

        :param organization_id: the organization id of the organization to return the affiliates
        :return: response containing the list of active affiliates        
        """
        affiliate_data: dict = get_affiliate_data(json_data)
        if affiliate_data.get('is_active'):
            return affiliates_view.get_active_affiliates(organization_id=affiliate_data.get('organization_id'))
        return affiliates_view.get_in_active_affiliates(organization_id=affiliate_data.get('organization_id'))
    elif path == 'get-deleted':
        """
                    **get_deleted_affiliates**
                return deleted affiliates by organization_id

        :param organization_id:
        :return: response containing the list of affiliates who are deleted
        """
        affiliate_data: dict = get_affiliate_data(json_data)
        return affiliates_view.get_deleted_affiliates(organization_id=affiliate_data.get('organization_id'))
    elif path == 'get-not-deleted':
        """
            **get_not_deleted_affiliates**
                # NOTE: this function may be redundant
                returns a list of affiliates which are not deleted by  ORGANIZATION_ID
        :param : organization_id: the organization to return deleted affiliates from
        :return : response containing the list of deleted affiliates        
        """
        affiliate_data: dict = get_affiliate_data(json_data)
        return affiliates_view.get_not_deleted_affiliates(organization_id=affiliate_data.get('organization_id'))


def get_affiliate_data(json_data: dict) -> dict:
    """
        **get_affiliate_data**
            given json_data as input validate data and return affiliate_data
    :param json_data:
    :raises: InputError and UnAuthenticatedError
    :return: affiliate_data as dict
    """
    organization_id: str = json_data.get('organization_id')
    uid: str = json_data.get('uid')
    compare_organization: bool = hmac.compare_digest(organization_id, config_instance.ORGANIZATION_ID)
    compare_uid: bool = hmac.compare_digest(uid, config_instance.ADMIN_UID)
    if not (compare_uid and compare_organization):
        message: str = "You are not authorized to access this resource"
        raise UnAuthenticatedError(description=message)
    affiliate_data: dict = json_data.get('affiliate_data')
    if isinstance(affiliate_data, dict):
        _message: str = 'please provide affiliate data in order to register affiliate'
        raise InputError(description=_message)
    return affiliate_data

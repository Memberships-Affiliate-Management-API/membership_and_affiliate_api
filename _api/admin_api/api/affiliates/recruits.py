"""
    **recruits admin api module**
        an admin api for recruits management
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
from views import recruits_view

admin_recruits_api_bp = Blueprint("admin_recruits_api", __name__)


def _compare_org_uid(organization_id, uid) -> tuple:
    compare_organization: bool = hmac.compare_digest(organization_id, config_instance.ORGANIZATION_ID)
    compare_uid: bool = hmac.compare_digest(uid, config_instance.ADMIN_UID)
    return compare_organization, compare_uid


@admin_recruits_api_bp.route('/_api/v1/admin/recruits/<string:path>', methods=['POST'])
@handle_apps_authentication
def recruits_admin(path: str) -> tuple:
    """
        **recruits_admin**
            system admin management api
    :param path:
    :return:
    """
    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get('SECRET_KEY')
    verify_secret_key(secret_key)
    if path == 'get-all':
        """ get all recruits for memberships and affiliate management api"""
        organization_id: str = json_data.get('organization_id')
        uid: str = json_data.get('uid')
        compare_organization, compare_uid = _compare_org_uid(organization_id, uid)
        if not (compare_organization and compare_uid):
            message: str = 'you are not authorized to access this resource'
            raise UnAuthenticatedError(description=message)
        return recruits_view.get_all_recruits(organization_id=organization_id)
    elif path == 'get-organization-recruits':
        """ get specific organization recruit"""
        organization_id: str = json_data.get('organization_id')
        return recruits_view.get_all_recruits(organization_id=organization_id)
    elif path == 'delete_recruit':
        """delete any recruit from any any other organization"""
        return recruits_view.delete_recruit(recruit_data=get_recruit_data(json_data))
    elif path == 'add-recruit':
        """add new admin recruit"""
        return recruits_view.add_recruit(recruit_data=get_recruit_data(json_data))
    elif path == "get-recruit":
        """get a specific recruit"""
        return recruits_view.get_recruit(recruit_data=get_recruit_data(json_data))


def get_recruit_data(json_data: dict) -> dict:
    """
        **get_recruit_data**
            authenticate admin user and get recruit_data
    :param json_data: dict
    :raises InputError and UnAuthenticatedError
    :return: recruit_data
    """
    organization_id: str = json_data.get('organization_id')
    uid: str = json_data.get('uid')
    compare_organization, compare_uid = _compare_org_uid(organization_id, uid)
    if not (compare_organization and compare_uid):
        message: str = 'you are not authorized to access this resource'
        raise UnAuthenticatedError(description=message)
    if not (compare_organization and compare_uid):
        message: str = 'you are not authorized to access this resource'
        raise UnAuthenticatedError(description=message)
    recruit_data: dict = json_data.get('recruit_data')
    if not isinstance(recruit_data, dict):
        _message: str = 'please supply the details of the recruit to delete in recruit_data'
        raise InputError(description=_message)
    return recruit_data

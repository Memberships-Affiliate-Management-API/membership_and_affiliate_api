"""
    handle users and admin authentication
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

import hmac
from typing import Optional

from flask import Blueprint, request, current_app, jsonify

from config import config_instance
from config.exceptions import error_codes, UnAuthenticatedError, if_bad_request_raise
from security.apps_authenticator import handle_apps_authentication
from security.users_authenticator import get_admin_user, encode_auth_token, decode_auth_token
from views import user_view

admin_users_api_bp = Blueprint("admin_users_api", __name__)


@admin_users_api_bp.route('/_api/v1/admin/users/<string:path>', methods=["GET", "POST"])
@handle_apps_authentication
def admin_users(path: str) -> tuple:
    """
    **admin_users**

    :param  path: indicates what route to follow for admin users
    :return:
    """
    # NOTE: only this application can call this endpoints-
    # For Purposes of authentication check if the calling url belongs to this app

    if_bad_request_raise(request)

    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get("SECRET_KEY")
    compare_secret_key: bool = hmac.compare_digest(secret_key, current_app.config.get('SECRET_KEY'))
    if not compare_secret_key:
        message: str = 'User Not Authorized: you cannot perform this action'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    if path == "get":
        organization_id: Optional[str] = json_data.get("organization_id")
        uid: Optional[str] = json_data.get("uid")
        compare_organization: bool = hmac.compare_digest(organization_id, config_instance.ORGANIZATION_ID)
        compare_uid: bool = hmac.compare_digest(uid, config_instance.ADMIN_UID)

        if compare_organization and compare_uid:
            return user_view.get_user(uid=uid, organization_id=organization_id)

    # NOTE: get all main organizations users
    elif path == "get-all":
        organization_id: Optional[str] = json_data.get("organization_id")
        uid: Optional[str] = json_data.get("uid")
        compare_organization: bool = hmac.compare_digest(organization_id, config_instance.ORGANIZATION_ID)
        compare_uid: bool = hmac.compare_digest(uid, config_instance.ADMIN_UID)

        if compare_organization and compare_uid:
            return user_view.get_all_users(organization_id=organization_id)

    elif path == "is-user-unique":
        # checks if user exists based on either email or uid - used for administration purposes
        email: Optional[str] = json_data.get("email")
        uid: Optional[str] = json_data.get("uid")
        compare_uid: bool = hmac.compare_digest(uid, config_instance.ADMIN_UID)
        compare_email: bool = hmac.compare_digest(email, config_instance.ADMIN_EMAIL)

        if compare_email and compare_uid:
            return user_view._system_user_exist(email=email, uid=uid)


@admin_users_api_bp.route('/_api/v1/admin/auth/<string:path>', methods=["GET", "POST"])
@handle_apps_authentication
def auth_admin(path: str) -> tuple:
    """

    :param path:
    :return:
    """
    if_bad_request_raise(request)

    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get('SECRET_KEY')

    compare_secret_key: bool = hmac.compare_digest(secret_key, current_app.config.get('SECRET_KEY'))
    if not compare_secret_key:
        message: str = 'User Not Authorized: you cannot perform this action'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    if path == "login":
        email: Optional[str] = json_data.get("email")
        password: Optional[str] = json_data.get("password")
        uid: Optional[str] = json_data.get("uid")
        organization_id: Optional[str] = json_data.get("organization_id")
        print(f'json data: {json_data}')

        # Comparing Digests
        compare_email: bool = hmac.compare_digest(email, config_instance.ADMIN_EMAIL)
        compare_password: bool = hmac.compare_digest(password, config_instance.ADMIN_PASSWORD)
        compare_uid: bool = hmac.compare_digest(uid, config_instance.ADMIN_UID)
        compare_org: bool = hmac.compare_digest(organization_id, config_instance.ORGANIZATION_ID)
        print(f'compare org : {compare_org}')
        print(f'compare uid: {compare_uid}')

        if compare_email and compare_password and compare_uid and compare_org:
            user_dict: dict = get_admin_user().to_dict()
            token: Optional[str] = encode_auth_token(uid=uid)
            message: str = 'welcome admin'
            payload: dict = dict(token=token, user=user_dict)
            # TODO - save auth details on MicroAuthDetails
            # NOTE: when applications communicate amongst each other they must authenticate using admin credentials
            # NOTE: in order to renew authentication details
            return jsonify({'status': True, 'payload': payload, 'message': message})

        raise UnAuthenticatedError(description='You are not authorized to login as admin')

    elif path == "logout":

        email: Optional[str] = json_data.get("email")
        token: str = json_data.get('token')
        uid: Optional[str] = json_data.get("uid")
        organization_id: Optional[str] = json_data.get("organization_id")
        token_uid: str = decode_auth_token(auth_token=token)
        # Comparing Digests
        compare_email: bool = hmac.compare_digest(email, config_instance.ADMIN_EMAIL)
        compare_uid: bool = hmac.compare_digest(uid, token_uid)
        compare_org: bool = hmac.compare_digest(organization_id, config_instance.ORGANIZATION_ID)

        # NOTE remove any cached tokens
        if compare_email and compare_uid and compare_org:
            user_dict: dict = get_admin_user().to_dict()
            user_dict.update(password="")
            token: Optional[str] = None
            message: str = 'successfully logged out user'

            payload: dict = dict(token=token, user=user_dict)
            return jsonify({'status': True, 'payload': payload, 'message': message})

    elif path == "get-admin-user":
        uid: Optional[str] = json_data.get("uid")
        organization_id: Optional[str] = json_data.get("organization_id")
        compare_uid: bool = hmac.compare_digest(uid, config_instance.ADMIN_UID)
        compare_org: bool = hmac.compare_digest(organization_id, config_instance.ORGANIZATION_ID)

        if compare_org and compare_uid:
            user_dict: dict = get_admin_user().to_dict()
            user_dict.update(password="")
            message: str = 'user successfully retrieved'
            return jsonify({'status': True, 'payload': user_dict, 'message': message})

    raise UnAuthenticatedError(description='You are not authorized access this resource')

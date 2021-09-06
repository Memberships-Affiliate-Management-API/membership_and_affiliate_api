"""
**memberships main or documentations application api endpoint**

"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from typing import Optional
from flask import Blueprint, jsonify, request
from config.exceptions import error_codes, UnAuthenticatedError, status_codes
from security.users_authenticator import logged_user
from main.app.memberships_main.api.main_api_view import MainAPPAPIView

main_api_bp = Blueprint('main_api', __name__)


# TODO: insure the organization for Memberships & affiliates Management API is created before
#  running any API's this can be done on app setup

@main_api_bp.route('/api/v1/main/auth/<path:path>', methods=['POST'])
@logged_user
def auth(current_user: Optional[dict], path: str) -> tuple:
    """
        **auth**
            for authentication based on password and email
            authentication api, handles login, password recovery, and user subscriptions,
            for membership & affiliates Management API, main app
    :return:
    """
    main_app_view: MainAPPAPIView = MainAPPAPIView()

    if path == 'login':
        if current_user and bool(current_user.get('uid')):
            message: str = "Access Forbidden: User already logged in"
            raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

        json_data: dict = request.get_json()
        email: str = json_data.get('email')
        password: str = json_data.get('password')
        response, status_code = main_app_view.send_login_request(email=email, password=password)
        return jsonify(response), status_code

    elif path == 'subscribe':
        if current_user and bool(current_user.get('uid')):
            message: str = "Access Forbidden: User already logged in"
            raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

        json_data: dict = request.get_json()
        names: Optional[str] = json_data.get('names')
        cell: Optional[str] = json_data.get('cell')
        email: Optional[str] = json_data.get('email')
        password: Optional[str] = json_data.get('password')
        name, surname = names.split(" ")
        response, status_code = main_app_view.send_register_request(email=email, cell=cell, names=name, surname=surname,
                                                                    password=password)
        return jsonify(response), status_code

    elif path == 'send-recovery-email':
        if current_user and bool(current_user.get('uid')):
            message: str = "Access Forbidden: User already logged in"
            raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

        json_data: dict = request.get_json()
        email = json_data.get('email')
        print(f"sending recovery email : {email}")
        response, status_code = main_app_view.send_recovery_email(email=email)
        return jsonify(response), status_code

    # NOTE that if user is logged in then user details will be present on current_user
    elif path == "get":
        # NOTE: this route could be called by the main app just in-case the user is already logged-in
        if current_user and bool(current_user.get('uid')):
            message: str = "user details successfully fetched"
            return jsonify({'status': True, 'payload': current_user, 'message': message})
        message: str = "unable to retrieve user details: please login"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code


@main_api_bp.route('/api/v1/main/contact', methods=['POST', 'GET', 'PUT', 'DELETE'])
@logged_user
def contact(current_user: Optional[dict]) -> tuple:
    """
        **contact**
            main contact api- handles everything related to
            contacts for both clients and admins
        :return: tuple: -> response, status_code
    """
    json_data: dict = request.get_json()
    if current_user and bool(current_user.get('uid')):
        # NOTE: if user is logged in add the user id in the message
        json_data.update(uid=current_user.get('uid'))

    main_app_view: MainAPPAPIView = MainAPPAPIView()
    response, status_code = main_app_view.send_contact_message_request(contact_message=json_data)

    return jsonify(response), status_code

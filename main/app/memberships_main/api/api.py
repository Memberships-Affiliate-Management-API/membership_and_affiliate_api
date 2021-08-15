from typing import Optional
from flask import Blueprint, jsonify, request, current_app
from config.exceptions import error_codes, UnAuthenticatedError, status_codes
from security.users_authenticator import logged_user
from main.app.memberships_main.api.main_api_view import MainAPPAPIView

main_api_bp = Blueprint('main_api', __name__)


# TODO: insure the organization for Memberships & affiliates Management API is created before
#  running any API's this can be done on app setup

@main_api_bp.route('/api/v1/main/auth/<path:path>', methods=['POST'])
@logged_user
def auth(current_user, path: str) -> tuple:
    ***REMOVED***
        **auth**
            for authentication based on password and email
            authentication api, handles login, password recovery, and user subscriptions,
            for membership & affiliates Management API, main app
    :return:
    ***REMOVED***
    main_app_view: MainAPPAPIView = MainAPPAPIView()

    if path == 'login':
        if current_user:
            message: str = "Access Forbidden: User already logged in"
            raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

        json_data: dict = request.get_json()
        email: str = json_data.get('email')
        password: str = json_data.get('password')
        return main_app_view.send_login_request(email=email, password=password)

    elif path == 'subscribe':
        if current_user:
            message: str = "Access Forbidden: User already logged in"
            raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

        json_data: dict = request.get_json()
        names: Optional[str] = json_data.get('names')
        cell: Optional[str] = json_data.get('cell')
        email: Optional[str] = json_data.get('email')
        password: Optional[str] = json_data.get('password')
        name, surname = names.split(" ")
        return main_app_view.send_register_request(email=email, cell=cell, names=name, surname=surname,
                                                   password=password)

    elif path == 'send-recovery-email':
        if current_user:
            message: str = "Access Forbidden: User already logged in"
            raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

        json_data: dict = request.get_json()
        email = json_data.get('email')
        return main_app_view.send_recovery_email(email=email)

    # NOTE that if user is logged in then user details will be present on current_user
    elif path == "get":
        # NOTE: this route could be called by the main app just in-case the user is already logged-in
        if current_user:
            message: str = "user details successfully fetched"
            return jsonify({'status': True, 'payload': current_user.to_dict(), 'message': message})
        message: str = "unable to retrieve user details: please login"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code


@main_api_bp.route('/api/v1/main/contact', methods=['POST', 'GET', 'PUT', 'DELETE'])
@logged_user
def contact(current_user) -> tuple:
    ***REMOVED***
        **contact**
            main contact api- handles everything related to
            contacts for both clients and admins
        :return:
    ***REMOVED***
    main_app_view: MainAPPAPIView = MainAPPAPIView()
    json_data: dict = request.get_json()
    return main_app_view.send_contact_message_request(contact_message=json_data)

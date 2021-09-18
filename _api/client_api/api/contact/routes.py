"""
    **Contact Module**
"""
import hmac
from typing import Optional
from flask import Blueprint, request, current_app, jsonify
from config.exceptions import UnAuthenticatedError, error_codes, if_bad_request_raise, InputError
from security.apps_authenticator import handle_apps_authentication, verify_secret_key

contact_api_bp = Blueprint('contact-api', __name__)


# noinspection DuplicatedCode
@contact_api_bp.route('/_api/v1/client/contact/<string:path>', methods=['POST'])
@handle_apps_authentication
def contact(path: str) -> tuple:
    """
        **contact**
            main contact api- handles everything related to contacts
            for both clients and admins
    :return:
    """
    if_bad_request_raise(request)
    json_data: dict = request.get_json()
    # print(json_data)
    if not isinstance(json_data, dict):
        message: str = "Invalid Input format this endpoint accept only json_data"
        raise InputError(status=error_codes.input_error_code, description=message)

    secret_key: Optional[str] = json_data.get('SECRET_KEY')
    verify_secret_key(secret_key)

    if path == "create":
        names: Optional[str] = json_data.get('names')
        email: Optional[str] = json_data.get('email')
        cell: Optional[str] = json_data.get('cell')
        topic: Optional[str] = json_data.get('topic')
        subject: Optional[str] = json_data.get('subject')
        body: Optional[str] = json_data.get('body')
        organization_id: Optional[str] = json_data.get('organization_id')
        # NOTE the only time uid would be available is when the user is already logged in
        uid: Optional[str] = json_data.get('uid')
        # TODO finish up contact its the same as helpdesk

        print(f'Names: {names}, Email: {email}, Cell: {cell}, Topic: {topic}, Subject: {subject}, Body: {body}')
    elif path == "get":
        pass

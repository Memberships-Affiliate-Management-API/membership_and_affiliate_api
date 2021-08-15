
***REMOVED***
***REMOVED***
from typing import Optional
from flask import Blueprint, request, current_app, jsonify
from config.exceptions import UnAuthenticatedError, error_codes, if_bad_request_raise

contact_api_bp = Blueprint('contact-api', __name__)


@contact_api_bp.route('/_api/v1/client/contact/<string:path>', methods=['POST'])
def contact(path: str) -> tuple:
    ***REMOVED***
        **contact**
            main contact api- handles everything related to contacts
            for both clients and admins
    :return:
    ***REMOVED***
    if_bad_request_raise(request)
    json_data: dict = request.get_json()
    # print(json_data)
    if isinstance(json_data, dict):
        secret_key: Optional[str] = json_data.get('SECRET_KEY')
        # print(f"SecretKey:  {secret_key}")

        if not isinstance(secret_key, str) or secret_key != current_app.config.get('SECRET_KEY'):
            message: str = 'User Not Authorized: you cannot perform this action'
            raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

        elif path == "create":
            names: Optional[str] = json_data.get('names')
            email: Optional[str] = json_data.get('email')
            cell: Optional[str] = json_data.get('cell')
            topic: Optional[str] = json_data.get('topic')
            subject: Optional[str] = json_data.get('subject')
            body: Optional[str] = json_data.get('body')
            organization_id: Optional[str] = json_data.get('organization_id')
            # NOTE the only time uid would be available is when the user is already logged in
            uid: Optional[str] = json_data.get('uid')

            print(f'Names: {names}, Email: {email}, Cell: {cell}, Topic: {topic}, Subject: {subject}, Body: {body}')
        elif path == "get":
            pass

    return jsonify({'status': False, 'message': 'Unable to send request please try again later'}), 200

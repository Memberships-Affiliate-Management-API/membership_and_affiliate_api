
***REMOVED***
***REMOVED***
from typing import Optional
from flask import Blueprint, request, current_app, jsonify
from security.users_authenticator import logged_user
from database.users import UserModel


contact_api_bp = Blueprint('contact-api', __name__)


@contact_api_bp.route('/api/v1/main/contact', methods=['POST', 'GET', 'PUT', 'DELETE'])
@logged_user
def contact(current_user: UserModel) -> tuple:
    ***REMOVED***
        **contact**
            main contact api- handles everything related to contacts
            for both clients and admins
    :return:
    ***REMOVED***
    json_data: dict = request.get_json()
    # TODO: send contact data to contact database view
    names: Optional[str] = json_data.get('names')
    email: Optional[str] = json_data.get('email')
    cell: Optional[str] = json_data.get('cell')
    topic: Optional[str] = json_data.get('topic')
    subject: Optional[str] = json_data.get('subject')
    body: Optional[str] = json_data.get('body')
    organization_id: Optional[str] = current_app.config.get('ORGANIZATION_ID')

    print('Names: {}, Email: {}, Cell: {}, Topic: {}, Subject: {}, Body: {}'.format(names, email, cell, topic,
                                                                                    subject, body))

    # TODO - add contact database view call here
    return jsonify({'status': False, 'message': 'Unable to send request please try again later'}), 200

from flask import Blueprint, jsonify, request, url_for, flash

from database.users import UserModel
from security.users_authenticator import logged_user
from views.users import UserView

main_api_bp = Blueprint('main_api', __name__)


# TODO: insure the organization for Memberships & affiliates Management API is created before
#  running any API's this can be done on app setup
@main_api_bp.route('/api/v1/main/auth/<path:path>', methods=['POST'])
@logged_user
def auth(current_user: UserModel, path: str) -> tuple:
    ***REMOVED***
        authentication api, handles login, password recovery, and user subscriptions,
        for membership & affiliates Management API, main app
    :return:
    ***REMOVED***
    if current_user:
        message: str = "User already logged in"
        return jsonify({'status': False, 'message': message}), 500

    if path == 'login':
        json_data: dict = request.get_json()
        users_view_instance: UserView = UserView()
        email: str = json_data.get('email')
        password: str = json_data.get('password')
        return users_view_instance.login(email=email, password=password)

    elif path == 'subscribe':
        json_data: dict = request.get_json()
        # TODO - check data validity
        names: str = json_data.get('names')
        cell: str = json_data.get('cell')
        email: str = json_data.get('email')
        password: str = json_data.get('password')
        print(json_data)
        users_view_instance: UserView = UserView()
        return users_view_instance.add_user(names=names, cell=cell, email=email, password=password)

    elif path == 'send-recovery-email':
        json_data: dict = request.get_json()
        print("email : {}".format(json_data.get('email')))
        # TODO: pass email address to a function to check its validity and then send a password recovery email
        email = json_data.get('email')
        users_view_instance: UserView = UserView()
        return users_view_instance.send_recovery_email(email=email)


@main_api_bp.route('/api/v1/main/contact', methods=['POST'])
def contact() -> tuple:
    json_data: dict = request.get_json()
    # TODO: send contact data to contact format
    print('Names: {}, Email: {}, Cell: {}, '
          'Topic: {}, Subject: {}, Body: {}'.format(json_data.get('names'), json_data.get('email'),
                                                    json_data.get('cell'), json_data.get('topic'),
                                                    json_data.get('subject'), json_data.get('body')))

    return jsonify({'status': False, 'message': 'Unable to send request please try again later'}), 200

import typing
from flask import Blueprint, jsonify, request, current_app, url_for, flash, redirect
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
        organization_id = current_app.config.get('ORGANIZATION_ID')
        return users_view_instance.login(organization_id=organization_id, email=email, password=password)

    elif path == 'subscribe':
        json_data: dict = request.get_json()
        # TODO - check data validity
        names: str = json_data.get('names')
        cell: str = json_data.get('cell')
        email: str = json_data.get('email')
        password: str = json_data.get('password')
        organization_id = current_app.config.get('ORGANIZATION_ID')
        users_view_instance: UserView = UserView()
        name, surname = names.split(" ")
        response = users_view_instance.add_user(organization_id=organization_id, names=names, surname=surname,
                                                cell=cell, email=email, password=password)
        print(response)
        return response

    elif path == 'send-recovery-email':
        json_data: dict = request.get_json()
        # TODO: pass email address to a function to check its validity and then send a password recovery email
        email = json_data.get('email')
        # Users here are logging into the main app not clients app
        organization_id = current_app.config.get('ORGANIZATION_ID')
        users_view_instance: UserView = UserView()
        return users_view_instance.send_recovery_email(organization_id=organization_id, email=email)


@main_api_bp.route('/api/v1/main/contact', methods=['POST', 'GET', 'PUT', 'DELETE'])
@logged_user
def contact(current_user: UserModel) -> tuple:
    ***REMOVED***
        main contact api- handles everything related to contacts for both clients and admins
    :return:
    ***REMOVED***
    json_data: dict = request.get_json()
    # TODO: send contact data to contact database view
    names: typing.Union[str, None] = json_data.get('names')
    email: typing.Union[str, None] = json_data.get('email')
    cell: typing.Union[str, None] = json_data.get('cell')
    topic: typing.Union[str, None] = json_data.get('topic')
    subject: typing.Union[str, None] = json_data.get('subject')
    body: typing.Union[str, None] = json_data.get('body')
    organization_id: typing.Union[str, None] = current_app.config.get('ORGANIZATION_ID')

    print('Names: {}, Email: {}, Cell: {}, Topic: {}, Subject: {}, Body: {}'.format(names, email, cell, topic,
                                                                                    subject, body))

    # TODO - add contact database view call here
    return jsonify({'status': False, 'message': 'Unable to send request please try again later'}), 200

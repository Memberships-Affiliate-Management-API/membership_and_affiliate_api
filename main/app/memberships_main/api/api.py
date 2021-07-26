from flask import Blueprint, jsonify, request

main_api_bp = Blueprint('main_api', __name__)


# TODO: insure the organization for Memberships & affiliates Management API is created before running any API's this can be done on app setup
@main_api_bp.route('/api/v1/main/auth/<path:path>', methods=['POST'])
def auth(path: str) -> tuple:
    ***REMOVED***
        authentication api, handles login, password recovery, and user subscriptions,
        for membership & affiliates Management API, main app
    :return:
    ***REMOVED***
    if path == 'login':
        json_data: dict = request.get_json()
        # TODO: pass login email and password to a function to login_form
        #  If login successful redirect to dashboard page and flash login success message

        message: str = 'login was not successful please check your ' \
                       '<strong>email: <code>{}</code> </strong> or <strong>password: <code>{}</code></strong>'.format(
                        json_data.get('email'), json_data.get('password'))

        return jsonify({'status': False, 'message': message}), 200

    elif path == 'subscribe':
        # TODO: pass subscription data to user add function if successfull redirect to dashboard and flash message
        message: str = 'unable to subscribe user please check your data or try again later'
        return jsonify({'status': False, 'message': message}), 200

    elif path == 'recover':
        json_data: dict = request.get_json()
        print("email : {}".format(json_data.get('email')))
        # TODO: pass email address to a function to check its validity and then send a password recovery email
        return jsonify({'status': True,
                        'message': 'successfully sent a password recovery email please check your email'}), 200


@main_api_bp.route('/api/v1/main/contact', methods=['POST'])
def contact() -> tuple:
    json_data: dict = request.get_json()
    # TODO: send contact data to contact format
    print('Names: {}, Email: {}, Cell: {}, '
          'Topic: {}, Subject: {}, Body: {}'.format(json_data.get('names'), json_data.get('email'),
                                                    json_data.get('cell'), json_data.get('topic'),
                                                    json_data.get('subject'), json_data.get('body')))

    return jsonify({'status': False, 'message': 'Unable to send request please try again later'}), 200

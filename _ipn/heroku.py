***REMOVED***
   https://memberships-affiliates-man-api.herokuapp.com/_ipn/auth/heroku
***REMOVED***
from flask import Blueprint, jsonify
from config.exceptions import status_codes

heroku_ipn_bp = Blueprint("heroku_ipn", __name__)


@heroku_ipn_bp.route('/_ipn/auth/heroku', methods=["GET", "POST"])
def heroku_auth_ipn():
    return jsonify({'status': False, 'message': 'coming soon'}), status_codes.status_ok_code

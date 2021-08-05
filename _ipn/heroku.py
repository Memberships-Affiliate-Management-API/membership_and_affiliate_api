***REMOVED***
   http://memberships-affiliates-man-api.herokuapp.com/_ipn/auth/heroku
***REMOVED***
from flask import Blueprint, request, jsonify

from config.exceptions import status_codes
from main import app_cache
from utils.utils import return_ttl, can_cache

heroku_ipn_bp = Blueprint("heroku_ipn", __name__)


@heroku_ipn_bp.route('/_ipn/auth/heroku', methods=["GET", "POST"])
def heroku_auth_ipn():
    return jsonify({'status': False, 'message': 'coming soon'}), status_codes.status_ok_code

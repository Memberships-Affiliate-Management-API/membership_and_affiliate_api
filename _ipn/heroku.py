***REMOVED***
    **Heroku Oauth Endpoint**
   https://memberships-affiliates-man-api.herokuapp.com/_ipn/auth/heroku
***REMOVED***
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from flask import Blueprint, jsonify
from config.exceptions import status_codes

heroku_ipn_bp = Blueprint("heroku_ipn", __name__)


@heroku_ipn_bp.route('/_ipn/auth/heroku', methods=["GET", "POST"])
def heroku_auth_ipn():
    return jsonify({'status': False, 'message': 'coming soon'}), status_codes.status_ok_code

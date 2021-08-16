***REMOVED***
    **Client Home Route**
        entry page to client dashboard
***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from flask import Blueprint, render_template, get_flashed_messages
from config.exceptions import status_codes
from database.users import UserModel
from main import app_cache
from security.users_authenticator import logged_user
from utils.utils import return_ttl, can_cache

client_home_bp = Blueprint('client_home', __name__)


@client_home_bp.route('/client', methods=["GET"])
@logged_user
@app_cache.cached(timeout=return_ttl('short'))
def client_home(current_user: UserModel) -> tuple:
    ***REMOVED***
        **client_home**
            entry page to client dashboard
    :param current_user:
    :return:
    ***REMOVED***
    get_flashed_messages()
    if current_user and current_user.uid:
        return render_template('client/home.html', current_user=current_user), status_codes.status_ok_code
    else:
        return render_template('client/home.html'), status_codes.status_ok_code




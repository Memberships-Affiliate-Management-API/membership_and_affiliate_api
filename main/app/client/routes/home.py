***REMOVED***
    this is a public route
***REMOVED***
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
    get_flashed_messages()
    if current_user and current_user.uid:
        return render_template('client/home.html', current_user=current_user), status_codes.status_ok_code
    else:
        return render_template('client/home.html'), status_codes.status_ok_code




***REMOVED***
    this is a public route
***REMOVED***
from flask import Blueprint, render_template, get_flashed_messages
from database.users import UserModel
from main import app_cache
from security.users_authenticator import logged_user
from utils.utils import return_ttl, can_cache

client_home_bp = Blueprint('client_home', __name__)


# noinspection PyTypeChecker
@client_home_bp.route('/client', methods=["GET"])
@logged_user
@app_cache.cached(timeout=return_ttl('short'), unless=can_cache())
def client_home(current_user: UserModel) -> tuple:
    get_flashed_messages()
    if current_user:
        return render_template('client/home.html', current_user=current_user), 200
    else:
        return render_template('client/home.html'), 200




***REMOVED***
    this is a public route
***REMOVED***
from flask import Blueprint, request, url_for, render_template, get_flashed_messages
from database.users import UserModel
from security.users_authenticator import logged_user

client_home_bp = Blueprint('client_home', __name__)


@client_home_bp.route('/client', methods=["GET"])
@logged_user
def client_home(current_user: UserModel) -> tuple:
    if current_user:
        return render_template('client/home.html', current_user=current_user), 200
    else:
        return render_template('client/home.html'), 200




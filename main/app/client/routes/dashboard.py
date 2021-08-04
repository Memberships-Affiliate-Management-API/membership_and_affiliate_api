***REMOVED***
    this is a private route
***REMOVED***
from flask import Blueprint, request, render_template, url_for, get_flashed_messages, redirect, flash

from config.exceptions import status_codes
from database.users import UserModel
from main import app_cache
from security.users_authenticator import handle_users_auth
from utils.utils import return_ttl, can_cache
client_dashboard_bp = Blueprint('client_dashboard', __name__)


@client_dashboard_bp.route('/client/dashboard', methods=["GET"])
@handle_users_auth
def client_dashboard(current_user: UserModel) -> tuple:
    get_flashed_messages()
    if not(current_user and current_user.uid):
        # TODO: insure local cache does not cache info if redirected
        flash('Please login or register to start using this app')
        return redirect(url_for('memberships_main.memberships_main_routes', path='login'))

    return render_template('client/dashboard.html', current_user=current_user), status_codes.status_ok_code


@client_dashboard_bp.route('/client/dashboard/<path:path>', methods=["GET"])
@handle_users_auth
def client_dashboard_routes(current_user: UserModel, path: str) -> tuple:
    get_flashed_messages()
    if not(current_user and current_user.uid):
        flash('Please login or register to start using this app')
        return redirect(url_for('memberships_main.memberships_main_routes', path='login'))

    if path == "dashboard":
        return render_template('client/dashboard.html', current_user=current_user), status_codes.status_ok_code
    elif path == "organizations":
        return render_template('client/organizations.html', current_user=current_user), status_codes.status_ok_code
    elif path == "affiliates":
        return render_template('client/affiliates.html', current_user=current_user), status_codes.status_ok_code
    elif path == "users":
        return render_template('client/users.html', current_user=current_user), status_codes.status_ok_code
    elif path == "api-keys":
        return render_template('client/api_keys.html', current_user=current_user), status_codes.status_ok_code
    elif path == "accounts":
        return render_template('client/accounts.html', current_user=current_user), status_codes.status_ok_code
    elif path == "help-desk":
        return render_template('client/helpdesk.html', current_user=current_user), status_codes.status_ok_code



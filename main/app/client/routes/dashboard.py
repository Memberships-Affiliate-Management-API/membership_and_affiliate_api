***REMOVED***
    this is a private route
***REMOVED***
from flask import Blueprint, request, render_template, url_for, get_flashed_messages, redirect, flash
from database.users import UserModel
from main import app_cache
from security.users_authenticator import handle_users_auth
from utils.utils import return_ttl, can_cache
client_dashboard_bp = Blueprint('client_dashboard', __name__)


@client_dashboard_bp.route('/client/dashboard', methods=["GET"])
@handle_users_auth
def client_dashboard(current_user: UserModel) -> tuple:
    get_flashed_messages()
    if current_user:
        return render_template('client/dashboard.html')
    else:
        # TODO: insure local cache does not cache info if redirected
        flash('Please login or register to start using this app')
        return redirect(url_for('memberships_main.memberships_main_routes', path='login'))


@client_dashboard_bp.route('/client/dashboard/<path:path>', methods=["GET"])
@handle_users_auth
def client_dashboard_routes(current_user: UserModel, path: str) -> tuple:
    get_flashed_messages()
    if not current_user:
        flash('Please login or register to start using this app')
        return redirect(url_for('memberships_main.memberships_main_routes', path='login'))

    if path == "dashboard":
        return render_template('client/dashboard.html'), 200
    elif path == "organizations":
        return render_template('client/organizations.html'), 200
    elif path == "affiliates":
        return render_template('client/affiliates.html'), 200
    elif path == "users":
        return render_template('client/users.html'), 200
    elif path == "api-keys":
        return render_template('client/api_keys.html'), 200
    elif path == "accounts":
        return render_template('client/accounts.html'), 200
    elif path == "help-desk":
        return render_template('client/helpdesk.html'), 200



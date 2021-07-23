***REMOVED***
    this is a private route
***REMOVED***
from flask import Blueprint, request, render_template, url_for, get_flashed_messages
from security.users_authenticator import handle_users_auth

client_dashboard_bp = Blueprint('client_dashboard', __name__)


@client_dashboard_bp.route('/client/dashboard', methods=["GET"])
@handle_users_auth
def client_dashboard() -> tuple:
    return render_template('client/dashboard.html')


@client_dashboard_bp.route('/client/dashboard/<path:path>', methods=["GET"])
@handle_users_auth
def client_dashboard_routes(path: str) -> tuple:
    if path == "dashboard":
        return render_template('client/dashboard.html')
    elif path == "organizations":
        return render_template('client/organizations.html')
    elif path == "affiliates":
        return render_template('client/affiliates.html')
    elif path == "users":
        return render_template('client/users.html')
    elif path == "api-keys":
        return render_template('client/api_keys.html')
    elif path == "accounts":
        return render_template('client/accounts.html')
    elif path == "help-desk":
        return render_template('client/helpdesk.html')



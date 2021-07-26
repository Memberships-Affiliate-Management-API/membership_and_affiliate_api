from flask import Blueprint, render_template, url_for, get_flashed_messages
from security.users_authenticator import handle_users_auth

admin_dashboard_bp = Blueprint("admin_dashboard", __name__)


@admin_dashboard_bp.route("/admin/dashboard", methods=["GET"])
@handle_users_auth
def admin_dashboard() -> tuple:
    return render_template('admin/dashboard.html'), 200


@admin_dashboard_bp.route("/admin/dashboard/<path:path>", methods=["GET"])
@handle_users_auth
def admin_dashboard_routes(path: str) -> tuple:
    if path == "affiliates":
        return render_template('admin/affiliates.html'), 200
    elif path == "users":
        return render_template('admin/users.html'), 200
    elif path == "organizations":
        return render_template('admin/organizations.html'), 200
    elif path == "api-keys":
        return render_template('admin/api_keys.html'), 200
    elif path == "accounts":
        return render_template('admin/accounts.html'), 200
    elif path == "help-desk":
        return render_template('admin/helpdesk.html'), 200




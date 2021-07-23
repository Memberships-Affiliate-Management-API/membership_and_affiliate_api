from flask import Blueprint, render_template, url_for, get_flashed_messages
from security.users_authenticator import handle_users_auth

admin_dashboard_bp = Blueprint("admin_dashboard", __name__)


@admin_dashboard_bp.route("/admin/dashboard", methods=["GET"])
@handle_users_auth
def admin_dashboard() -> tuple:
    return render_template('dashboard.html')


@admin_dashboard_bp.route("/admin/dashboard/<path:path>", methods=["GET"])
@handle_users_auth
def admin_dashboard_routes(path: str) -> tuple:
    if path == "affiliates":
        return render_template('affiliates.html')
    elif path == "users":
        return render_template('users.html')
    elif path == "organizations":
        return render_template('organizations.html')
    elif path == "api-keys":
        return render_template('api_keys.html')






from flask import Blueprint, render_template
from security.users_authenticator import handle_users_auth

temp_folder = "../admin_templates/templates"
admin_dashboard_bp = Blueprint("admin_dashboard", __name__, template_folder=temp_folder)


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






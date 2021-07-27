from flask import Blueprint, render_template, url_for, get_flashed_messages, redirect, flash

from database.users import UserModel
from security.users_authenticator import handle_users_auth, logged_user

admin_dashboard_bp = Blueprint("admin_dashboard", __name__)


@admin_dashboard_bp.route("/admin/dashboard", methods=["GET"])
@logged_user
def admin_dashboard(current_user: UserModel) -> tuple:
    if current_user and current_user.is_admin:
        return render_template('admin/dashboard.html'), 200
    flash('This area is not for public use sorry')
    return redirect(url_for('memberships_main.memberships_main_routes', path='login'))


@admin_dashboard_bp.route("/admin/dashboard/<path:path>", methods=["GET"])
@logged_user
def admin_dashboard_routes(current_user: UserModel, path: str) -> tuple:
    if current_user and (not current_user.is_admin):
        flash('This area is not for public use sorry')
        return redirect(url_for('memberships_main.memberships_main_routes', path='login'))

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




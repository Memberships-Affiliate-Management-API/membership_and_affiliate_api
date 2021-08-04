from flask import Blueprint, render_template, url_for, get_flashed_messages, redirect, flash

from config.exceptions import status_codes
from database.users import UserModel
from main import app_cache
from security.users_authenticator import logged_user, is_app_admin
from utils.utils import return_ttl, can_cache

admin_dashboard_bp = Blueprint("admin_dashboard", __name__)


# noinspection PyTypeChecker
@admin_dashboard_bp.route("/admin/dashboard", methods=["GET"])
@logged_user
def admin_dashboard(current_user: UserModel) -> tuple:
    get_flashed_messages()

    if is_app_admin(current_user=current_user):
        return render_template('admin/dashboard.html'), status_codes.status_ok_code
    flash('This area is not for public use sorry')
    return redirect(url_for('memberships_main.memberships_main_routes', path='login'))


# noinspection PyTypeChecker
@admin_dashboard_bp.route("/admin/dashboard/<path:path>", methods=["GET"])
@logged_user
def admin_dashboard_routes(current_user: UserModel, path: str) -> tuple:
    get_flashed_messages()

    if is_app_admin(current_user=current_user):
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




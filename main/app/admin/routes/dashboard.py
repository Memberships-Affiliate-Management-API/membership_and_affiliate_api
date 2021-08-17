from typing import Optional
from flask import Blueprint, render_template, url_for, get_flashed_messages, redirect, flash
from config.exceptions import status_codes
from security.users_authenticator import logged_user, is_app_admin


admin_dashboard_bp = Blueprint("admin_dashboard", __name__)


@admin_dashboard_bp.route("/admin/dashboard", methods=["GET"])
@logged_user
def admin_dashboard(current_user: Optional[dict]) -> tuple:
    ***REMOVED***
        **admin_dashboard**
            home route for system admin dashboard
    :param current_user:
    :return:
    ***REMOVED***
    get_flashed_messages()
    if is_app_admin(current_user=current_user):
        return render_template('admin/dashboard.html', current_user=current_user), status_codes.status_ok_code

    flash('This area is not for public use sorry')
    return redirect(url_for('memberships_main.memberships_main_routes', path='login'))


# noinspection PyTypeChecker
@admin_dashboard_bp.route("/admin/dashboard/<path:path>", methods=["GET"])
@logged_user
def admin_dashboard_routes(current_user: Optional[dict], path: str) -> tuple:
    ***REMOVED***
            **admin_dashboard_routes**
                home route for system admin dashboard

        :param current_user:
        :param path:
        :return:
    ***REMOVED***

    get_flashed_messages()

    if is_app_admin(current_user=current_user):
        flash('This area is not for public use sorry')
        return redirect(url_for('memberships_main.memberships_main_routes', path='login'))

    if path == "affiliates":
        return render_template('admin/affiliates.html', current_user=current_user), status_codes.status_ok_code
    elif path == "users":
        return render_template('admin/users.html', current_user=current_user), status_codes.status_ok_code
    elif path == "organizations":
        return render_template('admin/organizations.html', current_user=current_user), status_codes.status_ok_code
    elif path == "api-keys":
        return render_template('admin/api_keys.html', current_user=current_user), status_codes.status_ok_code
    elif path == "accounts":
        return render_template('admin/accounts.html', current_user=current_user), status_codes.status_ok_code
    elif path == "help-desk":
        return render_template('admin/helpdesk.html', current_user=current_user), status_codes.status_ok_code

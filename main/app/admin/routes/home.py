from flask import Blueprint, render_template, url_for, get_flashed_messages
from security.users_authenticator import handle_users_auth


admin_bp = Blueprint("admin_home", __name__)


@admin_bp.route("/admin", methods=["GET"])
@handle_users_auth
def admin_home() -> tuple:
    ***REMOVED***
        **admin_home**
            admin home page
    :return:
    ***REMOVED***
    get_flashed_messages()
    return render_template('admin/home.html')



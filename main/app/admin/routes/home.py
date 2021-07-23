from flask import Blueprint, render_template
from security.users_authenticator import handle_users_auth

temp_folder = "../admin_templates/templates"
admin_bp = Blueprint("admin_home", __name__, template_folder=temp_folder)


@admin_bp.route("/admin", methods=["GET"])
@handle_users_auth
def admin_home() -> tuple:
    return render_template('home.html')



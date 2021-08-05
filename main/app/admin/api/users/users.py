from flask import Blueprint, request, render_template, url_for, get_flashed_messages, redirect, flash, jsonify
from config.exceptions import status_codes
from database.users import UserModel
from security.users_authenticator import logged_user, is_app_admin
from typing import Union

admin_users_api_bp = Blueprint("admin_users_api", __name__)


@admin_users_api_bp.route('/_api/admin/users/<string:path>', methods=["GET", "POST"])
def admin_users(path: str) -> tuple:
    ***REMOVED***
        # TODO decide on the authentication mechanism for admin section
    :param  path: indicates what route to follow for admin users
    :return:
    ***REMOVED***
    if path == "get":
        json_data: dict = request.get_json()
        organization_id: Union[str, None] = json_data.get("organization_id")
        uid: Union[str, None] = json_data.get("uid")

        user_instance: UserModel = UserModel.query(UserModel.organization_id == organization_id,
                                                   UserModel.uid == uid).get()

        message: str = "successfully retrieved user"
        return jsonify({'status': True, 'message': message,
                        'payload': user_instance.to_dict()}), status_codes.status_ok_code






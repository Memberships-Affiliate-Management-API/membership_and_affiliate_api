from flask import Blueprint, request, current_app, jsonify

from config import config_instance
from config.exceptions import error_codes, UnAuthenticatedError, if_bad_request_raise
from database.users import UserModel
from security.apps_authenticator import handle_apps_authentication
from security.users_authenticator import get_admin_user, encode_auth_token
from views.users import UserView
from typing import Optional

admin_users_api_bp = Blueprint("admin_users_api", __name__)


@admin_users_api_bp.route('/_api/v1/admin/users/<string:path>', methods=["GET", "POST"])
@handle_apps_authentication
def admin_users(path: str) -> tuple:
    ***REMOVED***
    :param  path: indicates what route to follow for admin users
    :return:
    ***REMOVED***
    # NOTE: only this application can call this endpoints-
    # For Purposes of authentication check if the calling url belongs to this app

    if_bad_request_raise(request)

    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get("SECRET_KEY")
    if not isinstance(secret_key, str) or secret_key != current_app.config.get('SECRET_KEY'):
        message: str = 'User Not Authorized: you cannot perform this action'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    if path == "get":
        organization_id: Optional[str] = json_data.get("organization_id")
        uid: Optional[str] = json_data.get("uid")
        user_view_instance: UserView = UserView()
        return user_view_instance.get_user(uid=uid, organization_id=organization_id)

    elif path == "is-user-unique":
        # checks if user exists based on either email or uid - used for administration purposes
        email: Optional[str] = json_data.get("email")
        uid: Optional[str] = json_data.get("uid")
        user_view_instance: UserView = UserView()
        return user_view_instance._system_user_exist(email=email, uid=uid)

    elif path == "login":
        email: Optional[str] = json_data.get("email")
        password: Optional[str] = json_data.get("password")
        uid: Optional[str] = json_data.get("uid")
        organization_id: Optional[str] = json_data.get("organization_id")
        user_view_instance: UserView = UserView()

        if email == config_instance.ADMIN_EMAIL and password == config_instance.ADMIN_PASSWORD \
                and uid == config_instance.ADMIN_UID and organization_id == config_instance.ORGANIZATION_ID:
            user_instance = get_admin_user()
            token = encode_auth_token(uid=uid)
            message: str = 'welcome admin'
            payload: dict = dict(token=token, user=user_instance)
            return jsonify({'status': True, 'payload': payload, 'message': message})

        raise UnAuthenticatedError()








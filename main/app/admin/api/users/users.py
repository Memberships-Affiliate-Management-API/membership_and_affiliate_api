from flask import Blueprint, request, current_app
from config.exceptions import error_codes, UnAuthenticatedError
from views.users import UserView
from typing import Optional

admin_users_api_bp = Blueprint("admin_users_api", __name__)


@admin_users_api_bp.route('/_api/admin/users/<string:path>', methods=["GET", "POST"])
def admin_users(path: str) -> tuple:
    ***REMOVED***
    :param  path: indicates what route to follow for admin users
    :return:
    ***REMOVED***
    # NOTE: only this application can call this endpoints-
    # For Purposes of authentication check if the calling url belongs to this app
    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get("secret_key")
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





from flask import Blueprint, request
from views.users import UserView
from typing import Union, Optional

admin_users_api_bp = Blueprint("admin_users_api", __name__)


@admin_users_api_bp.route('/_api/admin/users/<string:path>', methods=["GET", "POST"])
def admin_users(path: str) -> tuple:
    ***REMOVED***
        # TODO decide on the authentication mechanism for admin section
    :param  path: indicates what route to follow for admin users
    :return:
    ***REMOVED***
    # NOTE: only this application can call this endpoints-
    if path == "get":
        json_data: dict = request.get_json()
        organization_id: Union[str, None] = json_data.get("organization_id")
        uid: Union[str, None] = json_data.get("uid")
        user_view_instance: UserView = UserView()
        return user_view_instance.get_user(uid=uid, organization_id=organization_id)

    elif path == "is-user-unique":
        # checks if user exists based on either email or uid - used for administration purposes
        json_data: dict = request.get_json()
        print('JSON DAT: ', json_data)
        email: Optional[str] = json_data.get("email")
        uid: Optional[str] = json_data.get("uid")
        user_view_instance: UserView = UserView()
        return user_view_instance._system_user_exist(email=email, uid=uid)





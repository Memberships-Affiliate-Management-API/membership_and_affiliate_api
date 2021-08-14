from flask import Blueprint, request, current_app
from config.exceptions import error_codes, UnAuthenticatedError, if_bad_request_raise
from views.users import UserView
from typing import Optional

# TODO - Could move this to the main api if needed
client_users_api_bp = Blueprint("client_users_api", __name__)


@client_users_api_bp.route('/_api/v1/client/users/<string:path>', methods=["POST"])
def client_users(path: str) -> tuple:
    ***REMOVED***
        **client_users**
            this api endpoints are used by clients or developers in order to login into the main membership application
        :param path:
        :return:
    ***REMOVED***
    if_bad_request_raise(request)
    user_data: dict = request.get_json()
    secret_key: Optional[str] = user_data.get("SECRET_KEY")
    user_view_instance: UserView = UserView()

    if not isinstance(secret_key, str) or secret_key != current_app.config.get('SECRET_KEY'):
        message: str = 'User Not Authorized: you cannot perform this action'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    if path == "login":
        email: Optional[str] = user_data.get("email")
        password: Optional[str] = user_data.get("password")
        organization_id: Optional[str] = user_data.get("organization_id")
        # Note error checking will be performed on View
        return user_view_instance.login(organization_id=organization_id, email=email, password=password)

    elif path == "logout":

        # TODO- handle logout procedure
        return "OK", 200

    elif path == "register":
        email: Optional[str] = user_data.get("email")
        cell: Optional[str] = user_data.get("cell")
        password: Optional[str] = user_data.get("password")
        names: Optional[str] = user_data.get("names")
        surname: Optional[str] = user_data.get("surname")
        organization_id: Optional[str] = user_data.get("organization_id")

        return user_view_instance.add_user(organization_id=organization_id, names=names, surname=surname, cell=cell,
                                           email=email, password=password)

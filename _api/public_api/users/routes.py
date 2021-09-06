"""
***Users Management API***

"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import typing
from flask import Blueprint, request, jsonify
from config.exceptions import if_bad_request_raise
from security.api_authenticator import handle_api_auth
from views import user_view

users_bp = Blueprint("users", __name__)


# TODO - include organization_id for this routes, and refactor the view functions


def get_kwargs(user_data: dict) -> tuple:
    uid: typing.Union[str, None] = user_data.get("uid")
    email: typing.Union[str, None] = user_data.get("email")
    cell: typing.Union[str, None] = user_data.get("cell")
    organization_id: typing.Union[str, None] = user_data.get("organization_id")
    return organization_id, uid, email, cell


@users_bp.route("/api/v1/public/user/create-user", methods=["POST"])
@handle_api_auth
def create_user() -> tuple:
    """
        given user details create new user
        :return: json response as tuple
    """
    # created new user
    user_data: dict = request.get_json()
    names: str = user_data.get("names")
    surname: str = user_data.get("surname")
    cell: str = user_data.get("cell")
    email: str = user_data.get("email")
    password: str = user_data.get("password")
    uid: str = user_data.get("uid")
    organization_id: str = user_data.get("organization_id")

    # Add User View will perform error checking
    return user_view.add_user(organization_id=organization_id, uid=uid, names=names, surname=surname,
                              cell=cell, email=email, password=password)


# NOTE: use "<uid>@<organization_id>" as path to obtain user
@users_bp.route("/api/v1/public/user/<path:path>", methods=["GET", "POST"])
@handle_api_auth
def user(path: str) -> tuple:
    """
        update or get a specific user by uid
        :param path:
        :return: json response as tuple
    """

    if request.method == "GET":
        # get a specific user
        uid, organization_id = path.split("@")
        return user_view.get_user(organization_id=organization_id, uid=uid)
    else:
        # Updating user details
        if path == "update":
            user_data: dict = request.get_json()
            uid: str = user_data.get("uid")
            organization_id: str = user_data.get("organization_id")
            names: str = user_data.get("names")
            surname: str = user_data.get("surname")
            cell: str = user_data.get("cell")
            email: str = user_data.get("email")
            is_admin: bool = user_data.get('is_admin')
            is_support: bool = user_data.get('is_support')
            return user_view.update_user(organization_id=organization_id, uid=uid, names=names,
                                         surname=surname, cell=cell, email=email, is_admin=is_admin,
                                         is_support=is_support)
        elif path == "delete":
            user_data: dict = request.get_json()
            organization_id, uid, email, cell = get_kwargs(user_data=user_data)
            return user_view.delete_user(organization_id=organization_id, uid=uid, email=email, cell=cell)
        elif path == "get":
            user_data: dict = request.get_json()
            organization_id, uid, email, cell = get_kwargs(user_data=user_data)
            return user_view.get_user(organization_id=organization_id, uid=uid, email=email, cell=cell)


@users_bp.route("/api/v1/public/users/<string:path>", methods=["GET", "POST"])
@handle_api_auth
def get_all(path: str) -> tuple:
    """
        get all , active or in-active users
        :param path:
        :return: json response as tuple
    """
    if path == "all":
        user_data: dict = request.get_json()
        organization_id: str = user_data.get("organization_id")
        return user_view.get_all_users(organization_id=organization_id)
    if path == "active":
        user_data: dict = request.get_json()
        organization_id: str = user_data.get("organization_id")
        return user_view.get_active_users(organization_id=organization_id)
    if path == "in-active":
        user_data: dict = request.get_json()
        organization_id: str = user_data.get("organization_id")
        return user_view.get_in_active_users(organization_id=organization_id)

    return jsonify({"status": False, "message": "general error fetching users"}), 500


@users_bp.route("/api/v1/public/check-password", methods=["POST"])
@handle_api_auth
def check_password() -> tuple:
    """
        given a password in json check if it matches the hash in file
        :return:
    """
    user_data: dict = request.get_json()
    uid: str = user_data.get("uid")
    organization_id: str = user_data.get("organization_id")
    password: str = user_data.get("password")

    return user_view.check_password(organization_id=organization_id, uid=uid, password=password)


@users_bp.route("/api/v1/public/deactivate-user", methods=["POST"])
@handle_api_auth
def de_activate_user() -> tuple:
    """
        given uid in json de-activate user
        :return: json as tuple
    """
    user_data: dict = request.get_json()
    uid: str = user_data.get("uid")
    organization_id: str = user_data.get("organization_id")

    return user_view.deactivate_user(organization_id=organization_id, uid=uid)


@users_bp.route("/api/v1/public/auth/login", methods=["POST"])
@handle_api_auth
def login() -> tuple:
    """
        **login**
            called by main application in order to login
    :return:
    """

    user_data: dict = request.get_json()
    email: typing.Union[str, None] = user_data.get("email")
    password: typing.Union[str, None] = user_data.get("password")
    organization_id: typing.Union[str, None] = user_data.get("organization_id")
    # Note error checking will be performed on View
    return user_view.login(organization_id=organization_id, email=email, password=password)


@users_bp.route("/api/v1/public/auth/logout", methods=["POST"])
@handle_api_auth
def logout() -> tuple:
    """
        **logout public api**
    :return:
    """
    # Raises Bad Request error if request is not in json format
    if_bad_request_raise(request)
    user_data: dict = request.get_json()
    # TODO- handle logout procedure
    return "OK", 200


@users_bp.route("/api/v1/public/auth/register", methods=["POST"])
@handle_api_auth
def register() -> tuple:
    # Raises Bad Request error if request is not in json format
    if_bad_request_raise(request)
    user_data: dict = request.get_json()

    email: str = user_data.get("email")
    cell: str = user_data.get("cell")
    password: str = user_data.get("password")
    names: str = user_data.get("names")
    surname: str = user_data.get("surname")
    organization_id: typing.Union[str, None] = user_data.get("organization_id")

    return user_view.add_user(organization_id=organization_id, names=names, surname=surname, cell=cell,
                              email=email, password=password)

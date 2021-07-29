import typing
from flask import Blueprint, request, jsonify
from security.api_authenticator import handle_api_auth
from views.users import UserView
users_bp = Blueprint("users", __name__)


# TODO - include organization_id for this routes, and refactor the view functions


def get_kwargs(user_data: dict) -> tuple:
    if ("uid" in user_data) and (user_data["uid"] != ""):
        uid: typing.Union[str, None] = user_data.get("uid")
    else:
        uid: typing.Union[str, None] = None
    if ("email" in user_data) and (user_data["email"] != ""):
        email: typing.Union[str, None] = user_data.get("email")
    else:
        email: typing.Union[str, None] = None
    if ("cell" in user_data) and (user_data["cell"] != ""):
        cell: typing.Union[str, None] = user_data.get("cell")
    else:
        cell: typing.Union[str, None] = None
    if ("organization_id" in user_data) and (user_data["organization_id"] != ""):
        organization_id: typing.Union[str, None] = user_data.get("organization_id")
    else:
        pass

    return organization_id, uid, email, cell


@users_bp.route("/api/v1/create-user", methods=["POST"])
@handle_api_auth
def create_user() -> tuple:
    ***REMOVED***
        given user details create new user
        :return: json response as tuple
    ***REMOVED***
    # created new user
    user_data: dict = request.get_json()
    users_view_instance: UserView = UserView()
    names: str = user_data.get("names")
    surname: str = user_data.get("surname")
    cell: str = user_data.get("cell")
    email: str = user_data.get("email")
    password: str = user_data.get("password")
    uid: str = user_data.get("uid")
    return users_view_instance.add_user(names=names, surname=surname, cell=cell,
                                        email=email, password=password, uid=uid)


# NOTE: use "<uid>@<organization_id>" as path to obtain user
@users_bp.route("/api/v1/user/<path:path>", methods=["GET", "POST"])
@handle_api_auth
def user(path: str) -> tuple:
    ***REMOVED***
        update or get a specific user by uid
        :param path:
        :return: json response as tuple
    ***REMOVED***

    users_view_instance: UserView = UserView()
    if request.method == "GET":
        # get a specific user
        uid, organization_id = path.split("@")
        return users_view_instance.get_user(organization_id=organization_id, uid=uid)
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
            return users_view_instance.update_user(organization_id=organization_id, uid=uid, names=names,
                                                   surname=surname, cell=cell, email=email, is_admin=is_admin,
                                                   is_support=is_support)
        elif path == "delete":
            user_data: dict = request.get_json()
            organization_id, uid, email, cell = get_kwargs(user_data=user_data)
            return users_view_instance.delete_user(organization_id=organization_id, uid=uid, email=email, cell=cell)
        elif path == "get":
            user_data: dict = request.get_json()
            organization_id, uid, email, cell = get_kwargs(user_data=user_data)
            return users_view_instance.get_user(organization_id=organization_id, uid=uid, email=email, cell=cell)


@users_bp.route("/api/v1/users/<path:path>", methods=["GET", "POST"])
@handle_api_auth
def get_all(path: str) -> tuple:
    ***REMOVED***
        get all , active or in-active users
        :param path:
        :return: json response as tuple
    ***REMOVED***
    if path == "all":
        user_data: dict = request.get_json()
        organization_id: str = user_data.get("organization_id")
        users_view_instance: UserView = UserView()
        return users_view_instance.get_all_users(organization_id=organization_id)
    if path == "active":
        user_data: dict = request.get_json()
        organization_id: str = user_data.get("organization_id")
        users_view_instance: UserView = UserView()
        return users_view_instance.get_active_users(organization_id=organization_id)
    if path == "in-active":
        user_data: dict = request.get_json()
        organization_id: str = user_data.get("organization_id")
        users_view_instance: UserView = UserView()
        return users_view_instance.get_in_active_users(organization_id=organization_id)

    return jsonify({"status": False, "message": "general error fetching users"}), 500


@users_bp.route("/api/v1/check-password", methods=["POST"])
@handle_api_auth
def check_password() -> tuple:
    ***REMOVED***
        given a password in json check if it matches the hash in file
        :return:
    ***REMOVED***
    user_data: dict = request.get_json()
    uid: str = user_data.get("uid")
    organization_id: str = user_data.get("organization_id")
    password: str = user_data.get("password")
    user_view_instance: UserView = UserView()
    return user_view_instance.check_password(organization_id=organization_id, uid=uid, password=password)


@users_bp.route("/api/v1/deactivate-user", methods=["POST"])
@handle_api_auth
def de_activate_user() -> tuple:
    ***REMOVED***
        given uid in json de-activate user
        :return: json as tuple
    ***REMOVED***
    user_data: dict = request.get_json()
    uid: str = user_data.get("uid")
    organization_id: str = user_data.get("organization_id")
    user_view_instance: UserView = UserView()
    return user_view_instance.deactivate_user(organization_id=organization_id, uid=uid)


@users_bp.route("/api/v1/auth/login", methods=["POST"])
@handle_api_auth
def login() -> tuple:
    # TODO- clients for users login handle it here the procedure is not clear
    user_view_instance: UserView = UserView()
    user_data: dict = request.get_json()

    if ("email" in user_data) and (user_data["email"] != ""):
        email: typing.Union[str, None] = user_data.get("email")
    else:
        return jsonify({"status": False,  "message": "email is required"}), 500

    if ("password" in user_data) and (user_data["password"] != ""):
        password: typing.Union[str, None] = user_data.get("password")
    else:
        return jsonify({"status": False, "message": "password is required"}), 500

    if ("organization_id" in user_data) and (user_data["organization_id"] != ""):
        organization_id: typing.Union[str, None] = user_data.get("organization_id")
    else:
        return jsonify({"status": False, "message": "an organization to login into is needed"}), 500

    return user_view_instance.login(organization_id=organization_id, email=email, password=password)


@users_bp.route("/api/v1/auth/logout", methods=["POST"])
@handle_api_auth
def logout() -> tuple:
    user_view_instance: UserView = UserView()
    user_data: dict = request.get_json()
    # TODO- handle logout procedure
    return "OK", 200


@users_bp.route("/api/v1/auth/register", methods=["POST"])
@handle_api_auth
def register() -> tuple:

    user_view_instance: UserView = UserView()
    user_data: dict = request.get_json()

    if ("email" in user_data) and (user_data["email"] != ""):
        email: str = user_data.get("email")
    else:
        return jsonify({"status": False, "message": "Email is required"}), 500

    if ("cell" in user_data) and (user_data["cell"] != ""):
        cell: str = user_data.get("cell")
    else:
        return jsonify({"status": False, "message": "Cell is Required"})

    if ("password" in user_data) and (user_data["password"] != ""):
        password: str = user_data.get("password")
    else:
        return jsonify({"status": False, "message": "Password is required"}), 500

    if ("names" in user_data) and (user_data["names"] != ""):
        names: str = user_data.get("names")
    else:
        return jsonify({"status": False, "message": "Names is required"}), 500

    if ("surname" in user_data) and (user_data["surname"] != ""):
        surname: str = user_data.get("surname")
    else:
        return jsonify({"status": False, "message": "Surname is required"}), 500

    if ("organization_id" in user_data) and (user_data["organization_id"] != ""):
        organization_id: typing.Union[str, None] = user_data.get("organization_id")
    else:
        return jsonify({"status": False, "message": "Organization is required"}), 500

    return user_view_instance.add_user(organization_id=organization_id, names=names, surname=surname, cell=cell,
                                       email=email, password=password)

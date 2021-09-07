"""
    **github_users module**
        admin routes for github authentication users data


"""
from flask import Blueprint, request
from config.exceptions import if_bad_request_raise
from security.apps_authenticator import handle_apps_authentication
from views.github_auth import GithubAuthView

client_github_users_api_bp = Blueprint('client_github_users_api', __name__)


@client_github_users_api_bp.route('/_api/v1/client/github-users/', methods=['POST', 'GET'])
@handle_apps_authentication
def github_users_api() -> tuple:
    """
        **github users client api**

    :return:
    """
    if_bad_request_raise(request)
    pass

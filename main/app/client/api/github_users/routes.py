***REMOVED***
    **github_users module**
        admin routes for github authentication users data


***REMOVED***
from flask import Blueprint
from views.github_auth import GithubAuthView

github_users_api_bp = Blueprint('github_users_api', __name__)


@github_users_api_bp.route('/_api/client/github-users/', methods=['POST', 'GET'])
def github_users_api() -> tuple:
    ***REMOVED***
        **github users client api**

    :return:
    ***REMOVED***
    pass

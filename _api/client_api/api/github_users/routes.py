***REMOVED***
    **github_users module**
        admin routes for github authentication users data


***REMOVED***
from flask import Blueprint

from config.exceptions import if_bad_request_raise
from views.github_auth import GithubAuthView

client_github_users_api_bp = Blueprint('client_github_users_api', __name__)


@client_github_users_api_bp.route('/_api/v1/client/github-users/', methods=['POST', 'GET'])
def github_users_api() -> tuple:
    ***REMOVED***
        **github users client api**

    :return:
    ***REMOVED***
    if_bad_request_raise(request)
    pass

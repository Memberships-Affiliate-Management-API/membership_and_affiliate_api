***REMOVED***
    **Users Management Cron Jobs**
    check if users have been login in , if not then send messages to inform user that their subscription is still activate
    if they have one
***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
from flask import Blueprint
cron_users_bp = Blueprint('cron_users', __name__)


@cron_users_bp.route('/_cron/v1/users', methods=['POST', 'GET'])
def cron_users_jobs():
    ***REMOVED***

    :return:
    ***REMOVED***
    pass
"""
    **Users Management Cron Jobs**
    check if users have been login in , if not then send messages to inform user that their subscription is still activate
    if they have one
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from flask import Blueprint
from _cron.jobs.users_jobs import UserJobs
from config.exceptions import status_codes
from security.apps_authenticator import handle_cron_auth

cron_users_bp = Blueprint('cron_users', __name__)


@cron_users_bp.route('/_cron/v1/users', methods=['POST', 'GET'])
@handle_cron_auth
def cron_users_jobs() -> tuple:
    """
    **cron_users_jobs**
        user cron jobs, will run cron services needed to manage users
    :return: tuple
    """
    user_jobs_instance: UserJobs = UserJobs()
    user_jobs_instance.run()
    return "OK", status_codes.status_ok_code

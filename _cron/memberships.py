"""
    **Memberships Management Cron Jobs**
    runs tasks to:
        1. check if users paid for their membership plans
            1.a if not paid then check if grace period has expired, if it expired then downgrade plan to unpaid plan
            1.b send notifications to users of actions taken here
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from flask import Blueprint
from _cron.jobs.membership_jobs import MembershipsJobs
from config.exceptions import status_codes
from schedulers.scheduler import schedule_func
from security.apps_authenticator import handle_apps_authentication, handle_cron_auth

cron_memberships_bp = Blueprint('cron_memberships', __name__)


@cron_memberships_bp.route('/_cron/v1/memberships', methods=['GET', 'POST'])
@handle_cron_auth
def cron_memberships_jobs() -> tuple:
    """
        **cron_memberships_jobs**
            memberships cron jobs, will be responsible for the following:
                1. check payment status for each plan -
                if not paid check grace period if expired then expire membership
    :return:
    """
    memberships_jobs_instance: MembershipsJobs = MembershipsJobs()

    schedule_func(func=memberships_jobs_instance.run,
                  job_name='cron_memberships_jobs')
    return "OK", status_codes.status_ok_code

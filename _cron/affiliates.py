"""
    **Affiliate Management Cron Jobs**

    check if an affiliate is due to be paid, if yes then send payment to wallet

    send affiliate report to users detailing how their recruitment have faired this month and also
    the status of their income
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from flask import Blueprint
from _cron.jobs.affiliates_jobs import AffiliateJobs
from config.exceptions import status_codes
from schedulers.scheduler import schedule_func
from security.apps_authenticator import handle_apps_authentication, handle_cron_auth

cron_affiliate_bp = Blueprint('cron_affiliate', __name__)


@cron_affiliate_bp.route('/_cron/v1/affiliates', methods=['POST', 'GET'])
@handle_cron_auth
def cron_affiliate_jobs() -> tuple:
    """
        **cron_affiliate_jobs**
            affiliate related cron jobs - for checking and
                1. finalizing affiliate payments.
                2. sending finalized amounts to wallets
                3. sending affiliate report - recruitments & earnings
    :return:
    """
    affiliate_cron_tasks: AffiliateJobs = AffiliateJobs()

    schedule_func(func=affiliate_cron_tasks.run, job_name='cron_affiliate')
    return "OK", status_codes.status_ok_code

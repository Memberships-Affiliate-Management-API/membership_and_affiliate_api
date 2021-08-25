***REMOVED***
    **Affiliate Management Cron Jobs**

    check if an affiliate is due to be paid, if yes then send payment to wallet

    send affiliate report to users detailing how their recruitment have faired this month and also
    the status of their income
***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from flask import Blueprint
from _cron.jobs.affiliates_jobs import AffiliateCronTasks
cron_affiliate_bp = Blueprint('cron_affiliate', __name__)


@cron_affiliate_bp.route('/_cron/v1/affiliates', methods=['POST', 'GET'])
def cron_affiliate_jobs():
    ***REMOVED***
        **cron_affiliate_jobs**
            affiliate related cron jobs - for checking and
                1. finalizing affiliate payments.
                2. sending finalized amounts to wallets
                3. sending affiliate report - recruitments & earnings
    :return:
    ***REMOVED***
    # TODO add authentication on this route
    affiliate_cron_tasks: AffiliateCronTasks = AffiliateCronTasks()
    affiliate_cron_tasks.run()

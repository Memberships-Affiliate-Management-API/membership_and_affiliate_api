***REMOVED***
    **Withdrawals Management Cron Jobs**
    runs a job to send approved withdrawals to withdrawals paypal accounts
***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
from flask import Blueprint
cron_withdrawals_bp = Blueprint('cron_withdrawals', __name__)


@cron_withdrawals_bp.route('/_cron/v1/withdrawals', methods=['POST', 'GET'])
def cron_withdrawals_jobs():
    ***REMOVED***

    :return:
    ***REMOVED***
    pass
"""
    **Withdrawals Management Cron Jobs**
    runs a job to send approved withdrawals to withdrawals paypal accounts
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
from flask import Blueprint
from _cron.jobs.transactions_jobs import TransactionsJobs
from config.exceptions import status_codes
from schedulers.scheduler import schedule_func
from security.apps_authenticator import handle_apps_authentication, handle_cron_auth

cron_transactions_bp = Blueprint('cron_withdrawals', __name__)


@cron_transactions_bp.route('/_cron/v1/transactions', methods=['POST', 'GET'])
@handle_cron_auth
def cron_transactions_jobs() -> tuple:
    """
        **cron_withdrawals_jobs**
            Manages Approved withdrawals - 0726177953
            actually sends approved withdrawals to users paypal wallets
    :return:
    """
    transactions: TransactionsJobs = TransactionsJobs()
    schedule_func(func=transactions.run, job_name='cron_transactions_jobs')
    return "OK", status_codes.status_ok_code

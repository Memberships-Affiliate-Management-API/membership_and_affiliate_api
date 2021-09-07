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
from security.apps_authenticator import handle_apps_authentication

cron_transactions_bp = Blueprint('cron_withdrawals', __name__)


@cron_transactions_bp.route('/_cron/v1/transactions', methods=['POST', 'GET'])
@handle_apps_authentication
def cron_transactions_jobs() -> tuple:
    """
        **cron_withdrawals_jobs**
            Manages Approved withdrawals - 0726177953
            actually sends approved withdrawals to users paypal wallets
    :return:
    """
    transactions: TransactionsJobs = TransactionsJobs()
    transactions.run()
    return "OK", status_codes.status_ok_code

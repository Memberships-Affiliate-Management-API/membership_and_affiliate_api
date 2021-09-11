import asyncio
from typing import List, Coroutine, Optional
from flask import current_app
from google.cloud import ndb
from google.cloud.ndb import toplevel, tasklet, Future, wait_all

from config.use_context import use_context
from database.mixins import AmountMixin
from database.wallet import WalletTransactionsModel, WalletModel


class TransactionsJobs:
    """
    **TransactionsJobs**
        withdrawals and deposits cron jobs
    """

    def __init__(self):
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @use_context
    @toplevel
    def run(self):
        approved_withdrawals = yield self.send_approved_withdrawals_to_paypal_wallets()
        approved_deposits = yield self.add_approved_deposits_to_wallet()

    @tasklet
    def do_send_to_client_paypal(self, transaction: WalletTransactionsModel) -> Future:
        """
        **do_send_to_client_paypal**
            send withdrawal amount to the client's paypal account
        :param transaction: contains a record of the transaction
        :return: bool indicating success or failure
        """
        # TODO use paypal SDK to send transactions to paypal here
        # TODO then update transaction to reflect that transaction was sent
        # NOTE: Could also listen to an _ipn to find out if transaction succeeded on paypal side
        wallet_instance: WalletModel = WalletModel.query(
            WalletModel.organization_id == transaction.organization_id, WalletModel.uid == transaction.uid).get_async().get_result()

        if wallet_instance.is_verified:
            paypal_address = wallet_instance.paypal_address
            amount_to_send: AmountMixin = transaction.amount
            # TODO send amount to paypal using paypal address from wallet and amount from transactions
            transaction.is_settled = True
            tran_key: Optional[ndb.Key] = transaction.put_async(retries=self._max_retries,
                                                                timeout=self._max_timeout).get_result()
            yield bool(tran_key)
        yield False

    @tasklet
    def send_approved_withdrawals_to_paypal_wallets(self) -> List[Future]:
        """
            **send_approved_withdrawals_to_paypal_wallets**
                fetches all processed and approved withdrawals and schedule them for sending to the client
                paypal wallet address

            :return: None
        """
        wallet_transactions: List[WalletTransactionsModel] = WalletTransactionsModel.query(
            WalletTransactionsModel.is_verified == True, WalletTransactionsModel.is_settled == False).fetch_async().get_result()
        print('approved withdrawals running')
        return [self.do_send_to_client_paypal(transaction=transaction) for transaction in wallet_transactions
                if transaction.transaction_type == 'withdrawal']

    # Note below methods deals with client deposits
    @tasklet
    def do_send_to_client_wallet(self, transaction: WalletTransactionsModel) -> Future:
        """
        **do_send_to_client_wallet**
            send the deposit to client wallet

        :param transaction: contains the deposit amount
        :return: bool indicating success or failure
        """
        # requesting the user wallet
        wallet_instance: WalletModel = WalletModel.query(
            WalletModel.organization_id == transaction.organization_id, WalletModel.uid == transaction.uid).get_async().get_result()

        is_currency_valid: bool = wallet_instance.available_funds.currency == transaction.amount.currency
        if isinstance(wallet_instance, WalletModel) and is_currency_valid:
            wallet_instance.available_funds.amount_cents += transaction.amount.amount_cents
            key: Optional[ndb.Key] = wallet_instance.put_async(
                retries=self._max_retries, timeout=self._max_timeout).get_result()
            if bool(key):
                transaction.is_settled = True
                tran_key: Optional[ndb.Key] = transaction.put_async(retries=self._max_retries,
                                                                    timeout=self._max_timeout).get_result()
                yield bool(tran_key)
        yield False

    @tasklet
    def add_approved_deposits_to_wallet(self) -> List[Future]:
        """
        **add_approved_deposits_to_wallet**
        fetches all processed deposits which are not yet settled and then adding them to the client wallet

        :return: None
        """
        wallet_transactions: List[WalletTransactionsModel] = WalletTransactionsModel.query(
            WalletTransactionsModel.is_verified == True, WalletTransactionsModel.is_settled == False).fetch_async().get_result()
        print("approved deposits running")
        return [self.do_send_to_client_wallet(transaction=transaction) for transaction in wallet_transactions
                if transaction.transaction_type == 'deposit']

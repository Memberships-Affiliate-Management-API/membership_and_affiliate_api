import asyncio
from typing import List, Coroutine, Optional
from flask import current_app
from google.cloud import ndb
from config.use_context import use_context
from database.wallet import WalletTransactionsModel, WalletModel


class TransactionsJobs:
    ***REMOVED***
    **TransactionsJobs**
        withdrawals and deposits cron jobs
    ***REMOVED***

    def __init__(self):
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    def run(self):
        asyncio.run(self.send_approved_withdrawals_to_paypal_wallets())
        asyncio.run(self.add_approved_deposits_to_wallet())

    async def do_send_to_client_paypal(self, transaction: WalletTransactionsModel) -> bool:
        ***REMOVED***

        :param transaction:
        :return:
        ***REMOVED***
        # TODO use paypal SDK to send transactions to paypal here
        # TODO then update transaction to reflect that transaction was sent
        # NOTE: Could also listen to an _ipn to find out if transaction succeeded on paypal side
        wallet_instance: WalletModel = await WalletModel.query(
            WalletModel.organization_id == transaction.organization_id, WalletModel.uid == transaction.uid).get_async()

        if wallet_instance.is_verified:
            paypal_address = wallet_instance.paypal_address
            amount = transaction.amount
            # TODO send amount to paypal using paypal address from wallet and amount from transactions
            transaction.is_settled = True
            tran_key: Optional[ndb.Key] = transaction.put_async(retries=self._max_retries,
                                                                timeout=self._max_timeout).get_result()
            return bool(tran_key)
        return False

    @use_context
    async def send_approved_withdrawals_to_paypal_wallets(self):
        ***REMOVED***
            **send_approved_withdrawals_to_paypal_wallets**

            :return:
        ***REMOVED***
        wallet_transactions: List[WalletTransactionsModel] = await WalletTransactionsModel.query(
            WalletTransactionsModel.is_verified == True, WalletTransactionsModel.is_settled == False).fetch_async()
        cron: List[Coroutine] = [self.do_send_to_client_paypal(transaction=transaction) for transaction in wallet_transactions
                                 if transaction.transaction_type == 'withdrawal']
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(asyncio.gather(cron))
        event_loop.close()

    # Note below methods deals with client deposits
    async def do_send_to_client_wallet(self, transaction: WalletTransactionsModel) -> bool:
        ***REMOVED***
        **do_send_to_client_wallet**
            send the deposit to client wallet

        :param transaction:
        :return:
        ***REMOVED***
        # requesting the user wallet
        wallet_instance: WalletModel = await WalletModel.query(
            WalletModel.organization_id == transaction.organization_id, WalletModel.uid == transaction.uid).get_async()

        is_currency_valid: bool = wallet_instance.available_funds.currency == transaction.amount.currency
        if isinstance(wallet_instance, WalletModel) and is_currency_valid:
            wallet_instance.available_funds.amount += transaction.amount.amount
            key: Optional[ndb.Key] = wallet_instance.put_async(
                retries=self._max_retries, timeout=self._max_timeout).get_result()
            if bool(key):
                transaction.is_settled = True
                tran_key: Optional[ndb.Key] = transaction.put_async(retries=self._max_retries,
                                                                    timeout=self._max_timeout).get_result()
                return bool(tran_key)
        return False

    @use_context
    async def add_approved_deposits_to_wallet(self):
        wallet_transactions: List[WalletTransactionsModel] = await WalletTransactionsModel.query(
            WalletTransactionsModel.is_verified == True, WalletTransactionsModel.is_settled == False).fetch_async()
        cron: List[Coroutine] = [self.do_send_to_client_wallet(transaction=transaction) for transaction in wallet_transactions
                                 if transaction.transaction_type == 'deposit']
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(asyncio.gather(cron))
        event_loop.close()


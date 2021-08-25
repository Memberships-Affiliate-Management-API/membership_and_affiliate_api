import asyncio
from typing import List, Coroutine
from database.wallet import WalletTransactionsModel, WalletModel


class WithdrawalsJobs:

    def __init__(self):
        pass

    def run(self):
        asyncio.run(self.send_approved_withdrawals_to_paypal_wallets())

    async def do_send_to_paypal(self, transaction: WalletTransactionsModel) -> bool:
        ***REMOVED***

        :param transaction:
        :return:
        ***REMOVED***
        # TODO use paypal SDK to send transactions to paypal here
        # TODO then update transaction to reflect that transaction was sent
        # NOTE: Could also listen to an _ipn to find out if transaction succeeded on paypal side
        pass

    async def send_approved_withdrawals_to_paypal_wallets(self):
        ***REMOVED***

            :return:
        ***REMOVED***
        wallet_transactions: List[WalletTransactionsModel] = await WalletTransactionsModel.query(
            WalletTransactionsModel.is_verified == True, WalletTransactionsModel.is_settled == False).fetch_async()
        cron: List[Coroutine] = [self.do_send_to_paypal(transaction=transaction) for transaction in wallet_transactions]
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(asyncio.gather(cron))
        event_loop.close()




***REMOVED***
        **affiliate_jobs**



***REMOVED***
import asyncio
from datetime import datetime, date
from typing import List, Coroutine, Optional
from flask import current_app
from google.cloud import ndb
from config.use_context import use_context
from database.affiliates import EarningsData, AffiliateTransactionItems
from database.mixins import AmountMixin
from database.wallet import WalletModel
from utils import create_id


class AffiliateJobs:
    ***REMOVED***
    **Class AffiliateJobs**
        runs affiliate cron jobs to complete recurring tasks

    ***REMOVED***

    def __init__(self):
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    def run(self):
        asyncio.run(self.finalize_affiliate_earnings())
        asyncio.run(self.create_affiliate_reports())

    async def do_finalize_earnings(self, earnings: EarningsData) -> bool:
        ***REMOVED***
            go through each affiliate payment record,
            1. then transfer earnings to wallet,
            2. close earnings record
            3. create a transaction on earnings transaction

        :param earnings:
        :return:
        ***REMOVED***
        wallet_instance: WalletModel = await WalletModel.query(WalletModel.organization_id == earnings.organization_id,
                                                               WalletModel.uid == earnings.affiliate_id).get_async()

        if wallet_instance.is_verified and (wallet_instance.available_funds.currency == earnings.total_earned.currency):
            wallet_instance.available_funds.amount += earnings.total_earned.amount
            key: Optional[ndb.Key] = wallet_instance.put_async(retries=self._max_retries,
                                                               timeout=self._max_timeout).get_result()
            if bool(key):
                amount_earned: AmountMixin = earnings.total_earned
                earnings.total_earned.amount = 0
                today: date = datetime.now().date()
                earnings.start_date = today
                earnings.last_updated = today
                earnings.is_paid = True
                earnings_key: Optional[ndb.Key] = earnings.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
                if bool(earnings_key):
                    transaction_item: AffiliateTransactionItems = AffiliateTransactionItems()
                    transaction_item.amount = amount_earned
                    transaction_item.transaction_id = create_id()
                    transaction_item.uid = earnings.affiliate_id
                    tran_key: Optional[ndb.Key] = transaction_item.put_async(retries=self._max_retries,
                                                                             timeout=self._max_timeout).get_result()

                    return True
        return False

    @use_context
    async def finalize_affiliate_earnings(self):
        ***REMOVED***
        **finalize_affiliate_payments**
            go through each affiliate payment record,
            1. then transfer earnings to wallet,
            2. close earnings record
            3. create a transaction on earnings transaction
        :return:
        ***REMOVED***
        earnings_list: List[EarningsData] = await EarningsData.query(EarningsData.is_paid == False,
                                                                     EarningsData.on_hold == False).fetch_async()
        event_loop = asyncio.get_event_loop()
        coro: List[Coroutine] = [self.do_finalize_earnings(earnings=earning) for earning in earnings_list]
        event_loop.run_until_complete(asyncio.gather(coro))
        event_loop.close()

    async def create_affiliate_reports(self):
        pass

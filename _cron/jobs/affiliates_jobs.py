"""
        **affiliate_jobs**

"""
import asyncio
from datetime import datetime, date
from typing import List, Coroutine, Optional
from google.cloud.ndb import Key as ndb_Key, tasklet, toplevel, Future
from database.affiliates import EarningsData, AffiliateTransactionItems
from database.mixins import AmountMixin
from database.wallet import WalletModel
from utils import create_id
from config import config_instance


class AffiliateJobs:
    """
    **Class AffiliateJobs**
        runs affiliate cron jobs to complete recurring tasks

    """

    def __init__(self):
        self._max_retries = config_instance.DATASTORE_RETRIES
        self._max_timeout = config_instance.DATASTORE_TIMEOUT

    @toplevel
    def run(self):
        final_earnings = yield self.finalize_affiliate_earnings()
        for finalized_earning in final_earnings:
            print(f"finalized earnings: {finalized_earning}")
        print(f"unable to find any earnings")

    @tasklet
    def do_finalize_earnings(self, earnings: EarningsData) -> Future:
        """
        **do_finalize_earnings**
            go through each affiliate payment record,
            1. then transfer earnings to wallet,
            2. close earnings record
            3. create a transaction on earnings transaction

        :param earnings:
        :return:
        """
        wallet_instance: WalletModel = WalletModel.query(WalletModel.organization_id == earnings.organization_id,
                                                         WalletModel.uid == earnings.affiliate_id).get_async().get_result()

        if wallet_instance.is_verified and (wallet_instance.available_funds.currency == earnings.total_earned.currency):
            wallet_instance.available_funds.amount_cents += earnings.total_earned.amount_cents
            key: Optional[ndb_Key] = wallet_instance.put_async(retries=self._max_retries,
                                                               timeout=self._max_timeout).get_result()
            if bool(key):
                amount_earned: AmountMixin = earnings.total_earned
                earnings.total_earned.amount_cents = 0
                today: date = datetime.now().date()
                earnings.start_date = today
                earnings.last_updated = today
                earnings.is_paid = True
                earnings_key: Optional[ndb_Key] = earnings.put_async(retries=self._max_retries,
                                                                     timeout=self._max_timeout).get_result()
                if bool(earnings_key):
                    transaction_item: AffiliateTransactionItems = AffiliateTransactionItems()
                    transaction_item.amount = amount_earned
                    transaction_item.transaction_id = create_id()
                    transaction_item.uid = earnings.affiliate_id
                    tran_key: Optional[ndb_Key] = transaction_item.put_async(retries=self._max_retries,
                                                                             timeout=self._max_timeout).get_result()

                    yield bool(tran_key)
        yield False

    @tasklet
    def finalize_affiliate_earnings(self) -> List[Future]:
        """
        **finalize_affiliate_payments**
            go through each affiliate payment record,
            1. then transfer earnings to wallet,
            2. close earnings record
            3. create a transaction on earnings transaction
        :return:
        """
        print(f" running finalize_affiliate_earnings")
        earnings_list: List[EarningsData] = EarningsData.query(EarningsData.is_paid == False,
                                                               EarningsData.on_hold == False).fetch_async().get_result()

        return [self.do_finalize_earnings(earning=earning) for earning in earnings_list]

    async def create_affiliate_reports(self):
        pass

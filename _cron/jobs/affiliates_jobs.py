"""
        **affiliate_jobs**

"""
import asyncio
from datetime import datetime, date
from typing import List, Coroutine, Optional

# noinspection PyPackageRequirements
from google.cloud import ndb
# noinspection PyPackageRequirements
from google.cloud.ndb import Key as ndb_Key, tasklet, toplevel, Future, wait_all

from config.use_context import use_context
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

    @use_context
    @toplevel
    def run(self):
        final_earnings = yield self.finalize_affiliate_earnings()
        return final_earnings

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
        wallet_query = WalletModel.query(WalletModel.organization_id == earnings.organization_id,
                                         WalletModel.uid == earnings.affiliate_id)

        wallet_instance: WalletModel = wallet_query.get_async().get_result()

        if wallet_instance.is_verified and (wallet_instance.available_funds.currency == earnings.total_earned.currency):
            wallet_instance.available_funds.amount_cents += earnings.total_earned.amount_cents
            key: Optional[ndb_Key] = wallet_instance.put_async(retries=self._max_retries,
                                                               timeout=self._max_timeout).get_result()
            if isinstance(key, ndb.Key):
                amount_earned: AmountMixin = earnings.total_earned
                earnings.total_earned.amount_cents = 0
                today: date = datetime.now().date()
                earnings.start_date = today
                earnings.last_updated = today
                earnings.is_paid = True
                earnings_key: Optional[ndb_Key] = earnings.put_async(retries=self._max_retries,
                                                                     timeout=self._max_timeout).get_result()
                if isinstance(earnings_key, ndb.Key):
                    transaction_item: AffiliateTransactionItems = AffiliateTransactionItems()
                    transaction_item.amount = amount_earned
                    transaction_item.transaction_id = create_id()
                    transaction_item.uid = earnings.affiliate_id
                    tran_key: Optional[ndb_Key] = transaction_item.put_async(retries=self._max_retries,
                                                                             timeout=self._max_timeout).get_result()

                    yield isinstance(tran_key, ndb.Key)
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

        earnings_future: Future = EarningsData.query(EarningsData.is_paid == False,
                                                     EarningsData.on_hold == False).fetch_async()

        return [self.do_finalize_earnings(earning=earning) for earning in earnings_future.get_result()]

    @tasklet
    def create_affiliate_reports(self) -> List[Future]:
        pass

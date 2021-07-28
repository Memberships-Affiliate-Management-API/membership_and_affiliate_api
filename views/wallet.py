import functools
import typing
from flask import jsonify, current_app
from config.exceptions import DataServiceError
from main import app_cache
from database.mixins import AmountMixin
from database.wallet import WalletModel, WalletValidator
from utils.utils import return_ttl, end_of_month, can_cache
from config.exception_handlers import handle_view_errors
from config.use_context import use_context


class Validator(WalletValidator):

    def __init__(self):
        super(Validator, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @staticmethod
    def is_uid_none(uid: typing.Union[None, str]) -> bool:
        if (uid is None) or (uid == ''):
            return True
        return False

    @staticmethod
    async def is_uid_none_async(uid: typing.Union[None, str]) -> bool:
        if (uid is None) or (uid == ''):
            return True
        return False

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def can_add_wallet(self, uid: typing.Union[None, str] = None) -> bool:
        if not(self.is_uid_none(uid=uid)):
            wallet_exist: typing.Union[bool, None] = self.wallet_exist(uid=uid)
            if isinstance(wallet_exist, bool):
                return not wallet_exist
            raise DataServiceError(status=500, description='Unable to verify wallet data')
        return False

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def can_add_wallet_async(self, uid: typing.Union[None, str] = None) -> bool:
        if not(self.is_uid_none(uid=uid)):
            wallet_exist: typing.Union[bool, None] = await self.wallet_exist_async(uid=uid)
            if isinstance(wallet_exist, bool):
                return not wallet_exist
            raise DataServiceError(status=500, description='Unable to verify wallet data')
        return False

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def can_update_wallet(self, uid: typing.Union[None, str] = None) -> bool:
        if not(self.is_uid_none(uid=uid)):
            wallet_exist: typing.Union[bool, None] = self.wallet_exist(uid=uid)
            if isinstance(wallet_exist, bool):
                return wallet_exist
            raise DataServiceError(status=500, description='Unable to verify wallet data')
        return False

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def can_update_wallet_async(self, uid: typing.Union[None, str] = None) -> bool:
        if not(self.is_uid_none(uid=uid)):
            wallet_exist: typing.Union[bool, None] = await self.wallet_exist_async(uid=uid)
            if isinstance(wallet_exist, bool):
                return wallet_exist
            raise DataServiceError(status=500, description='Unable to verify wallet data')
        return False

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def can_reset_wallet(self, uid: typing.Union[None, str]) -> bool:
        if not(self.is_uid_none(uid=uid)):
            wallet_exist: typing.Union[bool, None] = self.wallet_exist(uid=uid)
            if isinstance(wallet_exist, bool):
                return wallet_exist
            raise DataServiceError(status=500, description='Unable to verify wallet data')
        return False

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def can_reset_wallet_async(self, uid: typing.Union[None, str]) -> bool:
        if not(self.is_uid_none(uid=uid)):
            wallet_exist: typing.Union[bool, None] = await self.wallet_exist_async(uid=uid)
            if isinstance(wallet_exist, bool):
                return wallet_exist
            raise DataServiceError(status=500, description='Unable to verify wallet data')
        return False


# noinspection DuplicatedCode
class WalletView(Validator):
    ***REMOVED***
        view functions for the wallet
        # TODO -  Refactor Wallet View and improve functionality
    ***REMOVED***

    def __init__(self):
        super(WalletView, self).__init__()

    @use_context
    @handle_view_errors
    def create_wallet(self, uid: typing.Union[str, None], currency: typing.Union[str, None],
                      paypal_address: typing.Union[str, None]) -> tuple:
        # TODO - refactor the create wallet to include organization_id and also
        #   to include is_organization account in-case the wallet belongs to an organization
        if self.can_add_wallet(uid=uid) is True:
            wallet_instance: WalletModel = WalletModel()
            amount_instance: AmountMixin = AmountMixin()
            amount_instance.amount = 0
            amount_instance.currency = currency
            wallet_instance.uid = uid
            wallet_instance.available_funds = amount_instance
            wallet_instance.paypal_address = paypal_address
            key = wallet_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                raise DataServiceError(status=500, description="An Error occurred creating Wallet")
            return jsonify({'status': True, 'message': 'successfully created wallet',
                            'payload': wallet_instance.to_dict()}), 200
        return jsonify({'status': False, 'message': 'Unable to create wallet'}), 500

    @use_context
    @handle_view_errors
    async def create_wallet_async(self, uid: typing.Union[str, None], currency: typing.Union[str, None],
                                  paypal_address: typing.Union[str, None]) -> tuple:
        if await self.can_add_wallet_async(uid=uid) is True:
            wallet_instance: WalletModel = WalletModel()
            amount_instance: AmountMixin = AmountMixin()
            amount_instance.amount = 0
            amount_instance.currency = currency
            wallet_instance.uid = uid
            wallet_instance.available_funds = amount_instance
            wallet_instance.paypal_address = paypal_address
            key = wallet_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
            if key is None:
                raise DataServiceError(status=500, description="An Error occurred creating Wallet")
            return jsonify({'status': True, 'message': 'successfully created wallet',
                            'payload': wallet_instance.to_dict()}), 200
        return jsonify({'status': False, 'message': 'Unable to create wallet'}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_wallet(self, uid: typing.Union[str, None]) -> tuple:
        if not(self.is_uid_none(uid=uid)):
            wallet_instance: WalletModel = WalletModel.query(WalletModel.uid == uid).get()
            return jsonify({'status': True, 'payload': wallet_instance.to_dict(), 'message': 'wallet found'}), 200
        return jsonify({'status': False, 'message': 'uid cannot be None'}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def get_wallet_async(self, uid: typing.Union[str, None]) -> tuple:
        if not(self.is_uid_none(uid=uid)):
            wallet_instance: WalletModel = WalletModel.query(WalletModel.uid == uid).get_async().get_result()
            return jsonify({'status': True, 'payload': wallet_instance.to_dict(), 'message': 'wallet found'}), 200
        return jsonify({'status': False, 'message': 'uid cannot be None'}), 500

    @use_context
    @handle_view_errors
    def update_wallet(self, wallet_data: dict) -> tuple:

        uid: typing.Union[str, None] = wallet_data.get("uid")
        available_funds: typing.Union[int, None] = wallet_data.get("available_funds")
        currency: typing.Union[str, None] = wallet_data.get('currency')
        paypal_address: typing.Union[str, None] = wallet_data.get("paypal_address")

        if self.can_update_wallet(uid=uid) is True:
            wall_instance: WalletModel = WalletModel.query(WalletModel.uid == uid).get()
            # No need to test for wallet availability as can update returned True
            wall_instance.uid = uid
            amount_instance: AmountMixin = AmountMixin(amount=available_funds, currency=currency)
            wall_instance.available_funds = amount_instance
            wall_instance.paypal_address = paypal_address
            key = wall_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = "An Error occurred updating Wallet"
                raise DataServiceError(status=500, description=message)
            return jsonify({'status': True, 'payload': wall_instance.to_dict(),
                            'message': 'successfully updated wallet'}), 200
        return jsonify({'status': False, 'message': 'Unable to update wallet'}), 500

    @use_context
    @handle_view_errors
    async def update_wallet_async(self, wallet_data: dict) -> tuple:

        uid: typing.Union[str, None] = wallet_data.get("uid")
        available_funds: typing.Union[int, None] = wallet_data.get("available_funds")
        currency: typing.Union[str, None] = wallet_data.get('currency')
        paypal_address: typing.Union[str, None] = wallet_data.get("paypal_address")

        if await self.can_update_wallet_async(uid=uid) is True:
            wall_instance: WalletModel = WalletModel.query(WalletModel.uid == uid).get_async().get_result()
            # No need to test for wallet availability as can update returned True
            wall_instance.uid = uid
            amount_instance: AmountMixin = AmountMixin(amount=available_funds, currency=currency)
            wall_instance.available_funds = amount_instance
            wall_instance.paypal_address = paypal_address
            key = wall_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
            if key is None:
                message: str = "Database error while updating wallet"
                raise DataServiceError(status=500, description=message)
            return jsonify({'status': True, 'payload': wall_instance.to_dict(),
                            'message': 'successfully updated wallet'}), 200
        return jsonify({'status': False, 'message': 'Unable to update wallet'}), 500

    @use_context
    @handle_view_errors
    def reset_wallet(self, wallet_data: dict) -> tuple:
        uid: typing.Union[str, None] = wallet_data.get('uid')
        currency: typing.Union[str, None] = wallet_data.get('currency')
        if self.can_reset_wallet(uid=uid) is True:
            wallet_instance: WalletModel = WalletModel.query(WalletModel.uid == uid).get()
            amount_instance: AmountMixin = AmountMixin(amount=0, currency=currency)
            wallet_instance.available_funds = amount_instance
            key = wallet_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = "Database error while updating wallet"
                raise DataServiceError(status=500, description=message)

            return jsonify({'status': True, 'payload': wallet_instance.to_dict(),
                            'message': 'wallet is rest'}), 200
        return jsonify({'status': False, 'message': 'Unable to reset wallet'}), 500

    @use_context
    @handle_view_errors
    async def reset_wallet_async(self, wallet_data: dict) -> tuple:
        uid: typing.Union[str, None] = wallet_data.get('uid')
        currency: typing.Union[str, None] = wallet_data.get('currency')
        if await self.can_reset_wallet_async(uid=uid) is True:
            wallet_instance: WalletModel = WalletModel.query(WalletModel.uid == uid).get_async().get_result()
            amount_instance: AmountMixin = AmountMixin(amount=0, currency=currency)
            wallet_instance.available_funds = amount_instance
            key = wallet_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
            if key is None:
                message: str = "Database error while resetting wallet"
                raise DataServiceError(status=500, description=message)
            return jsonify({'status': True, 'payload': wallet_instance.to_dict(),
                            'message': 'wallet is rest'}), 200
        return jsonify({'status': False, 'message': 'Unable to reset wallet'}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def return_all_wallets(self) -> tuple:
        wallet_list: typing.List[WalletModel] = WalletModel.query().fetch()
        payload: typing.List[dict] = [wallet.to_dict() for wallet in wallet_list]
        return jsonify({'status': True,
                        'payload': payload,
                        'message': 'wallets returned'}), 200

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def return_all_wallets_async(self) -> tuple:
        wallet_list: typing.List[WalletModel] = WalletModel.query().fetch_async().get_result()
        payload: typing.List[dict] = [wallet.to_dict() for wallet in wallet_list]
        return jsonify({'status': True,
                        'payload': payload,
                        'message': 'wallets returned'}), 200

    @use_context
    @handle_view_errors
    def return_wallets_by_balance(self, lower_bound: int, higher_bound: int) -> tuple:
        # if either lower_bound and higher_bound are not int then exit
        if not(isinstance(lower_bound, int) or isinstance(higher_bound, int)):
            return jsonify({'status': False, 'message': "specify lower bound and higher bound"}), 500
        wallet_list: typing.List[WalletModel] = WalletModel.query(WalletModel.available_funds > lower_bound,
                                                                  WalletModel.available_funds < higher_bound).fetch()
        payload: typing.List[dict] = [wallet.to_dict() for wallet in wallet_list]
        return jsonify({'status': True, 'payload': payload, 'message': 'wallets returned'}), 200

    @use_context
    @handle_view_errors
    async def return_wallets_by_balance_async(self, lower_bound: int, higher_bound: int) -> tuple:
        # if either lower_bound and higher_bound are not int then exit
        if not(isinstance(lower_bound, int) or isinstance(higher_bound, int)):
            return jsonify({'status': False, 'message': "specify lower bound and higher bound"}), 500
        wallet_list: typing.List[WalletModel] = WalletModel.query(WalletModel.available_funds > lower_bound,
                                                                  WalletModel.available_funds < higher_bound).fetch_async().get_result()
        payload: typing.List[dict] = [wallet.to_dict() for wallet in wallet_list]
        return jsonify({'status': True, 'payload': payload, 'message': 'wallets returned'}), 200

    @use_context
    @handle_view_errors
    def wallet_transact(self, uid: str, add: int = None, sub: int = None) -> tuple:
        if self.can_update_wallet(uid=uid) is True:
            wallet_instance: WalletModel = WalletModel.query(WalletModel.uid == uid).get()
            if isinstance(wallet_instance, WalletModel):
                if add is not None:
                    wallet_instance.available_funds.amount += add
                if sub is not None:
                    wallet_instance.available_funds.amount -= sub
                key = wallet_instance.put()
                if key is None:
                    message: str = "General error updating database"
                    raise DataServiceError(status=500, description=message)
                message: str = "Successfully created transaction"
                return jsonify({'status': True, 'payload': wallet_instance.to_dict(),
                                'message': message}), 200
        message: str = "Unable to find wallet"
        return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    async def wallet_transact_async(self, uid: str, add: int = None, sub: int = None) -> tuple:
        if await self.can_update_wallet_async(uid=uid) is True:
            wallet_instance: WalletModel = WalletModel.query(WalletModel.uid == uid).get_async().get_result()
            if isinstance(wallet_instance, WalletModel):
                if isinstance(add, int):
                    wallet_instance.available_funds.amount += add
                if isinstance(sub, int):
                    wallet_instance.available_funds.amount -= sub
                key = wallet_instance.put_async().get_result()
                if key is None:
                    message: str = "General error updating database"
                    raise DataServiceError(status=500, description=message)
                message: str = "Successfully created transaction"
                return jsonify({'status': True, 'payload': wallet_instance.to_dict(),
                                'message': message}), 200
        message: str = "Unable to find wallet"
        return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    def wallet_withdraw_funds(self, uid: str, amount: int) -> tuple:
        ***REMOVED***
            organization must contain settings for funds withdrawals
            i.e from which paypal account may the withdrawal occur
            and so on.

            steps create a withdrawal transaction,
            with the requested amount,
            await admin approvals,
            cron job must run and process all approved withdrawals
            cron job must retain all the results of the transactions and save on the database
        :param uid:
        :param amount:
        :return:
        ***REMOVED***
        pass

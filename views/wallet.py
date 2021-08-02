import typing
from flask import jsonify, current_app
from config.exceptions import DataServiceError, UnAuthenticatedError, status_codes, error_codes, InputError
from main import app_cache
from database.mixins import AmountMixin
from database.wallet import WalletModel, WalletValidator
from utils.utils import return_ttl, can_cache
from config.exception_handlers import handle_view_errors
from config.use_context import use_context


class Validator(WalletValidator):
    ***REMOVED***
        Wallet Validators
        TODO- improve the validators to validate all aspects of wallet transactions
    ***REMOVED***

    def __init__(self):
        super(Validator, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @staticmethod
    def is_uid_none(uid: typing.Union[str, None]) -> bool:
        ***REMOVED***
            :param uid:
            :return:
        ***REMOVED***
        if not isinstance(uid, str) or not bool(uid.strip()):
            return True
        return False

    @staticmethod
    async def is_uid_none_async(uid: typing.Union[None, str]) -> bool:
        if not isinstance(uid, str) or not bool(uid.strip()):
            return True
        return False

    @staticmethod
    def raise_input_error_if_not_available(organization_id: str, uid: str) -> None:
        ***REMOVED***
            raise an error if organization_id or uid is not present
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def can_add_wallet(self, organization_id: typing.Union[str, None], uid: typing.Union[None, str] = None) -> bool:
        ***REMOVED***
                can add wallet
            :param organization_id:
            :param uid:
            :return:
        ***REMOVED***
        # NOTE this will raise input error if either or this
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_exist: typing.Union[bool, None] = self.wallet_exist(organization_id=organization_id, uid=uid)
        if isinstance(wallet_exist, bool):
            return not wallet_exist
        raise DataServiceError(status=error_codes.data_service_error_code, description='Unable to verify wallet data')

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def can_add_wallet_async(self, organization_id: typing.Union[str, None],
                                   uid: typing.Union[None, str] = None) -> bool:
        ***REMOVED***
            testing if user can add a wallet
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***

        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_exist: typing.Union[bool, None] = await self.wallet_exist_async(organization_id=organization_id, uid=uid)

        if isinstance(wallet_exist, bool):
            return not wallet_exist
        raise DataServiceError(status=error_codes.data_service_error_code, description='Unable to verify wallet data')

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def can_update_wallet(self, organization_id: typing.Union[str, None], uid: typing.Union[None, str] = None) -> bool:
        ***REMOVED***
            checks if user can update wallet
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_exist: typing.Union[bool, None] = self.wallet_exist(organization_id=organization_id, uid=uid)
        if isinstance(wallet_exist, bool):
            return wallet_exist
        raise DataServiceError(status=500, description='Unable to verify wallet data')

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def can_update_wallet_async(self, organization_id: typing.Union[str, None],
                                      uid: typing.Union[None, str] = None) -> bool:
        ***REMOVED***
            asynchronous version of can_update_wallet
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_exist: typing.Union[bool, None] = await self.wallet_exist_async(organization_id=organization_id, uid=uid)
        if isinstance(wallet_exist, bool):
            return wallet_exist
        raise DataServiceError(status=error_codes.data_service_error_code, description='Unable to verify wallet data')

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def can_reset_wallet(self, organization_id: typing.Union[str, None], uid: typing.Union[None, str]) -> bool:
        ***REMOVED***
            checks if user can reset wallet
        :param organization_id: required
        :param uid: required
        :return:
        ***REMOVED***
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_exist: typing.Union[bool, None] = self.wallet_exist(organization_id=organization_id, uid=uid)
        if isinstance(wallet_exist, bool):
            return wallet_exist
        raise DataServiceError(status=error_codes.data_service_error_code, description='Unable to verify wallet data')

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def can_reset_wallet_async(self, organization_id: typing.Union[str, None],
                                     uid: typing.Union[None, str]) -> bool:
        ***REMOVED***
            asynchronous version of can_reset_wallet
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_exist: typing.Union[bool, None] = await self.wallet_exist_async(organization_id=organization_id, uid=uid)

        if isinstance(wallet_exist, bool):
            return wallet_exist
        raise DataServiceError(status=error_codes.data_service_error_code, description='Unable to verify wallet data')


# noinspection DuplicatedCode
class WalletView(Validator):
    ***REMOVED***
        view functions for the wallet
    ***REMOVED***

    def __init__(self):
        super(WalletView, self).__init__()

    @use_context
    @handle_view_errors
    def create_wallet(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None],
                      currency: typing.Union[str, None], paypal_address: typing.Union[str, None],
                      is_org_wallet: bool = False) -> tuple:
        ***REMOVED***
                enables the system/user to create new wallet for a user
        :param organization_id:
        :param uid:
        :param currency:
        :param paypal_address:
        :param is_org_wallet:
        :return:
        ***REMOVED***
        # NOTE: no need to check if organization_id and uid are available
        if not self.can_add_wallet(organization_id=organization_id, uid=uid):
            message: str = "You are not authorized to create a new Wallet"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        # Creating new Wallet
        wallet_instance: WalletModel = WalletModel()
        amount_instance: AmountMixin = AmountMixin()
        amount_instance.amount = 0
        amount_instance.currency = currency
        wallet_instance.uid = uid
        wallet_instance.available_funds = amount_instance
        wallet_instance.paypal_address = paypal_address
        wallet_instance.organization_id = organization_id
        wallet_instance.is_org_wallet = is_org_wallet
        key = wallet_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not bool(key):
            raise DataServiceError(status=500, description="An Error occurred creating Wallet")

        return jsonify({'status': True, 'message': 'successfully created wallet',
                        'payload': wallet_instance.to_dict()}), status_codes.status_ok_code

    @use_context
    @handle_view_errors
    async def create_wallet_async(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None], currency: typing.Union[str, None],
                                  paypal_address: typing.Union[str, None], is_org_wallet: bool = False) -> tuple:
        ***REMOVED***
            asynchronous version of create_wallet
        :param organization_id:
        :param uid:
        :param currency:
        :param paypal_address:
        :param is_org_wallet:
        :return:
        ***REMOVED***

        # NOTE: no need to check if organization_id and uid are available
        if not await self.can_add_wallet_async(organization_id=organization_id, uid=uid):
            message: str = "You are not authorized to create a new Wallet"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        wallet_instance: WalletModel = WalletModel()
        amount_instance: AmountMixin = AmountMixin()
        amount_instance.amount = 0
        amount_instance.currency = currency
        wallet_instance.uid = uid
        wallet_instance.available_funds = amount_instance
        wallet_instance.paypal_address = paypal_address
        wallet_instance.organization_id = organization_id
        wallet_instance.is_org_wallet = is_org_wallet

        key = wallet_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
        if not bool(key):
            raise DataServiceError(status=error_codes.data_service_error_code,
                                   description="An Error occurred creating Wallet")

        return jsonify({'status': True, 'message': 'successfully created wallet',
                        'payload': wallet_instance.to_dict()}), status_codes.status_ok_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_wallet(self, organization_id: typing.Union[str, None], uid: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            # TODO - may need to update cache or find a way to update cache when there are updates
            # this could mean that the old method of having a separate cache for every module may be useful here

            returns a specific wallet from database
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                         WalletModel.uid == uid).get()

        return jsonify({'status': True, 'payload': wallet_instance.to_dict(),
                        'message': 'wallet found'}), status_codes.status_ok_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def get_wallet_async(self, organization_id: typing.Union[str, None],  uid: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            get_wallet_async an asynchronous version of get_wallet
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                         WalletModel.uid == uid).get_async().get_result()

        return jsonify({'status': True, 'payload': wallet_instance.to_dict(),
                        'message': 'wallet found'}), 200

    @use_context
    @handle_view_errors
    def update_wallet(self, wallet_data: dict) -> tuple:
        ***REMOVED***
            lets user or system update wallet
        :param wallet_data:
        :return:
        ***REMOVED***

        uid: typing.Union[str, None] = wallet_data.get("uid")
        organization_id: typing.Union[str, None] = wallet_data.get('organization_id')
        # NOTE checking if organization_id or uid is present
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        available_funds: typing.Union[int, None] = int(wallet_data.get("available_funds", 0))

        if not isinstance(available_funds, int):
            message: str = "available_funds is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        currency: typing.Union[str, None] = wallet_data.get('currency')
        if not isinstance(currency, str) or not bool(currency.strip()):
            message: str = "currency symbol is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        paypal_address: typing.Union[str, None] = wallet_data.get("paypal_address")
        if not isinstance(paypal_address, str) or not bool(paypal_address.strip()):
            message: str = "paypal_address is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        # TODO update can update wallet to take into account Org Account Roles
        if not self.can_update_wallet(organization_id=organization_id, uid=uid):
            message: str = "You are not authorized to update this Wallet"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        wall_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                       WalletModel.uid == uid).get()

        # No need to test for wallet availability as can update returned True
        amount_instance: AmountMixin = AmountMixin(amount=available_funds, currency=currency)
        wall_instance.available_funds = amount_instance
        wall_instance.paypal_address = paypal_address
        key = wall_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not bool(key):
            message: str = "An Error occurred updating Wallet"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        return jsonify({'status': True, 'payload': wall_instance.to_dict(),
                        'message': 'successfully updated wallet'}), status_codes.status_ok_code

    @use_context
    @handle_view_errors
    async def update_wallet_async(self, wallet_data: dict) -> tuple:

        uid: typing.Union[str, None] = wallet_data.get("uid")
        organization_id: typing.Union[str, None] = wallet_data.get('organization_id')
        available_funds: typing.Union[int, None] = wallet_data.get("available_funds")
        currency: typing.Union[str, None] = wallet_data.get('currency')
        paypal_address: typing.Union[str, None] = wallet_data.get("paypal_address")

        if await self.can_update_wallet_async(organization_id=organization_id, uid=uid) is True:
            wall_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                           WalletModel.uid == uid).get_async().get_result()

            # No need to test for wallet availability as can update returned True

            amount_instance: AmountMixin = AmountMixin(amount=available_funds, currency=currency)
            wall_instance.available_funds = amount_instance
            wall_instance.paypal_address = paypal_address
            key = wall_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
            if not bool(key):
                message: str = "Database error while updating wallet"
                raise DataServiceError(status=500, description=message)
            return jsonify({'status': True, 'payload': wall_instance.to_dict(),
                            'message': 'successfully updated wallet'}), 200
        return jsonify({'status': False, 'message': 'Unable to update wallet'}), 500

    @use_context
    @handle_view_errors
    def reset_wallet(self, wallet_data: dict) -> tuple:
        uid: typing.Union[str, None] = wallet_data.get('uid')
        organization_id: typing.Union[str, None] = wallet_data.get('organization_id')
        currency: typing.Union[str, None] = wallet_data.get('currency')
        if self.can_reset_wallet(organization_id=organization_id, uid=uid) is True:
            wallet_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                             WalletModel.uid == uid).get()

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
        organization_id: typing.Union[str, None] = wallet_data.get('organization_id')
        currency: typing.Union[str, None] = wallet_data.get('currency')
        if await self.can_reset_wallet_async(organization_id=organization_id, uid=uid) is True:
            wallet_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                             WalletModel.uid == uid).get_async().get_result()

            amount_instance: AmountMixin = AmountMixin(amount=0, currency=currency)
            wallet_instance.available_funds = amount_instance
            key = wallet_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
            if not bool(key):
                message: str = "Database error while resetting wallet"
                raise DataServiceError(status=500, description=message)
            return jsonify({'status': True, 'payload': wallet_instance.to_dict(),
                            'message': 'wallet is rest'}), 200
        return jsonify({'status': False, 'message': 'Unable to reset wallet'}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def return_all_wallets(self, organization_id: typing.Union[str, None]) -> tuple:
        wallet_list: typing.List[WalletModel] = WalletModel.query(WalletModel.organization_id == organization_id).fetch()
        payload: typing.List[dict] = [wallet.to_dict() for wallet in wallet_list]
        return jsonify({'status': True,
                        'payload': payload,
                        'message': 'wallets returned'}), 200

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    async def return_all_wallets_async(self, organization_id: typing.Union[str, None]) -> tuple:

        wallet_list: typing.List[WalletModel] = WalletModel.query(
            WalletModel.organization_id == organization_id).fetch_async().get_result()

        payload: typing.List[dict] = [wallet.to_dict() for wallet in wallet_list]
        return jsonify({'status': True,
                        'payload': payload,
                        'message': 'wallets returned'}), 200

    @use_context
    @handle_view_errors
    def return_wallets_by_balance(self, organization_id: typing.Union[str, None],
                                  lower_bound: int, higher_bound: int) -> tuple:

        # if either lower_bound and higher_bound are not int then exit
        if not(isinstance(lower_bound, int) or isinstance(higher_bound, int)):
            return jsonify({'status': False, 'message': "specify lower bound and higher bound"}), 500
        wallet_list: typing.List[WalletModel] = WalletModel.query(WalletModel.organization_id == organization_id,
                                                                  WalletModel.available_funds > lower_bound,
                                                                  WalletModel.available_funds < higher_bound).fetch()

        payload: typing.List[dict] = [wallet.to_dict() for wallet in wallet_list]
        return jsonify({'status': True, 'payload': payload, 'message': 'wallets returned'}), 200

    @use_context
    @handle_view_errors
    async def return_wallets_by_balance_async(self, organization_id: typing.Union[str, None],
                                              lower_bound: int, higher_bound: int) -> tuple:

        # if either lower_bound and higher_bound are not int then exit
        if not(isinstance(lower_bound, int) or isinstance(higher_bound, int)):
            return jsonify({'status': False, 'message': "specify lower bound and higher bound"}), 500
        wallet_list: typing.List[WalletModel] = WalletModel.query(
            WalletModel.organization_id == organization_id, WalletModel.available_funds > lower_bound,
            WalletModel.available_funds < higher_bound).fetch_async().get_result()

        payload: typing.List[dict] = [wallet.to_dict() for wallet in wallet_list]
        return jsonify({'status': True, 'payload': payload, 'message': 'wallets returned'}), 200

    @use_context
    @handle_view_errors
    def wallet_transact(self, organization_id: typing.Union[str, None], uid: str,
                        add: int = None, sub: int = None) -> tuple:

        if self.can_update_wallet(organization_id=organization_id, uid=uid) is True:
            wallet_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                             WalletModel.uid == uid).get()

            if isinstance(wallet_instance, WalletModel):
                if isinstance(sub, int):
                    wallet_instance.available_funds.amount -= sub
                if isinstance(add, int):
                    wallet_instance.available_funds.amount += sub
                key = wallet_instance.put()
                if not bool(key):
                    message: str = "General error updating database"
                    raise DataServiceError(status=500, description=message)
                message: str = "Successfully created transaction"
                return jsonify({'status': True, 'payload': wallet_instance.to_dict(),
                                'message': message}), 200
        message: str = "Unable to find wallet"
        return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    async def wallet_transact_async(self, organization_id: typing.Union[str, None], uid: str,
                                    add: int = None, sub: int = None) -> tuple:

        if await self.can_update_wallet_async(organization_id=organization_id, uid=uid) is True:
            wallet_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                             WalletModel.uid == uid).get_async().get_result()

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
    def wallet_withdraw_funds(self, organization_id: typing.Union[str, None], uid: str, amount: int) -> tuple:
        ***REMOVED***
            organization must contain settings for funds withdrawals
            i.e from which paypal account may the withdrawal occur
            and so on.

            steps create a withdrawal transaction,
            with the requested amount,
            await admin approvals,
            cron job must run and process all approved withdrawals
            cron job must retain all the results of the transactions and save on the database
        :param organization_id:
        :param uid:
        :param amount:
        :return:
        ***REMOVED***
        pass

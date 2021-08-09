***REMOVED***
    **Module Wallet View Controller**
    **Class Definitions for handling Wallet data input and validations **
***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import typing
from flask import jsonify, current_app
from _sdk._email import Mailgun
from database.mixins import AmountMixin
from database.wallet import WalletModel, WalletValidator
from utils import return_ttl
from config.exceptions import DataServiceError, UnAuthenticatedError, status_codes, error_codes, InputError
from config.exception_handlers import handle_view_errors
from config.use_context import use_context
from main import app_cache


class WalletEmails(Mailgun):
    ***REMOVED***
        Class used to send Wallet related Emails and Notifications
    ***REMOVED***
    def __init__(self):
        super(WalletEmails, self).__init__()

    def __do_send_mail(self, to_email: str, subject: str, text: str, html: str) -> None:
        ***REMOVED***
            **__do_send_mail
                  **If possible this method should be run asynchronously**
                  a method to actually send email

        :param to_email: email address to send the email to
        :param subject: subject of the email
        :param text: body in text format
        :param html: body in html format
        :return: does not return anything
        ***REMOVED***
        self.__send_with_mailgun_rest_api(to_list=[to_email], subject=subject, text=text, html=html)

    def send_balance_changed_notification(self, organization_id: str, uid: str) -> None:
        ***REMOVED***
            **send_balance_changed_notification**
                send an email to client or organization informing them that balance has changed on their wallet

        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        # TODO finish send_balance_changed_notification
        pass

    def wallet_created_successfully(self, organization_id: str, uid: str) -> None:
        ***REMOVED***
            **wallet_created_successfully**
                send an email informing user that their wallet has been created and its details

        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        # TODO wallet_created_successfully
        pass

    def wallet_details_changed(self, organization_id: str, uid: str) -> None:
        ***REMOVED***
            **wallet_details_changed**
                send an email informing the user that wallet details has changed

        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        # TODO wallet_details_changed
        pass


class Validator(WalletValidator):
    ***REMOVED***
        **Class Wallet Validators**
            validates wallet transactions
        TODO- improve the validators to validate all aspects of wallet transactions
    ***REMOVED***

    def __init__(self):
        super(Validator, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @staticmethod
    def raise_input_error_if_not_available(organization_id: str, uid: str) -> None:
        ***REMOVED***
            **raise_input_error_if_not_available
                raise an error if organization_id or uid is not present

        :param organization_id:
        :param uid:
        :return: Nothing
        ***REMOVED***

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

    @staticmethod
    def raise_input_error(**kwargs) -> None:
        ***REMOVED***
            **raise_input_error**
                general function to raise input errors in-case when string variables are not string or are Empty
                raise an input error if any of the input variables are Null or Empty

        :param kwargs:
        :return:
        ***REMOVED***
        for arg in kwargs.items():
            if not isinstance(arg, str) or not bool(arg.strip()):
                message: str = "{} is required".format(arg.__class__.__name__)
                raise InputError(status=error_codes.input_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'))
    def can_add_wallet(self, organization_id: typing.Union[str, None], uid: typing.Union[None, str] = None) -> bool:
        ***REMOVED***
            **can_add_wallet**
                this method will check if a new wallet can be added

            :param organization_id:
            :param uid:
            :return:
        ***REMOVED***
        # NOTE this will raise input error if either or this
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_exist: typing.Union[bool, None] = self.wallet_exist(organization_id=organization_id, uid=uid)
        if isinstance(wallet_exist, bool):
            return not wallet_exist

        # result is None meaning an error occurred then Raise a DataServiceError
        message: str = 'database Error: Unable to verify wallet data'
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'))
    async def can_add_wallet_async(self, organization_id: typing.Union[str, None],
                                   uid: typing.Union[None, str] = None) -> bool:
        ***REMOVED***
            **can_add_wallet_async**
                An asynchronous version of can_add_wallet
                testing if user can add a wallet

        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***

        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_exist: typing.Union[bool, None] = await self.wallet_exist_async(organization_id=organization_id, uid=uid)

        if isinstance(wallet_exist, bool):
            return not wallet_exist

        message: str = 'database Error: Unable to verify wallet data'
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'))
    def can_update_wallet(self, organization_id: typing.Union[str, None], uid: typing.Union[None, str] = None) -> bool:
        ***REMOVED***
            **can_add_wallet**
                checks if user can update wallet - a wallet need to already exists for it to be updated
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_exist: typing.Union[bool, None] = self.wallet_exist(organization_id=organization_id, uid=uid)
        if isinstance(wallet_exist, bool):
            return wallet_exist
        message: str = 'database error: Unable to verify wallet data'
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'))
    async def can_update_wallet_async(self, organization_id: typing.Union[str, None],
                                      uid: typing.Union[None, str] = None) -> bool:
        ***REMOVED***
            **can_update_wallet_async**
                asynchronous version of can_update_wallet

        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_exist: typing.Union[bool, None] = await self.wallet_exist_async(organization_id=organization_id, uid=uid)
        if isinstance(wallet_exist, bool):
            return wallet_exist
        message: str = "database error: Unable to verify wallet data"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'))
    def can_reset_wallet(self, organization_id: typing.Union[str, None], uid: typing.Union[None, str]) -> bool:
        ***REMOVED***
            **can_reset_wallet**
                checks if user can reset wallet
        :param organization_id: required
        :param uid: required
        :return:
        ***REMOVED***
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_exist: typing.Union[bool, None] = self.wallet_exist(organization_id=organization_id, uid=uid)
        if isinstance(wallet_exist, bool):
            return wallet_exist

        message: str = 'database Error: Unable to verify wallet data'
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.memoize(timeout=return_ttl('short'))
    async def can_reset_wallet_async(self, organization_id: typing.Union[str, None],
                                     uid: typing.Union[None, str]) -> bool:
        ***REMOVED***
            **can_reset_wallet_async**
                asynchronous version of can_reset_wallet
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_exist: typing.Union[bool, None] = await self.wallet_exist_async(organization_id=organization_id, uid=uid)

        if isinstance(wallet_exist, bool):
            return wallet_exist
        message: str = 'database Error: Unable to verify wallet data'
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)


# noinspection DuplicatedCode
class WalletView(Validator, WalletEmails):
    ***REMOVED***
        **Class WalletView**
            view functions for the wallet

        **Class Methods**
            1. create_wallet -> enables the creation of new wallets only
            2. update_wallet -> enables the update of existing wallets
            3. get_wallet -> fetches a specific wallet depending on method parameters
            4. reset_wallet -> resets wallet to default values except uid and organization_id
            5. return_all_wallets -> returns all wallets specific to an organization_id
            6. return_wallets_by_balance -> returns specific wallets in an organization by their balance ranges
            7. wallet_transact -> create a wallet transaction
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
        :return: tuple with created wallet_instance
        ***REMOVED***
        # NOTE: no need to check if organization_id and uid are available
        if not self.can_add_wallet(organization_id=organization_id, uid=uid):
            message: str = "You are not authorized to create a new Wallet"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        # creating new Wallet for a new user
        amount_instance: AmountMixin = AmountMixin(amount=0, currency=currency)

        wallet_instance: WalletModel = WalletModel(organization_id=organization_id, uid=uid,
                                                   is_org_wallet=is_org_wallet, available_funds=amount_instance,
                                                   paypal_address=paypal_address)

        key = wallet_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not bool(key):
            message: str = "Database Error: Wallet may not have been created"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        # Sending an email notification to the user informing them that the wallet has been created successfully
        self.wallet_created_successfully(organization_id=organization_id, uid=uid)

        return jsonify({'status': True, 'message': 'successfully created wallet',
                        'payload': wallet_instance.to_dict()}), status_codes.successfully_updated_code

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
            message: str = "Operation Denied: cannot create a new Wallet"
            raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

        amount_instance: AmountMixin = AmountMixin(amount=0, currency=currency)

        wallet_instance: WalletModel = WalletModel(organization_id=organization_id, uid=uid,
                                                   is_org_wallet=is_org_wallet, available_funds=amount_instance,
                                                   paypal_address=paypal_address)

        key = wallet_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
        if not bool(key):
            raise DataServiceError(status=error_codes.data_service_error_code,
                                   description="An Error occurred creating Wallet")

        # Sending an email notification to the user informing them that the wallet has been created successfully
        self.wallet_created_successfully(organization_id=organization_id, uid=uid)

        return jsonify({'status': True, 'message': 'successfully created wallet',
                        'payload': wallet_instance.to_dict()}), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
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
        if isinstance(wallet_instance, WalletModel):
            return jsonify({'status': True, 'payload': wallet_instance.to_dict(),
                            'message': 'wallet found'}), status_codes.status_ok_code

        message: str = "Wallet not found"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
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
        if isinstance(wallet_instance, WalletModel):
            return jsonify({'status': True, 'payload': wallet_instance.to_dict(),
                            'message': 'wallet found'}), status_codes.status_ok_code

        message: str = "Wallet not found"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

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

        # TODO - consider using Sentinel as an indicator of something went wrong
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
            message: str = "Database Error: occurred updating Wallet"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        return jsonify({'status': True, 'payload': wall_instance.to_dict(),
                        'message': 'successfully updated wallet'}), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    async def update_wallet_async(self, wallet_data: dict) -> tuple:
        ***REMOVED***
            can update wallet asynchronous version of
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
        if not self.can_update_wallet_async(organization_id=organization_id, uid=uid):
            message: str = "You are not authorized to update this Wallet"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        wall_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                       WalletModel.uid == uid).get_async().get_result()

        # No need to test for wallet availability as can update returned True

        amount_instance: AmountMixin = AmountMixin(amount=available_funds, currency=currency)
        wall_instance.available_funds = amount_instance
        wall_instance.paypal_address = paypal_address
        key = wall_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
        if not bool(key):
            message: str = "Database Error: while updating wallet"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        return jsonify({'status': True, 'payload': wall_instance.to_dict(),
                        'message': 'successfully updated wallet'}), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def reset_wallet(self, wallet_data: dict) -> tuple:
        ***REMOVED***

        :param wallet_data:
        :return:
        ***REMOVED***
        uid: typing.Union[str, None] = wallet_data.get('uid')
        organization_id: typing.Union[str, None] = wallet_data.get('organization_id')
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        currency: typing.Union[str, None] = wallet_data.get('currency')
        if not isinstance(currency, str) or not bool(currency.strip()):
            message: str = "currency is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if self.can_reset_wallet(organization_id=organization_id, uid=uid) is True:
            message: str = "You are not authorized to reset this wallet"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        wallet_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                         WalletModel.uid == uid).get()

        amount_instance: AmountMixin = AmountMixin(amount=0, currency=currency)
        wallet_instance.available_funds = amount_instance
        key = wallet_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not bool(key):
            message: str = "Database Error: while updating wallet"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        return jsonify({'status': True, 'payload': wallet_instance.to_dict(),
                        'message': 'wallet is rest'}), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    async def reset_wallet_async(self, wallet_data: dict) -> tuple:
        ***REMOVED***
            asynchronous version of reset wallet
        :param wallet_data:
        :return:
        ***REMOVED***

        uid: typing.Union[str, None] = wallet_data.get('uid')
        organization_id: typing.Union[str, None] = wallet_data.get('organization_id')
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        currency: typing.Union[str, None] = wallet_data.get('currency')
        if not isinstance(currency, str) or not bool(currency.strip()):
            message: str = "currency is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not await self.can_reset_wallet_async(organization_id=organization_id, uid=uid):
            message: str = "You are not authorized to reset this wallet"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        wallet_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                         WalletModel.uid == uid).get_async().get_result()

        amount_instance: AmountMixin = AmountMixin(amount=0, currency=currency)
        wallet_instance.available_funds = amount_instance
        key = wallet_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
        if not bool(key):
            message: str = "Database error while resetting wallet"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        return jsonify({'status': True, 'payload': wallet_instance.to_dict(),
                        'message': 'wallet is rest'}), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    def return_all_wallets(self, organization_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
        given an organization_id return all the organizations wallets
        :param organization_id:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        wallet_list: typing.List[WalletModel] = WalletModel.query(WalletModel.organization_id == organization_id).fetch()
        payload: typing.List[dict] = [wallet.to_dict() for wallet in wallet_list]

        if len(payload):
            return jsonify({'status': True,
                            'payload': payload,
                            'message': 'wallets returned'}), status_codes.status_ok_code
        return jsonify({'status': False, 'message': 'no wallets found'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'))
    async def return_all_wallets_async(self, organization_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            given an organization_id return all the organizations wallets
        :param organization_id:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        wallet_list: typing.List[WalletModel] = WalletModel.query(
            WalletModel.organization_id == organization_id).fetch_async().get_result()

        payload: typing.List[dict] = [wallet.to_dict() for wallet in wallet_list]

        if len(payload):
            return jsonify({'status': True,
                            'payload': payload,
                            'message': 'wallets returned'}), status_codes.status_ok_code
        return jsonify({'status': False, 'message': 'wallets not found'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def return_wallets_by_balance(self, organization_id: typing.Union[str, None],
                                  lower_bound: int, higher_bound: int) -> tuple:
        ***REMOVED***
            # TODO consider supplying lower_bound and higher_bound as a dict
            return wallets with balances within lower_bound and higher_bound
        :param organization_id:
        :param lower_bound:
        :param higher_bound:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(lower_bound, int) or not isinstance(higher_bound, int):
            message: str = "lower_bound and higher_bound are required"
            raise InputError(status=error_codes.input_error_code, description=message)

        wallet_list: typing.List[WalletModel] = WalletModel.query(WalletModel.organization_id == organization_id,
                                                                  WalletModel.available_funds > lower_bound,
                                                                  WalletModel.available_funds < higher_bound).fetch()

        payload: typing.List[dict] = [wallet.to_dict() for wallet in wallet_list]
        if len(payload):
            return jsonify({'status': True, 'payload': payload,
                            'message': 'wallets returned'}), status_codes.status_ok_code

        message: str = "Wallets not found"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    async def return_wallets_by_balance_async(self, organization_id: typing.Union[str, None],
                                              lower_bound: int, higher_bound: int) -> tuple:
        ***REMOVED***
            # TODO - consider changing the function name to : return_wallets_by_balance_range_async
            asynchronous version of return wallets by balance
        :param organization_id:
        :param lower_bound:
        :param higher_bound:
        :return:
        ***REMOVED***

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(lower_bound, int) or not isinstance(higher_bound, int):
            message: str = "lower_bound and higher_bound are required"
            raise InputError(status=error_codes.input_error_code, description=message)

        wallet_list: typing.List[WalletModel] = WalletModel.query(
            WalletModel.organization_id == organization_id, WalletModel.available_funds > lower_bound,
            WalletModel.available_funds < higher_bound).fetch_async().get_result()

        payload: typing.List[dict] = [wallet.to_dict() for wallet in wallet_list]
        if len(payload):
            return jsonify({'status': True, 'payload': payload,
                            'message': 'wallets returned'}), status_codes.status_ok_code

        message: str = "Wallets not found"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def wallet_transact(self, organization_id: typing.Union[str, None], uid: str,
                        add: int = None, sub: int = None) -> tuple:
        ***REMOVED***
            # TODO -- consider providing an amount to add or substract on a dict
            perform a transaction on a wallet
        :param organization_id:
        :param uid:
        :param add:
        :param sub:
        :return:
        ***REMOVED***
        # Raise InputError if any of this are not available
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        if not (isinstance(sub, int) or isinstance(add, int)):
            message: str = "sub or add are required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not self.can_update_wallet(organization_id=organization_id, uid=uid):
            message: str = "You are not authorized to perform a transaction on this wallet"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        wallet_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                         WalletModel.uid == uid).get()

        if isinstance(wallet_instance, WalletModel):
            # NOTE: insure that this works or perform this operation in another way
            if isinstance(sub, int):
                wallet_instance.available_funds.amount -= sub
            if isinstance(add, int):
                wallet_instance.available_funds.amount += sub
                
            key = wallet_instance.put()
            if not bool(key):
                message: str = "General error updating database"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            message: str = "Successfully created transaction"
            return jsonify({'status': True, 'payload': wallet_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = "Unable to find wallet - cannot perform transaction"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    async def wallet_transact_async(self, organization_id: typing.Union[str, None], uid: str,
                                    add: int = None, sub: int = None) -> tuple:
        ***REMOVED***
            asynchronous version of wallet_transact
        :param organization_id:
        :param uid:
        :param add:
        :param sub:
        :return:
        ***REMOVED***
        # Raise InputError if any of this are not available
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        if not (isinstance(sub, int) or isinstance(add, int)):
            message: str = "sub or add are required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not self.can_update_wallet_async(organization_id=organization_id, uid=uid):
            message: str = "You are not authorized to perform a transaction on this wallet"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        wallet_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                         WalletModel.uid == uid).get_async().get_result()

        if isinstance(wallet_instance, WalletModel):

            # NOTE: insure that this works or perform this operation in another way
            if isinstance(sub, int):
                wallet_instance.available_funds.amount -= sub
            if isinstance(add, int):
                wallet_instance.available_funds.amount += add

            key = wallet_instance.put_async().get_result()
            if not bool(key):
                message: str = "General error updating database"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            message: str = "Successfully created transaction"
            return jsonify({'status': True, 'payload': wallet_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = "Unable to find wallet - cannot perform transaction"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

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

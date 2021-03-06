"""
    **Module Wallet View Controller**
        Class Definitions for handling Wallet data input and validations
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from typing import Optional, List
from flask import jsonify, current_app
from google.cloud import ndb
from _sdk._email import Mailgun
from database.mixins import AmountMixin
from database.wallet import WalletModel, WalletValidator
from utils import return_ttl, create_id
from config.exceptions import DataServiceError, UnAuthenticatedError, status_codes, error_codes, InputError
from config.exception_handlers import handle_view_errors
from config.use_context import use_context
from cache.cache_manager import app_cache


class WalletEmails(Mailgun):
    """
        **Class WalletEmails**
            Class used to send Wallet related Emails and Notifications
    """

    def __init__(self) -> None:
        super().__init__()

    def send_balance_changed_notification(self, wallet_instance: WalletModel, organization_id: str, uid: str) -> None:
        """
            **send_balance_changed_notification**
                send an email to client or organization informing them that balance has changed on their wallet

        :param wallet_instance:
        :param organization_id:
        :param uid:
        :return:
        """
        user_data, organization_data = self.return_organization_user(organization_id=organization_id, uid=uid)

        email: str = user_data.get('email')
        name: str = user_data.get('names')
        surname: str = user_data.get('surname')
        email_verified: bool = user_data.get('email_verified')
        new_balance: AmountMixin = wallet_instance.available_funds
        monthly_withdrawal_allowance: AmountMixin = wallet_instance.monthly_withdrawal_allowance

        subject = f"{organization_data.get('organization_name')} Your Wallet Balance Changed"
        text = f'''
            hi {name} {surname} 
            this email is intended to notify you that your wallet balance has changed.
            
            Available Funds: {str(new_balance)}
            Monthly Withdrawal Allowance: {str(monthly_withdrawal_allowance)}
            
            Thank you
            {organization_data.get('organization_name')}                 
        '''
        html = f'''
            hi {name} {surname} 
            this email is intended to notify you that your wallet balance has changed.
            
            Available Funds: {str(new_balance)}
            Monthly Withdrawal Allowance: {str(monthly_withdrawal_allowance)}
            
            Thank you
            {organization_data.get('organization_name')}                         
        '''
        if email_verified:
            self._do_schedule_mail(to_email=email, subject=subject, text=text, html=html)

    def wallet_created_successfully(self, wallet_instance: WalletModel, organization_id: str, uid: str) -> None:
        """
            **wallet_created_successfully**
                send an email informing user that their wallet has been created and its details

        :param wallet_instance:
        :param organization_id:
        :param uid:
        :return:
        """
        user_data, organization_data = self.return_organization_user(organization_id=organization_id, uid=uid)
        email: str = user_data.get('email')
        name: str = user_data.get('names')
        surname: str = user_data.get('surname')
        email_verified: bool = user_data.get('email_verified')

        subject = f"{organization_data.get('organization_name')} wallet created successfully"

        text = f'''
               hi {name} {surname} 
               this email is intended to notify you that your wallet balance has been successfully created.
    
               Available Funds: {str(wallet_instance.available_funds)}
               Monthly Withdrawal Allowance: {str(wallet_instance.monthly_withdrawal_allowance)}
    
               Thank you
               {organization_data.get('organization_name')}                 
               '''
        html = f'''
               hi {name} {surname} 
               this email is intended to notify you that your wallet balance has been successfully created.
    
               Available Funds: {str(wallet_instance.available_funds)}
               Monthly Withdrawal Allowance: {str(wallet_instance.monthly_withdrawal_allowance)}
    
               Thank you
               {organization_data.get('organization_name')}                 
               '''
        if email_verified:
            self._do_schedule_mail(to_email=email, subject=subject, text=text, html=html)

    def wallet_details_changed(self, wallet_instance: WalletModel, organization_id: str, uid: str) -> None:
        """
            **wallet_details_changed**
                send an email informing the user that wallet details has changed

        :param wallet_instance:
        :param organization_id:
        :param uid:
        :return:
        """
        user_data, organization_data = self.return_organization_user(organization_id=organization_id, uid=uid)
        email: str = user_data.get('email')
        name: str = user_data.get('names')
        surname: str = user_data.get('surname')
        email_verified: bool = user_data.get('email_verified')

        subject = f"{organization_data.get('organization_name')} wallet created successfully"

        text = f'''
               hi {name} {surname} 
               this email is intended to notify you that your wallet details have changed.

               Available Funds: {str(wallet_instance.available_funds)}
               Monthly Withdrawal Allowance: {str(wallet_instance.monthly_withdrawal_allowance)}
               Paypal Email: {wallet_instance.paypal_address}
               is_verified: {wallet_instance.is_verified}
               last_transaction_time: {str(wallet_instance.last_transaction_time)}

               Thank you
               {organization_data.get('organization_name')}                 
               '''
        html = f'''
               hi {name} {surname} 
               this email is intended to notify you that your wallet details have changed.

               Available Funds: {str(wallet_instance.available_funds)}
               Monthly Withdrawal Allowance: {str(wallet_instance.monthly_withdrawal_allowance)}
               Paypal Email: {wallet_instance.paypal_address}
               is_verified: {wallet_instance.is_verified}
               last_transaction_time: {str(wallet_instance.last_transaction_time)}

               Thank you
               {organization_data.get('organization_name')}                 
               '''
        if email_verified:
            self._do_schedule_mail(to_email=email, subject=subject, text=text, html=html)


class Validator(WalletValidator):
    """
        **Class Wallet Validators**
            validates wallet transactions
        TODO- improve the validators to validate all aspects of wallet transactions
    """

    def __init__(self) -> None:
        super().__init__()
        self._max_retries: int = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout: int = current_app.config.get('DATASTORE_TIMEOUT')

    def _create_unique_wallet_id(self) -> str:
        """

        :return:
        """
        _id = create_id()
        wallet_instance: WalletModel = WalletModel.query(WalletModel.wallet_id == _id).get()
        # NOTE: if wallet_id is unique return it or Repeat otherwise
        return self._create_unique_wallet_id() if isinstance(wallet_instance, WalletModel) and bool(
            wallet_instance) else _id

    @staticmethod
    def raise_input_error_if_not_available(organization_id: str, uid: str) -> None:
        """
            **raise_input_error_if_not_available
                raise an error if organization_id or uid is not present

        :param organization_id:
        :param uid:
        :return: Nothing
        """

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

    @staticmethod
    def raise_input_error(**kwargs) -> None:
        """
            **raise_input_error**
                general function to raise input errors in-case when string variables are not string or are Empty
                raise an input error if any of the input variables are Null or Empty

        :param kwargs:
        :return:
        """
        for arg in kwargs.items():
            if not isinstance(arg, str) or not bool(arg.strip()):
                message: str = "{} is required".format(arg.__class__.__name__)
                raise InputError(status=error_codes.input_error_code, description=message)

    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def can_add_wallet(self, organization_id: Optional[str], uid: Optional[str] = None) -> bool:
        """
            **can_add_wallet**
                this method will check if a new wallet can be added

            :param organization_id:
            :param uid:
            :return:
        """
        # NOTE this will raise input error if either or this
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_exist: Optional[bool] = self.wallet_exist(organization_id=organization_id, uid=uid)
        if isinstance(wallet_exist, bool):
            return not wallet_exist

        # result is None meaning an error occurred then Raise a DataServiceError
        message: str = 'database Error: Unable to verify wallet data'
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.cache.memoize(timeout=return_ttl('short'))
    async def can_add_wallet_async(self, organization_id: Optional[str], uid: Optional[str] = None) -> bool:
        """
            **can_add_wallet_async**
                An asynchronous version of can_add_wallet
                testing if user can add a wallet

        :param organization_id:
        :param uid:
        :return:
        """

        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_exist: Optional[bool] = await self.wallet_exist_async(organization_id=organization_id, uid=uid)

        if isinstance(wallet_exist, bool):
            return not wallet_exist

        message: str = 'database Error: Unable to verify wallet data'
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def can_update_wallet(self, organization_id: Optional[str], uid: Optional[str] = None) -> bool:
        """
            **can_add_wallet**
                checks if user can update wallet - a wallet need to already exists for it to be updated
        :param organization_id:
        :param uid:
        :return:
        """
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_exist: Optional[bool] = self.wallet_exist(organization_id=organization_id, uid=uid)
        if isinstance(wallet_exist, bool):
            return wallet_exist
        message: str = 'database error: Unable to verify wallet data'
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.cache.memoize(timeout=return_ttl('short'))
    async def can_update_wallet_async(self, organization_id: Optional[str], uid: Optional[str] = None) -> bool:
        """
            **can_update_wallet_async**
                asynchronous version of can_update_wallet

        :param organization_id:
        :param uid:
        :return:
        """
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_exist: Optional[bool] = await self.wallet_exist_async(organization_id=organization_id, uid=uid)
        if isinstance(wallet_exist, bool):
            return wallet_exist
        message: str = "database error: Unable to verify wallet data"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def can_reset_wallet(self, organization_id: Optional[str], uid: Optional[str]) -> bool:
        """
            **can_reset_wallet**
                checks if user can reset wallet
        :param organization_id: required
        :param uid: required
        :return:
        """
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_exist: Optional[bool] = self.wallet_exist(organization_id=organization_id, uid=uid)
        if isinstance(wallet_exist, bool):
            return wallet_exist

        message: str = 'database Error: Unable to verify wallet data'
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    @app_cache.cache.memoize(timeout=return_ttl('short'))
    async def can_reset_wallet_async(self, organization_id: Optional[str],
                                     uid: Optional[str]) -> bool:
        """
            **can_reset_wallet_async**
                asynchronous version of can_reset_wallet
        :param organization_id:
        :param uid:
        :return:
        """
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_exist: Optional[bool] = await self.wallet_exist_async(organization_id=organization_id, uid=uid)

        if isinstance(wallet_exist, bool):
            return wallet_exist
        message: str = 'database Error: Unable to verify wallet data'
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)


# noinspection DuplicatedCode
class WalletView(Validator, WalletEmails):
    """
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
    """

    def __init__(self) -> None:
        super().__init__()

    @use_context
    @handle_view_errors
    def create_wallet(self, organization_id: Optional[str], uid: Optional[str],
                      currency: Optional[str], paypal_address: Optional[str],
                      is_org_wallet: bool = False) -> tuple:
        """
            **create_wallet**
                enables the system/user to create new wallet for a user - the user may not already own a wallet

        :param organization_id:
        :param uid:
        :param currency:
        :param paypal_address:
        :param is_org_wallet:
        :return: tuple with created wallet_instance
        """
        # NOTE: no need to check if organization_id and uid are available
        if not self.can_add_wallet(organization_id=organization_id, uid=uid):
            message: str = "You are not authorized to create a new Wallet"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        # creating new Wallet for a new user
        amount_instance: AmountMixin = AmountMixin(amount_cents=0, currency=currency)

        wallet_id: str = self._create_unique_wallet_id()

        wallet_instance: WalletModel = WalletModel(organization_id=organization_id, uid=uid, wallet_id=wallet_id,
                                                   is_org_wallet=is_org_wallet, available_funds=amount_instance,
                                                   paypal_address=paypal_address)

        key: Optional[ndb.Key] = wallet_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not isinstance(key, ndb.Key):
            message: str = "Database Error: Wallet may not have been created"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        _kwargs: dict = dict(wallet_view=WalletView, organization_id=organization_id, uid=uid)
        app_cache._schedule_cache_deletion(func=app_cache._delete_wallet_cache, kwargs=_kwargs)

        # Sending an email notification to the user informing them that the wallet has been created successfully
        kwargs: dict = dict(wallet_instance=wallet_instance, organization_id=organization_id, uid=uid)
        self._base_email_scheduler(func=self.wallet_created_successfully, kwargs=kwargs)
        return jsonify(dict(status=True,
                            payload=wallet_instance.to_dict(),
                            message='Successfully created wallet')), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    async def create_wallet_async(self, organization_id: Optional[str], uid: Optional[str], currency: Optional[str],
                                  paypal_address: Optional[str], is_org_wallet: bool = False) -> tuple:
        """
        **create_wallet_async**
            asynchronous version of create_wallet

            :param organization_id:
            :param uid:
            :param currency:
            :param paypal_address:
            :param is_org_wallet:
            
        :return: tuple with created wallet_instance
        """

        # NOTE: no need to check if organization_id and uid are available
        if not await self.can_add_wallet_async(organization_id=organization_id, uid=uid):
            message: str = "Operation Denied: cannot create a new Wallet"
            raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

        amount_instance: AmountMixin = AmountMixin(amount_cents=0, currency=currency)

        wallet_instance: WalletModel = WalletModel(organization_id=organization_id, uid=uid,
                                                   is_org_wallet=is_org_wallet,
                                                   available_funds=amount_instance,
                                                   paypal_address=paypal_address)

        key: Optional[ndb.Key] = wallet_instance.put_async(retries=self._max_retries,
                                                           timeout=self._max_timeout).get_result()
        if not isinstance(key, ndb.Key):
            raise DataServiceError(status=error_codes.data_service_error_code,
                                   description="An Error occurred creating Wallet")

        _kwargs: dict = dict(wallet_view=WalletView, organization_id=organization_id, uid=uid)
        app_cache._schedule_cache_deletion(func=app_cache._delete_wallet_cache, kwargs=_kwargs)

        # Sending an email notification to the user informing them that the wallet has been created successfully
        kwargs: dict = dict(wallet_instance=wallet_instance, organization_id=organization_id, uid=uid)
        self._base_email_scheduler(func=self.wallet_created_successfully, kwargs=kwargs)        
        return jsonify(dict(status=True, payload=wallet_instance.to_dict(),
                            message='Successfully Created Wallet')), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def get_wallet(self, organization_id: Optional[str], uid: Optional[str]) -> tuple:
        """
            **get_wallet**
                # TODO- may need to update cache or find a way to update cache when there are updates
                # this could mean that the old method of having a separate cache for every module may be useful here

                returns a specific wallet from database

        :param organization_id:
        :param uid:
        :return: tuple
        """
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                         WalletModel.uid == uid).get()
        if isinstance(wallet_instance, WalletModel) and bool(wallet_instance):
            return jsonify(dict(status=True,
                                payload=wallet_instance.to_dict(),
                                message='wallet found')), status_codes.status_ok_code

        message: str = "Wallet not found"
        return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    async def get_wallet_async(self, organization_id: Optional[str], uid: Optional[str]) -> tuple:
        """
            **get_wallet_async**
                get_wallet_async an asynchronous version of get_wallet

        :param organization_id:
        :param uid:
        :return:
        """
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        wallet_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                         WalletModel.uid == uid).get_async().get_result()
        if isinstance(wallet_instance, WalletModel) and bool(wallet_instance):
            return jsonify(dict(status=True,
                                payload=wallet_instance.to_dict(),
                                message='Wallet found')), status_codes.status_ok_code

        message: str = "Wallet not found"
        return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def update_wallet(self, wallet_data: dict) -> tuple:
        """
            **update_wallet**
                lets user or system update wallet

        :param wallet_data:
        :return:
        """

        uid: Optional[str] = wallet_data.get("uid")
        organization_id: Optional[str] = wallet_data.get('organization_id')
        # NOTE checking if organization_id or uid is present
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        # NOTE: integer conversion errors will be caught by handle_view_errors as ValueError
        available_funds: int = int(wallet_data.get("available_funds", 0))

        if not isinstance(available_funds, int):
            message: str = "available_funds is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        currency: Optional[str] = wallet_data.get('currency')
        if not isinstance(currency, str) or not bool(currency.strip()):
            message: str = "currency symbol is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        paypal_address: Optional[str] = wallet_data.get("paypal_address")
        if not isinstance(paypal_address, str) or not bool(paypal_address.strip()):
            message: str = "paypal_address is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        # TODO update can update wallet to take into account Org Account Roles
        if not self.can_update_wallet(organization_id=organization_id, uid=uid):
            message: str = "You are not authorized to update this Wallet"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        wallet_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                         WalletModel.uid == uid).get()

        # No need to test for wallet availability as can update returned True
        amount_instance: AmountMixin = AmountMixin(amount_cents=available_funds, currency=currency)
        wallet_instance.available_funds = amount_instance        
        wallet_instance.paypal_address = paypal_address
        key: Optional[ndb.Key] = wallet_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not isinstance(key, ndb.Key):
            message: str = "Database Error: occurred updating Wallet"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        _kwargs: dict = dict(wallet_view=WalletView, organization_id=organization_id, uid=uid)
        app_cache._schedule_cache_deletion(func=app_cache._delete_wallet_cache, kwargs=_kwargs)

        kwargs: dict = dict(wallet_instance=wallet_instance, organization_id=organization_id, uid=uid)
        self._base_email_scheduler(func=self.wallet_details_changed, kwargs=kwargs)

        return jsonify(dict(status=True,
                            payload=wallet_instance.to_dict(),
                            message='successfully updated wallet')), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    async def update_wallet_async(self, wallet_data: dict) -> tuple:
        """
            **update_wallet_async**
                can update wallet asynchronous version of
        :param wallet_data:
        :return:
        """

        uid: Optional[str] = wallet_data.get("uid")
        organization_id: Optional[str] = wallet_data.get('organization_id')
        # NOTE checking if organization_id or uid is present
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        available_funds: int = int(wallet_data.get("available_funds", 0))

        if not isinstance(available_funds, int):
            message: str = "available_funds is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        currency: Optional[str] = wallet_data.get('currency')
        if not isinstance(currency, str) or not bool(currency.strip()):
            message: str = "currency symbol is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        paypal_address: Optional[str] = wallet_data.get("paypal_address")
        if not isinstance(paypal_address, str) or not bool(paypal_address.strip()):
            message: str = "paypal_address is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        # TODO update can update wallet to take into account Org Account Roles
        if not self.can_update_wallet_async(organization_id=organization_id, uid=uid):
            message: str = "You are not authorized to update this Wallet"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        wallet_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                         WalletModel.uid == uid).get_async().get_result()

        # No need to test for wallet availability as can update returned True

        amount_instance: AmountMixin = AmountMixin(amount_cents=available_funds, currency=currency)
        wallet_instance.available_funds = amount_instance
        wallet_instance.paypal_address = paypal_address
        key: Optional[ndb.Key] = wallet_instance.put_async(
            retries=self._max_retries, timeout=self._max_timeout).get_result()
        if not isinstance(key, ndb.Key):
            message: str = "Database Error: while updating wallet"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        _kwargs: dict = dict(wallet_view=WalletView, organization_id=organization_id, uid=uid)
        app_cache._schedule_cache_deletion(func=app_cache._delete_wallet_cache, kwargs=_kwargs)

        kwargs: dict = dict(wallet_instance=wallet_instance, organization_id=organization_id, uid=uid)
        self._base_email_scheduler(func=self.wallet_details_changed, kwargs=kwargs)

        return jsonify(dict(status=True,
                            payload=wallet_instance.to_dict(),
                            message='successfully updated wallet')), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def reset_wallet(self, wallet_data: dict) -> tuple:
        """
            **reset_wallet**
                resets wallet to their default values except the uid and organization_Id

        :param wallet_data:
        :return:
        """
        uid: Optional[str] = wallet_data.get('uid')
        organization_id: Optional[str] = wallet_data.get('organization_id')
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        currency: Optional[str] = wallet_data.get('currency')
        if not isinstance(currency, str) or not bool(currency.strip()):
            message: str = "currency is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if self.can_reset_wallet(organization_id=organization_id, uid=uid) is True:
            message: str = "You are not authorized to reset this wallet"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        wallet_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                         WalletModel.uid == uid).get()

        amount_instance: AmountMixin = AmountMixin(amount_cents=0, currency=currency)
        wallet_instance.available_funds = amount_instance
        key: Optional[ndb.Key] = wallet_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not isinstance(key, ndb.Key):
            message: str = "Database Error: while updating wallet"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        # Note scheduling cache deletion function
        _kwargs: dict = dict(wallet_view=WalletView, organization_id=organization_id, uid=uid)
        app_cache._schedule_cache_deletion(func=app_cache._delete_wallet_cache, kwargs=_kwargs)

        # Note scheduling an email to send wallet details changed notifications
        kwargs: dict = dict(wallet_instance=wallet_instance, organization_id=organization_id, uid=uid)
        self._base_email_scheduler(func=self.wallet_details_changed, kwargs=kwargs)

        return jsonify(dict(status=True,
                            payload=wallet_instance.to_dict(),
                            message='Wallet successfully updated')), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    async def reset_wallet_async(self, wallet_data: dict) -> tuple:
        """
            **reset_wallet_async**
                asynchronous version of reset wallet

        :param wallet_data:
        :return:
        """

        uid: Optional[str] = wallet_data.get('uid')
        organization_id: Optional[str] = wallet_data.get('organization_id')
        self.raise_input_error_if_not_available(organization_id=organization_id, uid=uid)

        currency: Optional[str] = wallet_data.get('currency')
        if not isinstance(currency, str) or not bool(currency.strip()):
            message: str = "currency is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not await self.can_reset_wallet_async(organization_id=organization_id, uid=uid):
            message: str = "You are not authorized to reset this wallet"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        wallet_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                         WalletModel.uid == uid).get_async().get_result()

        amount_instance: AmountMixin = AmountMixin(amount_cents=0, currency=currency)
        wallet_instance.available_funds = amount_instance
        key: Optional[ndb.Key] = wallet_instance.put_async(
            retries=self._max_retries, timeout=self._max_timeout).get_result()
        if not isinstance(key, ndb.Key):
            message: str = "Database error while resetting wallet"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        # Note Scheduling task to delete caches
        _kwargs: dict = dict(wallet_view=WalletView, organization_id=organization_id, uid=uid)
        app_cache._schedule_cache_deletion(func=app_cache._delete_wallet_cache, kwargs=_kwargs)

        # Note scheduling task to send Emails
        kwargs: dict = dict(wallet_instance=wallet_instance, organization_id=organization_id, uid=uid)
        self._base_email_scheduler(func=self.wallet_details_changed, kwargs=kwargs)

        return jsonify(dict(status=True,
                            payload=wallet_instance.to_dict(),
                            message='Wallet successfully updated')), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def return_all_wallets(self, organization_id: Optional[str]) -> tuple:
        """
            **return_all_wallets**
                given an organization_id return all the organizations wallets

        :param organization_id:
        :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        wallet_list: List[WalletModel] = WalletModel.query(WalletModel.organization_id == organization_id).fetch()
        payload: List[dict] = [wallet.to_dict() for wallet in wallet_list]

        if payload:
            return jsonify(dict(status=True,
                                payload=payload,
                                message='Wallets Found and Returned')), status_codes.status_ok_code

        message: str = 'Data Not Found: Wallets not found meeting the search criteria'
        return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    async def return_all_wallets_async(self, organization_id: Optional[str]) -> tuple:
        """
            **return_all_wallets_async**
                given an organization_id return all the organizations wallets

        :param organization_id:
        :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

        wallet_list: List[WalletModel] = WalletModel.query(
            WalletModel.organization_id == organization_id).fetch_async().get_result()

        payload: List[dict] = [wallet.to_dict() for wallet in wallet_list]

        if payload:
            message: str = 'Wallets found'
            return jsonify(dict(status=True, payload=payload, message=message)), status_codes.status_ok_code
        return jsonify(dict(status=False, message='wallets not found')), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def return_wallets_by_balance(self, organization_id: Optional[str],
                                  lower_bound: int, higher_bound: int) -> tuple:
        """
            **return_wallets_by_balance**
                # TODO consider supplying lower_bound and higher_bound as a dict
                return wallets with balances within lower_bound and higher_bound
        :param organization_id:
        :param lower_bound:
        :param higher_bound:
        :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(lower_bound, int) or not isinstance(higher_bound, int):
            message: str = "lower_bound and higher_bound are required"
            raise InputError(status=error_codes.input_error_code, description=message)

        wallet_list: List[WalletModel] = WalletModel.query(WalletModel.organization_id == organization_id).fetch()

        payload: List[dict] = [wallet.to_dict() for wallet in wallet_list if
                               higher_bound < wallet.available_funds.amount_cents > lower_bound]

        if payload:
            message: str = 'Wallets returned'
            return jsonify(dict(status=True, payload=payload, message=message)), status_codes.status_ok_code

        message: str = "Data Not Found: There are no wallets found meeting your search criteria"
        return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    async def return_wallets_by_balance_async(self, organization_id: Optional[str],
                                              lower_bound: int, higher_bound: int) -> tuple:
        """
            **return_wallets_by_balance_async**
                # TODO - consider changing the function name to : return_wallets_by_balance_range_async
                asynchronous version of return wallets by balance

        :param organization_id:
        :param lower_bound:
        :param higher_bound:
        :return:
        """

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(lower_bound, int) or not isinstance(higher_bound, int):
            message: str = "lower_bound and higher_bound are required"
            raise InputError(status=error_codes.input_error_code, description=message)

        wallet_list: List[WalletModel] = WalletModel.query(
            WalletModel.organization_id == organization_id).fetch_async().get_result()

        payload: List[dict] = [wallet.to_dict() for wallet in wallet_list if
                               higher_bound < wallet.available_funds.amount_cents > lower_bound]

        if payload:
            return jsonify(dict(status=True, payload=payload, message='wallets returned')), status_codes.status_ok_code

        message: str = "Wallets not found"
        return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def wallet_transact(self, organization_id: Optional[str], uid: str,
                        add: int = None, sub: int = None) -> tuple:
        """
            **wallet_transact**
                # TODO -- consider providing an amount to add or subtract on a dict
                perform a transaction on a wallet
        :param organization_id:
        :param uid:
        :param add:
        :param sub:
        :return:
        """
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

        if not isinstance(wallet_instance, WalletModel) or wallet_instance.uid != uid:
            message: str = "Unable to find wallet - cannot perform transaction"
            return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

        if isinstance(sub, int):
            wallet_instance.available_funds.amount_cents -= sub
        if isinstance(add, int):
            wallet_instance.available_funds.amount_cents += sub

        key: Optional[ndb.Key] = wallet_instance.put()
        if not isinstance(key, ndb.Key):
            message: str = "General error updating database"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        # Scheduling cache deletions
        _kwargs: dict = dict(wallet_view=WalletView, organization_id=organization_id, uid=uid)
        app_cache._schedule_cache_deletion(func=app_cache._delete_wallet_cache, kwargs=_kwargs)

        # Scheduling emails
        kwargs: dict = dict(wallet_instance=wallet_instance, organization_id=organization_id, uid=uid)
        self._base_email_scheduler(func=self.send_balance_changed_notification, kwargs=kwargs)

        message: str = "Successfully created transaction"
        return jsonify(dict(status=True,
                            payload=wallet_instance.to_dict(),
                            message=message)), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    async def wallet_transact_async(self, organization_id: Optional[str], uid: str,
                                    add: int = None, sub: int = None) -> tuple:
        """
            **wallet_transact_async**
                asynchronous version of wallet_transact
        :param organization_id:
        :param uid:
        :param add:
        :param sub:
        :return:
        """
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

        if not isinstance(wallet_instance, WalletModel) or wallet_instance.uid != uid:
            message: str = "Unable to find wallet - cannot perform transaction"
            return jsonify(dict(status=False, message=message)), status_codes.data_not_found_code

        if isinstance(sub, int):
            wallet_instance.available_funds.amount_cents -= sub
        if isinstance(add, int):
            wallet_instance.available_funds.amount_cents += add

        key: Optional[ndb.Key] = wallet_instance.put_async().get_result()
        if not isinstance(key, ndb.Key):
            message: str = "General error updating database"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        _kwargs: dict = dict(wallet_view=WalletView, organization_id=organization_id, uid=uid)
        app_cache._schedule_cache_deletion(func=app_cache._delete_wallet_cache, kwargs=_kwargs)

        message: str = "Successfully created transaction"
        return jsonify(dict(status=True,
                            payload=wallet_instance.to_dict(),
                            message=message)), status_codes.successfully_updated_code

    # noinspection PyUnusedLocal
    @use_context
    @handle_view_errors
    def _wallet_withdraw_funds(self, organization_id: Optional[str], uid: str, amount: int) -> tuple:
        """
            **wallet_withdraw_funds**
                ** for system admin or system calls only
                organization must contain settings for funds withdrawals
                i.e from which paypal account may the withdrawal occur
                and so on.

                steps create a withdrawal transaction,
                with the requested amount,
                await admin approvals,
                cron job must run and process all approved withdrawals
                cron job must retain all the results of the transactions and save on the database
        :param organization_id: string ->
        :param uid: string ->
        :param amount: AmountMixin ->
        :return:
        """
        # TODO - complete this method

        _kwargs: dict = dict(wallet_view=WalletView, organization_id=organization_id, uid=uid)
        app_cache._schedule_cache_deletion(func=app_cache._delete_wallet_cache, kwargs=_kwargs)

        return "OK", status_codes.status_ok_code

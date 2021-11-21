"""
    Swagger Compatible API for wallet
"""
from flask_apispec import doc, marshal_with, use_kwargs
from _swagger_api import ViewModel
from _swagger_api.schemas.wallet import WalletResponseSchema, WalletListResponseSchema, WalletRequestSchema
from security.api_authenticator import handle_api_auth
from views import wallet_view


# TODO add request Schema


class WalletView(ViewModel):
    """
        **WalletView**
            get, update, delete Wallet
    """
    methods = ["GET", "PUT", "POST", "DELETE"]
    method_decorators = [handle_api_auth]

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    @doc(description=wallet_view.get_wallet.__doc__)
    @marshal_with(WalletResponseSchema)
    def get(organization_id: str, uid: str) -> tuple:
        """
            eval(wallet_view.get_wallet.__doc__)
        :return:
        """
        return wallet_view.get_wallet(organization_id=organization_id, uid=uid)

    @staticmethod
    @doc(description=wallet_view.update_wallet.__doc__)
    @marshal_with(WalletResponseSchema)
    @use_kwargs(WalletRequestSchema, location='json')
    def put(payload: dict) -> tuple:
        """
            updates an existing wallet by uid
        :return:
        """
        return wallet_view.update_wallet(wallet_data=payload)

    @staticmethod
    @doc(description=wallet_view.create_wallet.__doc__)
    @marshal_with(WalletResponseSchema)
    @use_kwargs(WalletRequestSchema, location='json')
    def post(payload: dict) -> tuple:
        """
        **Create User Wallet**
            create new user wallet
        :return:
        """
        organization_id: str = payload.get('organization_id')
        uid: str = payload.get('uid')
        currency: str = payload.get('currency')
        paypal_address: str = payload.get('paypal_address')

        return wallet_view.create_wallet(organization_id=organization_id,
                                         uid=uid,
                                         currency=currency,
                                         paypal_address=paypal_address,
                                         is_org_wallet=False)

    @staticmethod
    @doc(description=wallet_view.reset_wallet.__doc__)
    @marshal_with(WalletResponseSchema)
    def delete(organization_id: str, uid: str) -> tuple:
        """
            deletes an existing wallet by uid
        :return:
        """
        return wallet_view.reset_wallet(wallet_data=dict(organization_id=organization_id, uid=uid))


class WalletListView(ViewModel):
    """
        **WalletListView**
            returns a list of all wallets for a specific organization
    """
    methods = ["GET"]
    method_decorators = [handle_api_auth]

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    @doc(description=wallet_view.return_all_wallets.__doc__)
    @marshal_with(WalletListResponseSchema)
    def get(organization_id: str) -> tuple:
        """
        **get**
            will return a list of all wallets belonging to a specific organization
        :return:
        """
        return wallet_view.return_all_wallets(organization_id=organization_id)


class OrganizationWallets(ViewModel):
    """
        **OrganizationWallets**
            create organization wallets
    """
    methods = ["POST"]
    method_decorators = [handle_api_auth]

    @staticmethod
    @doc(description=wallet_view.create_wallet.__doc__)
    @marshal_with(WalletResponseSchema)
    def post(wallet_dict: dict) -> tuple:
        """
        **Create Organization Wallet**
            create a new organizational wallet
        :return:
        """
        organization_id: str = wallet_dict.get('organization_id')
        uid: str = wallet_dict.get('uid')
        currency: str = wallet_dict.get('currency')
        paypal_address: str = wallet_dict.get('paypal_address')

        return wallet_view.create_wallet(organization_id=organization_id,
                                         uid=uid,
                                         currency=currency,
                                         paypal_address=paypal_address,
                                         is_org_wallet=True)

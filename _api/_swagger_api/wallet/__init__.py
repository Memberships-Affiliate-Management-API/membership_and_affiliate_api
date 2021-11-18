"""
    Swagger Compatible API for wallet
"""
from _api._swagger_api import ViewModel
from security.api_authenticator import handle_api_auth


class WalletView(ViewModel):
    """
        **WalletView**
            get, update, delete Wallet
    """
    methods = ["GET", "PUT", "DELETE"]
    method_decorators = [handle_api_auth]

    def __init__(self) -> None:
        super().__init__()

    def get(self):
        """
            fetches an existing wallet using uid
        :return:
        """
        pass

    def put(self):
        """
            updates an existing wallet by uid
        :return:
        """
        pass

    def delete(self):
        """
            deletes an existing wallet by uid
        :return:
        """
        pass

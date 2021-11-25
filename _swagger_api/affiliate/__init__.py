from flask_apispec import doc, marshal_with, use_kwargs

from _swagger_api import ViewModel
from _swagger_api.schemas.affiliate import AffiliateResponseSchema
from security.api_authenticator import handle_api_auth
from views import affiliates_view


class AffiliateView(ViewModel):
    """
        **Class AffiliateView**

    """
    methods = ['GET', 'POST', 'PUT', 'GET']
    method_decorators = [handle_api_auth]

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    @doc(description=affiliates_view.get_affiliate.__doc__)
    @marshal_with(AffiliateResponseSchema)
    def get(**payload) -> tuple:
        """
        ** obtains a specific affiliate record **
            :return:
        """
        return affiliates_view.get_affiliate(payload)

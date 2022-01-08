from __future__ import annotations
from typing import List, Callable

from flask_apispec import doc, marshal_with, use_kwargs
from _swagger_api import ViewModel
from _swagger_api.schemas.affiliate import AffiliateResponseSchema
from security.api_authenticator import handle_api_auth
from views import affiliates_view


class AffiliateView(ViewModel):
    """
        **Class AffiliateView**
    """
    def __new__(cls, *args, **kwargs) -> AffiliateView:
        cls.methods: List[str] = ['GET', 'POST']
        cls.method_decorators: List[Callable] = [handle_api_auth]
        return super().__new__(cls, *args, **kwargs)

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
    
    @staticmethod
    @doc(description=affiliates_view.register_affiliate.__doc__)
    @marshal_with(AffiliateResponseSchema)
    def post(**payload) -> tuple:
        """
            **create a new affiliate**
        :param payload:
        :return:
        """
        return affiliates_view.register_affiliate(payload)



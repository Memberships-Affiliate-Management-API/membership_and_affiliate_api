"""
    BaseModels for Swagger based restful api
"""
from __future__ import annotations
from flask_apispec import MethodResource
from flask_restful import Resource


class ViewModel(MethodResource, Resource):
    """
    ViewModel class
    """
    def __new__(cls, *args, **kwargs) -> ViewModel:
        return super().__new__(cls, *args, **kwargs)

    def __init__(self) -> None:
        """
        Constructor
        """
        super().__init__()


class ListViewModel(MethodResource, Resource):
    """
    ListViewModel class
    """
    def __new__(cls, *args, **kwargs) -> ListViewModel:
        return super().__new__(cls, *args, **kwargs)

    def __init__(self) -> None:
        """
        Constructor
        """
        super().__init__()

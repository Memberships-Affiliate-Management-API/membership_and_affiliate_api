"""
    BaseModels for Swagger based restful api
"""

from flask_apispec import MethodResource
from flask_restful import Resource


class ViewModel(MethodResource, Resource):
    """
    ViewModel class
    """
    methods = []
    method_decorators = []

    def __init__(self):
        """
        Constructor
        """
        super().__init__()


class ListViewModel(MethodResource, Resource):
    """
    ListViewModel class
    """
    methods = []
    method_decorators = []

    def __init__(self):
        """
        Constructor
        """
        super().__init__()

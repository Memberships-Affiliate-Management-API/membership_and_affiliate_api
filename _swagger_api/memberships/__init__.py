from flask_apispec import doc, marshal_with
from _swagger_api import ViewModel
from _swagger_api.schemas.memberships import MembershipResponseSchema
from security.api_authenticator import handle_api_auth
from views import memberships_view


class MembershipsView(ViewModel):
    """
        ** Class  MembershipsView **
            View model for Memberships
    """
    methods = ['GET', 'POST', 'PUT']
    method_decorators = [handle_api_auth]

    def __init__(self):
        super().__init__()

    @staticmethod
    @doc(description=memberships_view.is_member_off.__doc__)
    @marshal_with(MembershipResponseSchema)
    def get(self, **payload):
        """
        **get memberships**
            Get all memberships
        """
        return memberships_view.is_member_off(**payload)

    @staticmethod
    @doc(description=memberships_view.add_membership.__doc__)
    @marshal_with(MembershipResponseSchema)
    def post(self, **payload):
        """
        **create memberships**
            Create a new membership
        """
        return memberships_view.add_membership(**payload)

    @staticmethod
    @doc(description=memberships_view.update_membership.__doc__)
    @marshal_with(MembershipResponseSchema)
    def put(self, **payload):
        """
        **update membership**
            Update a membership
        """
        return memberships_view.update_membership(**payload)

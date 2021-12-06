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
    def get(**payload):
        """
        **get memberships**
            Get all memberships
        """
        return memberships_view.is_member_off(**payload)

    @staticmethod
    @doc(description=memberships_view.add_membership.__doc__)
    @marshal_with(MembershipResponseSchema)
    def post(**payload):
        """
        **create memberships**
            Create a new membership
        """
        return memberships_view.add_membership(**payload)

    @staticmethod
    @doc(description=memberships_view.update_membership.__doc__)
    @marshal_with(MembershipResponseSchema)
    def put(**payload):
        """
        **update membership**
            Update a membership
        """
        return memberships_view.update_membership(**payload)


class MembershipPaymentsView(ViewModel):
    """
        allows clients to access & create memberships payment records
    """
    methods = ['GET', 'POST', 'PUT']
    method_decorators = [handle_api_auth]

    def __init__(self):
        super().__init__()

    @staticmethod
    @doc(description="get membership payment record")
    @marshal_with()
    def get(**payload):
        """
            get membership payment record
        :return:
        """
        pass

    @staticmethod
    def post(**payload):
        """
            create membership payment record
        :return:
        """
        pass

    @staticmethod
    def put(**payload):
        """
            update membership payment record
        :return:
        """
        pass


class CouponsView(ViewModel):
    """

    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def get(**payload):
        """
            get Coupons View
        :param payload:
        :return:
        """
        pass

    @staticmethod
    def post(**payload):
        """
            create coupon codes
        :param payload:
        :return:
        """
        pass

    @staticmethod
    def put(**payload):
        """
            update coupon codes
        :param payload:
        :return:
        """
        pass



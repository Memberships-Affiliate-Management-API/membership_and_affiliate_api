"""
    ** Class Memberships **
        memberships view model
"""
from __future__ import annotations
from collections import Callable
from typing import List

from marshmallow import fields
from _swagger_api.schemas.coupons import CouponResponseSchema
from flask_apispec import doc, marshal_with, use_kwargs
from _swagger_api import ViewModel
from _swagger_api.schemas.memberships import MembershipPaymentResponseSchema, MembershipResponseSchema
from security.api_authenticator import handle_api_auth
from views import memberships_view, coupons_view


class MembershipsView(ViewModel):
    """
        ** Class  MembershipsView **
            View model for Memberships
    """
    def __new__(cls, *args, **kwargs) -> MembershipsView:
        cls.methods: List[str] = ['GET', 'POST', 'PUT']
        cls.method_decorators: List[Callable] = [handle_api_auth]
        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        super().__init__()

    @staticmethod
    @doc(description=memberships_view.is_member_off.__doc__)
    @marshal_with(MembershipResponseSchema)
    def get(**payload) -> tuple:
        """
            **get memberships**
                Get all memberships
        """
        return memberships_view.is_member_off(**payload)

    @staticmethod
    @doc(description=memberships_view.add_membership.__doc__)
    @marshal_with(MembershipResponseSchema)
    def post(**payload) -> tuple:
        """
            **create memberships**
                Create a new membership
        """
        return memberships_view.add_membership(**payload)

    @staticmethod
    @doc(description=memberships_view.update_membership.__doc__)
    @marshal_with(MembershipResponseSchema)
    def put(**payload) -> tuple:
        """
            ** update membership **
                Update a membership
        """
        return memberships_view.update_membership(**payload)


class MembershipPaymentsView(ViewModel):
    """
        ** Class MembershipPaymentsView **
        allows clients to access & create memberships payment records
    """

    def __new__(cls, *args, **kwargs) -> MembershipPaymentsView:
        """new MembershipPaymentsView"""
        cls.methods = ['GET', 'POST', 'PUT']
        cls.method_decorators = [handle_api_auth]
        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        """initialize MembershipPaymentsView"""
        super().__init__()

    @staticmethod
    @doc(description="get membership payment record")
    @marshal_with(MembershipPaymentResponseSchema)
    def get(**payload) -> tuple:
        """
            get membership payment record
        :return:
        """
        pass

    @staticmethod
    @doc(description="create membership payment record")
    @marshal_with(MembershipPaymentResponseSchema)
    def post(**payload) -> tuple:
        """
        ** create membership **
            create membership payment record
        :return:
        """
        pass

    @staticmethod
    @doc(description="update membership payment record")
    @marshal_with(MembershipPaymentResponseSchema)
    def put(**payload) -> tuple:
        """
            ** update membership **
                update membership payment record
        :return:
        """
        pass


class CouponsView(ViewModel):
    """
        allows access and updating of coupon codes

    """
    def __new__(cls, *args, **kwargs) -> CouponsView:
        cls.methods = ['GET', 'POST', 'PUT']
        cls.method_decorators = [handle_api_auth]
        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        super().__init__()

    @staticmethod
    @doc(description="get coupon code")
    @marshal_with(CouponResponseSchema)
    def get(**payload) -> tuple:
        """
        ** get coupon codes **
            get Coupons View
        :param payload:
        :return:
        """
        # coupon_data must include organization_id and code
        return coupons_view.get_coupon(coupon_data=payload)

    @staticmethod
    @doc(description="create coupon code")
    @marshal_with(CouponResponseSchema)
    @use_kwargs({'organization_id': fields.String(), 'code': fields.String(), 'discount': fields.Integer(),
                 'expiration_time': fields.Integer()}, location='json')
    def post(**payload) -> tuple:
        """
            ** create coupon codes **
                create new coupon codes
        :param payload:
        :return:
        """
        # organization_id: str, code: str, discount: int, expiration_time: str
        return coupons_view.add_coupon(**payload)

    @staticmethod
    @doc(description="update coupon code")
    @marshal_with(CouponResponseSchema)
    @use_kwargs({'organization_id': fields.String(), 'code': fields.String(), 'discount': fields.Integer(),
                 'expiration_time': fields.Integer()}, location='json')
    def put(**payload) -> tuple:
        """
            ** put coupon **
                update coupon codes
        :param payload:
        :return:
        """
        #  organization_id: str, code: str, discount: int, expiration_time: int
        return coupons_view.add_coupon(**payload)


class CouponsListView(ViewModel):
    """
        **Class CouponsListView**
            will return a list of all coupon codes
    """

    def __new__(cls, *args, **kwargs) -> CouponsListView:
        """New CouponsListView"""
        cls.methods = ['GET', 'POST', 'PUT', 'DELETE']
        cls.method_decorators = [handle_api_auth]
        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        """initialize CouponsListView"""
        super().__init__()

    @staticmethod
    @doc(description="get coupons list")
    @use_kwargs({'organization_id': fields.String()}, location='json')
    def get(**payload) -> tuple:
        """
            will return a list of all coupon codes
        :return:
        """
        return coupons_view.get_all_coupons(organization_id=payload.get('organization_id'))

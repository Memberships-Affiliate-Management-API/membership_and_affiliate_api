"""
    **Module Memberships Client API**
        Memberships related api requests will be handled here
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import hmac
from datetime import date
from typing import Optional
from flask import Blueprint, request, current_app
from config.exceptions import if_bad_request_raise, UnAuthenticatedError, error_codes, InputError
from security.apps_authenticator import handle_apps_authentication
from utils import today
from views import memberships_view, membership_plans_view

memberships_client_api_bp = Blueprint('memberships_client_api', __name__)


# noinspection DuplicatedCode
@memberships_client_api_bp.route('/_api/v1/client/memberships/<string:path>', methods=['POST'])
@handle_apps_authentication
def memberships_client_api(path: str) -> tuple:
    """
        **memberships_client_api**
            handles client admin requests for memberships -
            this means clients or developers

            **USE CASES**
                1. will subscribe to membership plans in order to use this website from this endpoint
            - this endpoints can be called from the client dashboard
            in order to start using the API for as a paid client or a free client
    :param path:
    :return:
    """
    if_bad_request_raise(request)
    json_data: dict = request.get_json()

    if not isinstance(json_data, dict):
        message: str = "Invalid Input format this endpoint accept only json_data"
        raise InputError(status=error_codes.input_error_code, description=message)

    secret_key: Optional[str] = json_data.get('SECRET_KEY')
    _secret_keys_match: bool = hmac.compare_digest(secret_key, current_app.config.get('SECRET_KEY'))

    if not _secret_keys_match:
        message: str = 'User Not Authorized: you cannot perform this action'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code,
                                   description=message)
    # NOTE : this enable clients to join membership plans in order to start
    #  using api
    if path == "subscribe":
        # Memberships Subscriptions
        plan_id: Optional[str] = json_data.get('plan_id')
        uid: Optional[str] = json_data.get('uid')
        organization_id: Optional[str] = current_app.config.get('ORGANIZATION_ID')
        # consider verifying organization_id and uid
        payment_method: Optional[str] = json_data.get('payment_method')
        plan_start_date: date = today()
        return memberships_view.add_membership(organization_id=organization_id, uid=uid,
                                               plan_id=plan_id, payment_method=payment_method,
                                               plan_start_date=plan_start_date)

    elif path == "un-subscribe":
        plan_id: Optional[str] = json_data.get('plan_id')
        uid: Optional[str] = json_data.get('uid')
        organization_id: Optional[str] = json_data.get('organization_id')
        return memberships_view.un_subscribe(organization_id=organization_id, uid=uid, plan_id=plan_id)


@memberships_client_api_bp.route('/_api/v1/client/admin/memberships/<string:path>', methods=["POST"])
@handle_apps_authentication
def client_memberships_management(path: str) -> tuple:
    """
        **client_memberships_management**
            used to manage client's membership plans which they are offering to the
            public - this api will also be called from client dashboard app

            **USE CASES**
                1. create and update services or products - NOT HERE
                2. create and update membership plans / payment plans for services or products

    :param path:
    :return:
    """
    if_bad_request_raise(request)
    json_data: dict = request.get_json()

    # this endpoint allows users to create their own membership plan should be called after service
    # has been created and with the service or product id

    if not isinstance(json_data, dict):
        message: str = "Invalid Input format this endpoint accept only json_data"
        raise InputError(status=error_codes.input_error_code, description=message)

    secret_key: Optional[str] = json_data.get('SECRET_KEY')
    _secret_keys_match: bool = hmac.compare_digest(secret_key, current_app.config.get('SECRET_KEY'))

    if not _secret_keys_match:
        message: str = 'User Not Authorized: you cannot perform this action'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code,
                                   description=message)

    # NOTE: creates a new membership plan
    organization_id: Optional[str] = current_app.config.get('ORGANIZATION_ID')
    service_id: Optional[str] = json_data.get('service_id')
    plan_name: Optional[str] = json_data.get('plan_name')
    description: Optional[str] = json_data.get('description')
    schedule_day: Optional[int] = json_data.get('schedule_day')
    schedule_term: Optional[str] = json_data.get('schedule_term')
    term_payment: Optional[int] = json_data.get('term_payment')
    registration_amount: Optional[int] = json_data.get('registration_amount')
    currency: Optional[str] = json_data.get('currency')

    # NOTE : relevant to update membership plan
    is_active: Optional[bool] = json_data.get('is_active')
    plan_id: Optional[str] = json_data.get('plan_id')

    if path == "create-membership-plan":
        # NOTE: All monetary amounts are in cents - USD cents
        return membership_plans_view.add_plan(organization_id=organization_id, service_id=service_id,
                                              plan_name=plan_name, description=description,
                                              schedule_day=schedule_day, schedule_term=schedule_term,
                                              term_payment=term_payment, registration_amount=registration_amount,
                                              currency=currency)

    elif path == "update-membership-plan":
        return membership_plans_view.update_plan(organization_id=organization_id, plan_id=plan_id,
                                                 service_id=service_id, plan_name=plan_name,
                                                 description=description,
                                                 schedule_day=schedule_day, schedule_term=schedule_term,
                                                 term_payment=term_payment, registration_amount=registration_amount,
                                                 currency=currency, is_active=is_active)

    elif path == "get-plan":
        return membership_plans_view.return_plan(organization_id=organization_id, plan_id=plan_id)

    elif path == "return-all-plans":
        # NOTE this will return all main membership plans for subscribing to this API
        return membership_plans_view.return_all_plans(organization_id=organization_id)

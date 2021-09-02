***REMOVED***
***Memberships Management API***

***REMOVED***
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import typing
from flask import Blueprint, request, jsonify
from datetime import datetime, date
from security.api_authenticator import handle_api_auth
from config.exceptions import if_bad_request_raise
from utils.utils import date_string_to_date
from views import memberships_view, membership_plans_view

memberships_bp = Blueprint('memberships', __name__)


# NOTE: path is plan_id@organization_id
@memberships_bp.route("/api/v1/public/members/<string:path>", methods=['POST'])
@handle_api_auth
def get_members(path: str) -> tuple:
    plan_id, organization_id = path.split('@')

    return memberships_view.return_plan_members(organization_id=organization_id, plan_id=plan_id)


@memberships_bp.route("/api/v1/public/member", methods=['POST', 'PUT'])
@handle_api_auth
def create_member() -> tuple:
    ***REMOVED***
        create or update member
    ***REMOVED***
    # Raises Bad Request error if request is not in json format
    if_bad_request_raise(request)

    member_details: dict = request.get_json()
    uid: str = member_details.get("uid")
    organization_id: typing.Union[str, None] = member_details.get("organization_id")
    plan_id: str = member_details.get("plan_id")
    plan_start_date: date = date_string_to_date(member_details.get("plan_start_date", datetime.now().date()))

    return memberships_view.add_membership(organization_id=organization_id, uid=uid, plan_id=plan_id,
                                           plan_start_date=plan_start_date)


# NOTE: path is <uid@organization_id>
@memberships_bp.route("/api/v1/public/member/status/<string:path>", methods=['GET', 'PUT'])
@handle_api_auth
def get_update_status(path: str) -> tuple:
    ***REMOVED***
        plan_id for the status to get or update
    ***REMOVED***
    # Raises Bad Request error if request is not in json format
    if_bad_request_raise(request)

    if request.method == "PUT":
        json_data: dict = request.get_json()
        if ("status" in json_data) and (json_data["status"] != ""):
            status: str = json_data.get("status")
        else:
            message: str = "status is required and should be paid or unpaid"
            return jsonify({'status': True, 'message': message}), 500
        uid, organization_id = path.split("@")

        return memberships_view.set_membership_payment_status(organization_id=organization_id, uid=uid, status=status)
    elif request.method == "GET":
        ***REMOVED***
            return membership record    
        ***REMOVED***
        uid, organization_id = path.split("@")
        return memberships_view.is_member_off(organization_id=organization_id, uid=uid)


# NOTE: path is <plan_id@organization_id>
@memberships_bp.route("/api/v1/public/members/<string:path>/status/<string:status>", methods=["GET"])
@handle_api_auth
def get_plan_members_by_payment_status(path: str, status: str) -> tuple:
    plan_id, organization_id = path.split("@")
    if (plan_id != "") and (status != ""):
        return memberships_view.return_plan_members_by_payment_status(organization_id=organization_id,
                                                                      plan_id=plan_id, status=status)


# NOTE: path is <plan_id@organization_id>
@memberships_bp.route("/api/v1/public/membership/plan/<string:path>")
@handle_api_auth
def change_membership_plan(path: str) -> tuple:
    plan_id, organization_id = path.split("@")
    # Raises Bad Request error if request is not in json format
    if_bad_request_raise(request)

    if plan_id != "":
        json_data: dict = request.get_json()
        if ("uid" in json_data) and (json_data['uid'] != ""):
            uid: typing.Union[str, None] = json_data.get("uid")
        else:
            return jsonify({'status': False, 'message': 'User Id is required'}), 500

        if ('dest_plan_id' in json_data) and (json_data['dest_plan_id'] != ""):
            dest_plan_id: typing.Union[str, None] = json_data.get("dest_plan_id")
        else:
            return jsonify({"status": False, "message": "destination plan id is required"}), 500

        return memberships_view.change_membership(organization_id=organization_id,
                                                  uid=uid, origin_plan_id=plan_id,
                                                  dest_plan_id=dest_plan_id)


@memberships_bp.route('/api/v1/public/membership-plan', methods=["POST"])
@handle_api_auth
def create_membership_plan() -> tuple:
    # Raises Bad Request error if request is not in json format
    if_bad_request_raise(request)

    membership_plan_data: dict = request.get_json()

    return membership_plans_view.add_plan(membership_plan_data=membership_plan_data)


# NOTE path equal organization_id
@memberships_bp.route('/api/v1/public/membership-plans/<string:path>', methods=["GET"])
@handle_api_auth
def get_membership_plans(path: str) -> tuple:
    return membership_plans_view.return_all_plans(organization_id=path)


@memberships_bp.route('/api/v1/public/update-membership-plan', methods=["POST"])
@handle_api_auth
def update_membership_plan() -> tuple:
    # Raises Bad Request error if request is not in json format
    if_bad_request_raise(request)
    membership_plan: dict = request.get_json()
    if ("plan_id" in membership_plan) and (membership_plan["plan_id"] != ""):
        plan_id: typing.Union[str, None] = membership_plan.get("plan_id")
    else:
        return jsonify({'status': False, 'message': 'plan_id cannot be null'}), 500
    if ("plan_name" in membership_plan) and (membership_plan["plan_name"] != ""):
        plan_name: typing.Union[str, None] = membership_plan.get("plan_name")
    else:
        return jsonify({'status': False, 'message': "plan_name is required"}), 500
    if ("description" in membership_plan) and (membership_plan["description"] != ""):
        description: typing.Union[str, None] = membership_plan.get("description")
    else:
        return jsonify({'status': False, 'message': 'description is required'}), 500
    if ("schedule_day" in membership_plan) and (membership_plan["schedule_day"] != ""):
        schedule_day: typing.Union[int, None] = int(membership_plan.get("schedule_day")) \
            if membership_plan.get("schedule_day") is not None else None
    else:
        return jsonify({'status': False, 'message': 'schedule_day is required'}), 500
    if ("schedule_term" in membership_plan) and (membership_plan["schedule_term"] != ""):
        schedule_term: typing.Union[str, None] = membership_plan.get("schedule_term")
    else:
        return jsonify({'status': False, 'message': 'schedule_term is required'}), 500
    if ("term_payment" in membership_plan) and (membership_plan["term_payment"] != ""):
        term_payment: typing.Union[int, None] = int(membership_plan['term_payment']) \
            if membership_plan['term_payment'] is not None else None
    else:
        return jsonify({'status': False, 'message': 'term_payment is required'}), 500
    if ("registration_amount" in membership_plan) and (membership_plan["registration_amount"] != ""):
        registration_amount: typing.Union[int, None] = int(membership_plan["registration_amount"]) \
            if membership_plan.get("registration_amount") is not None else None
    else:
        return jsonify({'status': False, 'message': 'registration_amount is required'}), 500
    if ("currency" in membership_plan) and (membership_plan["currency"] != ""):
        currency: typing.Union[str, None] = membership_plan.get("currency")
    else:
        return jsonify({'status': False, 'message': 'currency is required'}), 500
    if ('is_active' in membership_plan) and (membership_plan['is_active'] != ""):
        is_active: bool = membership_plan.get("is_active")
    else:
        return jsonify({'status': False, 'message': 'is_active is required'}), 500

    if ("organization_id" in membership_plan) and (membership_plan["organization_id"] != ""):
        organization_id: typing.Union[str, None] = membership_plan.get("organization_id")
    else:
        return jsonify({'status': False, 'message': 'organization_id is required'}), 500

    return membership_plans_view.update_plan(organization_id=organization_id, plan_id=plan_id, plan_name=plan_name,
                                             description=description, term_payment=term_payment,
                                             registration_amount=registration_amount, schedule_day=schedule_day,
                                             schedule_term=schedule_term, currency=currency, is_active=is_active)


# NOTE: path is <uid@organization_id>
@memberships_bp.route('/api/v1/public/is-member-off/<string:path>', methods=["GET"])
@handle_api_auth
def is_member_off(path: str) -> tuple:
    ***REMOVED***
        for a specific user returns membership
    ***REMOVED***
    uid, organization_id = path.split("@")

    return memberships_view.is_member_off(organization_id=organization_id, uid=uid)


# NOTE: path is <uid@organization_id>
@memberships_bp.route('/api/v1/public/memberships-payment-amount/<string:path>', methods=["GET"])
@handle_api_auth
def payment_amount(path: str) -> tuple:
    ***REMOVED***
        for a specific member return payment amounts
    ***REMOVED***
    uid, organization_id = path.split("@")
    return memberships_view.payment_amount(organization_id=organization_id, uid=uid)


# NOTE: path is <uid@organization_id>
@memberships_bp.route('/api/v1/public/memberships-set-payment-status/<string:path>/<string:status>', methods=["GET"])
@handle_api_auth
def set_payment_status(path: str, status: str) -> tuple:
    uid, organization_id = path.split("@")
    return memberships_view.set_membership_payment_status(organization_id=organization_id, uid=uid, status=status)

import typing
from flask import Blueprint, request, jsonify
from datetime import datetime, date
from security.api_authenticator import handle_api_auth
from config.exceptions import InputError
from utils.utils import date_string_to_date
from views.memberships import MembershipsView, MembershipPlansView
memberships_bp = Blueprint('memberships', __name__)


# TODO - include organization_id for this routes, and refactor the view functions

# NOTE: path is plan_id@organization_id
@memberships_bp.route("/api/v1/members/<path:path>", methods=['POST'])
@handle_api_auth
def get_members(path: str) -> tuple:
    plan_id, organization_id = path.split('@')
    members_instance: MembershipsView = MembershipsView()
    return members_instance.return_plan_members(organization_id=organization_id, plan_id=plan_id)


@memberships_bp.route("/api/v1/member", methods=['POST', 'PUT'])
@handle_api_auth
def create_member() -> tuple:
    ***REMOVED***
        create or update member
    ***REMOVED***
    member_details: dict = request.get_json()
    if ("uid" in member_details) and (member_details["uid"] != ""):
        uid: str = member_details.get("uid")
    else:
        message: str = "uid is required"
        return jsonify({"status": False, "message": message}), 500

    if ("organization_id" in member_details) and (member_details["organization_id"] != ""):
        organization_id: typing.Union[str, None] = member_details.get("organization_id")
    else:
        message: str = "organization_id is required"
        return jsonify({"status": False, "message": message}), 500

    if ("plan_id" in member_details) and (member_details["plan_id"] != ""):
        plan_id: str = member_details.get("plan_id")
    else:
        message: str = "plan_id is required"
        return jsonify({"status": False, "message": message}), 500

    if ("plan_start_date" in member_details) and (member_details["plan_start_date"] != ""):
        plan_start_date: date = date_string_to_date(member_details.get("plan_start_date"))
    else:
        plan_start_date: date = datetime.now().date()

    members_view_instance: MembershipsView = MembershipsView()
    return members_view_instance.add_membership(organization_id=organization_id, uid=uid, plan_id=plan_id,
                                                plan_start_date=plan_start_date)


# NOTE: path is <uid@organization_id>
@memberships_bp.route("/api/v1/member/status/<path:path>", methods=['GET', 'PUT'])
@handle_api_auth
def get_update_status(path: str) -> tuple:
    ***REMOVED***
        plan_id for the status to get or update
    ***REMOVED***
    if request.method == "PUT":
        json_data: dict = request.get_json()
        if ("status" in json_data) and (json_data["status"] != ""):
            status: str = json_data.get("status")
        else:
            message: str = "status is required and should be paid or unpaid"
            return jsonify({'status': True, 'message': message}), 500
        uid, organization_id = path.split("@")
        membership_view_instance: MembershipsView = MembershipsView()
        return membership_view_instance.set_membership_status(organization_id=organization_id, uid=uid, status=status)
    elif request.method == "GET":
        ***REMOVED***
            return membership record    
        ***REMOVED***
        membership_view_instance: MembershipsView = MembershipsView()
        uid, organization_id = path.split("@")
        return membership_view_instance.is_member_off(organization_id=organization_id, uid=uid)


# NOTE: path is <plan_id@organization_id>
@memberships_bp.route("/api/v1/members/<path:path>/status/<path:status>", methods=["GET"])
@handle_api_auth
def get_plan_members_by_payment_status(path: str, status: str) -> tuple:
    plan_id, organization_id = path.split("@")
    if (plan_id != "") and (status != ""):
        membership_view_instance: MembershipsView = MembershipsView()
        return membership_view_instance.return_plan_members_by_payment_status(organization_id=organization_id,
                                                                              plan_id=plan_id, status=status)


# NOTE: path is <plan_id@organization_id>
@memberships_bp.route("/api/v1/membership/plan/<path:path>")
@handle_api_auth
def change_membership_plan(path: str) -> tuple:
    plan_id, organization_id = path.split("@")
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

        member_ship_instance_view: MembershipsView = MembershipsView()
        return member_ship_instance_view.change_membership(organization_id=organization_id,
                                                           uid=uid, origin_plan_id=plan_id,
                                                           dest_plan_id=dest_plan_id)


@memberships_bp.route('/api/v1/membership-plan', methods=["POST"])
def create_membership_plan() -> tuple:
    membership_plan_data: dict = request.get_json()
    member_ship_instance_view: MembershipPlansView = MembershipPlansView()
    return member_ship_instance_view.add_plan(membership_plan_data=membership_plan_data)


# NOTE path equal organization_id
@memberships_bp.route('/api/v1/membership-plans/<path:path>', methods=["GET"])
def get_membership_plans(path: str) -> tuple:
    member_ship_instance_view: MembershipPlansView = MembershipPlansView()
    return member_ship_instance_view.return_all_plans(organization_id=path)


@memberships_bp.route('/api/v1/update-membership-plan', methods=["POST"])
def update_membership_plan() -> tuple:
    member_ship_instance_view: MembershipPlansView = MembershipPlansView()
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

    return member_ship_instance_view.update_plan(organization_id=organization_id, plan_id=plan_id, plan_name=plan_name,
                                                 description=description, term_payment=term_payment,
                                                 registration_amount=registration_amount, schedule_day=schedule_day,
                                                 schedule_term=schedule_term, currency=currency, is_active=is_active)


# NOTE: path is <uid@organization_id>
@memberships_bp.route('/api/v1/is-member-off/<path:path>', methods=["GET"])
def is_member_off(path: str) -> tuple:
    ***REMOVED***
        for a specific user returns membership
    ***REMOVED***
    uid, organization_id = path.split("@")
    membership_instance: MembershipsView = MembershipsView()
    return membership_instance.is_member_off(organization_id=organization_id, uid=uid)


# NOTE: path is <uid@organization_id>
@memberships_bp.route('/api/v1/memberships-payment-amount/<path:path>', methods=["GET"])
def payment_amount(path: str) -> tuple:
    ***REMOVED***
        for a specific member return payment amounts
    ***REMOVED***
    uid, organization_id = path.split("@")
    membership_instance: MembershipsView = MembershipsView()
    return membership_instance.payment_amount(organization_id=organization_id, uid=uid)


# NOTE: path is <uid@organization_id>
@memberships_bp.route('/api/v1/memberships-set-payment-status/<path:path>/<path:status>', methods=["GET"])
def set_payment_status(path: str, status: str) -> tuple:
    uid, organization_id = path.split("@")
    membership_instance: MembershipsView = MembershipsView()
    return membership_instance.set_payment_status(organization_id=organization_id, uid=uid, status=status)



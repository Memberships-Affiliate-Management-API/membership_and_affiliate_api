***REMOVED***
    **Module Memberships Client API**
        Memberships related api requests will be handled here
***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from typing import Optional
from flask import Blueprint, request, current_app
from config.exceptions import if_bad_request_raise, UnAuthenticatedError, error_codes

memberships_client_api_bp = Blueprint('memberships_client_api', __name__)


@memberships_client_api_bp.route('/_api/v1/client/memberships/<string:path>', methods=['POST'])
def memberships_client_api(path: str) -> tuple:
    ***REMOVED***
        **memberships_client_api**
            handles client admin requests for memberships -
            this means clients or developers

            **USE CASES**
                1. will subscribe to membership plans in order to use this website from this endpoint
            - this endpoints can be called from the client dashboard
            in order to start using the API for as a paid client or a free client
    :param path:
    :return:
    ***REMOVED***
    if_bad_request_raise(request)
    json_data: dict = request.get_json()

    if isinstance(json_data, dict):
        secret_key: Optional[str] = json_data.get('SECRET_KEY')

        if not isinstance(secret_key, str) or secret_key != current_app.config.get('SECRET_KEY'):
            message: str = 'User Not Authorized: you cannot perform this action'
            raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code,
                                       description=message)

        elif path == "join-plan":
            pass
        elif path == "leave-plan":
            pass

    return "OK", 200


@memberships_client_api_bp.route('_api/v1/client/admin/memberships/<string:path>', methods=["POST"])
def client_memberships_management(path: str) -> tuple:
    ***REMOVED***
        **client_memberships_management**
            used to manage client's membership plans which they are offering to the
            public - this api will also be called from client dashboard app

            **USE CASES**
                1. create and update services or products
                2. create and update membership plans / payment plans for services or products

    :param path:
    :return:
    ***REMOVED***
    pass
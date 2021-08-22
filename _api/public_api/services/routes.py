***REMOVED***
    **Public facing Services API**

***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from typing import Optional
from flask import Blueprint, request, current_app
from config.exceptions import if_bad_request_raise, UnAuthenticatedError, error_codes
from security.api_authenticator import handle_api_auth
from views.services import ServicesView

services_public_api_bp = Blueprint('services_public_api', __name__)


@services_public_api_bp.route('/api/v1/public/service/<string:org_id>/<string:service_id>', methods=["GET"])
@handle_api_auth
def get_services(org_id: str, service_id: str) -> tuple:
    ***REMOVED***
        **public_services_api**
            returns a service governed by organization_id and service_id
    :param org_id:
    :param service_id:
    :return:
    ***REMOVED***
    service_view: ServicesView = ServicesView()
    return service_view.get_service(service_id=service_id, organization_id=org_id)


@services_public_api_bp.route('/api/v1/public/services/<string:org_id>', methods=["GET"])
@handle_api_auth
def get_all_services(org_id: str) -> tuple:
    ***REMOVED***
        **public_services_api**
            returns a service governed by organization_id and service_id
    :param org_id:
    :return:
    ***REMOVED***
    service_view: ServicesView = ServicesView()
    return service_view.return_services(organization_id=org_id)

***REMOVED***
    **Services API Module**

***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from typing import Optional
from flask import Blueprint, request, current_app
from config.exceptions import if_bad_request_raise, UnAuthenticatedError, error_codes
from views.services import ServicesView

services_client_api_bp = Blueprint('services_client_api', __name__)


@services_client_api_bp.route('/_api/v1/client/services/<string:path>', methods=["POST"])
def services_api(path: str) -> tuple:
    ***REMOVED***
        **services_api**

    :param path:
    :return:
    ***REMOVED***
    if_bad_request_raise(request)
    services_data: dict = request.get_json()
    secret_key: Optional[str] = services_data.get('SECRET_KEY')
    services_view_instance: ServicesView = ServicesView()

    if not isinstance(secret_key, str) or secret_key != current_app.config.get('SECRET_KEY'):
        message: str = 'User Not Authorized: you cannot perform this action'
        raise UnAuthenticatedError(status=error_codes.access_forbidden_error_code, description=message)

    organization_id: Optional[str] = services_data.get('organization_id')
    uid: Optional[str] = services_data.get('uid')
    name: Optional[str] = services_data.get('name')
    description: Optional[str] = services_data.get('description')
    category: Optional[str] = services_data.get('category')
    image_url: Optional[str] = services_data.get('image_url')
    home_url: Optional[str] = services_data.get('home_url')

    if path == "create-service":
        return services_view_instance.create_service(organization_id=organization_id, uid=uid, name=name,
                                                     description=description, category=category, image_url=image_url,
                                                     home_url=home_url)

    elif path == "update-service":
        services_id: Optional[str] = services_data.get('services_id')
        return services_view_instance.update_service(services_id=services_id, organization_id=organization_id, uid=uid,
                                                     name=name, description=description, category=category,
                                                     image_url=image_url, home_url=home_url)
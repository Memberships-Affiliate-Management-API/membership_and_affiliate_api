***REMOVED***
    routes for api_keys endpoints
***REMOVED***
import typing
from flask import Blueprint, request
from config.exceptions import RequestError
from security.users_authenticator import handle_users_auth
from views.apikeys import APIKeysView

api_keys_bp = Blueprint('api_keys', __name__)


@api_keys_bp.route('/api/v1/api-keys', methods=["GET", "POST"])
@handle_users_auth
def api_keys() -> tuple:
    json_data: dict = request.get_json()
    api_view_instance: APIKeysView = APIKeysView()
    if request.method == "GET":
        organization_id = json_data.get('organization_id')
        return api_view_instance.return_all_organization_keys(organization_id=organization_id)
    elif request.method == "POST":
        organization_id = json_data.get('organization_id')
        uid = json_data.get('uid')
        return api_view_instance.create_keys(uid=uid, organization_id=organization_id)
    else:
        message: str = "RequestError : cannot understand request, please see documentation"
        raise RequestError(status=500, description=message)

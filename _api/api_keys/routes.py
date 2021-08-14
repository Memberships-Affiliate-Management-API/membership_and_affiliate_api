***REMOVED***
    **api keys module**
        will be used by clients and application to get access to api keys
        for authentication purposes
***REMOVED***
from typing import Optional
from flask import Blueprint, request, current_app
from config.exceptions import UnAuthenticatedError, error_codes
from views.apikeys import APIKeysView

api_keys_bp = Blueprint('api-keys', __name__)


@api_keys_bp.route('/_api/admin/api-keys/<string:key>/org/<string:organization_id>', methods=["POST"])
def return_api_key(key: str, organization_id) -> tuple:
    ***REMOVED***
        **return api_key**
            this module cannot be called from the outside
    :param key: api key to verify
    :param organization_id: the organization_id of the organization the api key belongs to
    :return:
    ***REMOVED***
    json_data: dict = request.get_json()
    secret_key: Optional[str] = json_data.get('SECRET_KEY')
    if isinstance(secret_key, str) and secret_key == current_app.config.get('SECRET_KEY'):
        api_view_instance: APIKeysView = APIKeysView()
        return api_view_instance.get_api_key(api_key=key, organization_id=organization_id)

    message: str = "User not Authorized: you are not authorized to call this API"
    raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

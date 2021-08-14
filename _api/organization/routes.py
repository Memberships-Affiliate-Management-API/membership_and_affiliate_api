***REMOVED***
    **Organization Routes Module**
        Handles API Requests for Organizations

***REMOVED***
from typing import Optional

from flask import request, Blueprint, current_app
organizations_api_bp = Blueprint('organizations_api', __name__)


@organizations_api_bp.route('/api/organization', methods=['GET', 'POST'])
def organization_main() -> tuple:
    ***REMOVED***
        **organization_main**
            handles requests related to organizations creations and manipulation

        **NOTE**
            this api will only be called from the main application -
            that means no users for clients will make requests to this endpoint
    :return:
    ***REMOVED***
    # NOTE: create organization
    if request.method == "POST":
        json_data: dict = request.get_json()
        secret_key: str = current_app.config.get('SECRET_KEY')
        organization_name: Optional[str] = json_data.get('organization_name')
        description: Optional[str] = json_data.get('description')


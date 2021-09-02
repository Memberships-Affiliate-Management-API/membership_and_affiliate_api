***REMOVED***
    this is a private route
***REMOVED***

__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from typing import List, Optional

from flask import Blueprint, render_template, url_for, get_flashed_messages, redirect, flash

from config.exceptions import status_codes
from security.users_authenticator import handle_users_auth
from utils.utils import create_id

client_dashboard_bp = Blueprint('client_dashboard', __name__)


temp_organizations: List[dict] = [
    {
        'organization_id': create_id(),
        'organization_name': 'Memberships API',
        'description': 'if you are interested in our api tools you are welcome'

    },
    {
        'organization_id': create_id(),
        'organization_name': 'Memberships APIKeysView & Memberships',
        'description': 'if you are interested in our api tools you are welcome'
    }
]


@client_dashboard_bp.route('/client/dashboard', methods=["GET"])
@handle_users_auth
def client_dashboard(current_user: Optional[dict]) -> tuple:
    ***REMOVED***
        **client_dashboard**
            allows client to get access to their organizations
    :param current_user:
    :return:
    ***REMOVED***
    get_flashed_messages()
    if not isinstance(current_user, dict) or not bool(current_user.get('uid')):
        # TODO: insure local cache does not cache info if redirected
        flash('Please login or register to start using this app')
        return redirect(url_for('memberships_main.memberships_main_routes', path='login'))

    # TODO - retrieve a list of organizations here

    return render_template('client/dashboard.html', current_user=current_user,
                           organizations_list=temp_organizations), status_codes.status_ok_code


@client_dashboard_bp.route('/client/dashboard/<path:path>', methods=["GET"])
@handle_users_auth
def client_dashboard_routes(current_user: Optional[dict], path: str) -> tuple:
    get_flashed_messages()
    if not isinstance(current_user, dict) or not bool(current_user.get('uid')):
        flash('Please login or register to start using this app')
        return redirect(url_for('memberships_main.memberships_main_routes', path='login'))

    if path == "my-account":
        return render_template('client/my_account.html', current_user=current_user), status_codes.status_ok_code
    elif path == "organizations":
        # print(f"organizations list : {temp_organizations}")
        return render_template('client/organizations.html', current_user=current_user,
                               organizations_list=temp_organizations), status_codes.status_ok_code
    elif path == "affiliates":
        return render_template('client/affiliates.html', current_user=current_user), status_codes.status_ok_code
    elif path == "users":
        return render_template('client/users.html', current_user=current_user), status_codes.status_ok_code
    elif path == "api-keys":
        return render_template('client/api_keys.html', current_user=current_user), status_codes.status_ok_code
    elif path == "accounts":
        return render_template('client/subscriptions.html', current_user=current_user), status_codes.status_ok_code
    elif path == "help-desk":
        return render_template('client/helpdesk.html', current_user=current_user), status_codes.status_ok_code



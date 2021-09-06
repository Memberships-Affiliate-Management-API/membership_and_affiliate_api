"""
    **Client Home Route**
        entry page to client dashboard
"""

__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from typing import Optional

from flask import Blueprint, render_template, get_flashed_messages

from cache.cache_manager import app_cache
from config.exceptions import status_codes
from security.users_authenticator import logged_user
from utils.utils import return_ttl

client_home_bp = Blueprint('client_home', __name__)


@client_home_bp.route('/client', methods=["GET"])
@logged_user
@app_cache.cache.cached(timeout=return_ttl('short'))
def client_home(current_user: Optional[dict]) -> tuple:
    """
        **client_home**
            entry page to client dashboard
    :param current_user:
    :return:
    """
    get_flashed_messages()
    if isinstance(current_user, dict) and bool(current_user.get('uid')):
        return render_template('client/home.html', current_user=current_user), status_codes.status_ok_code
    else:
        return render_template('client/home.html'), status_codes.status_ok_code




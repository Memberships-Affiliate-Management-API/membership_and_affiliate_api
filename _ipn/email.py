***REMOVED***
    **Email Messages IPN Endpoints**
    notifications for when emails have been sent will be received here

***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from flask import Blueprint
from main import app_cache
from utils.utils import return_ttl, can_cache

email_ipn_bp = Blueprint("email_ipn", __name__)


@email_ipn_bp.route('/_ipn/v1/email/received/<path:path>', methods=["GET", "POST"])
@app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
def email_received_ipn(path: str) -> tuple:
    ***REMOVED***
        :param path: organization_id
        :return: OK, 200
    ***REMOVED***

    return "OK", 200


@email_ipn_bp.route('/_ipn/v1/email/mailgun/<string:path>', methods=["GET", "POST"])
@app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
def email_sent_ipn(path: str) -> tuple:
    ***REMOVED***
        Delivered ipn for mailgun
        :param path: organization_id
        :return: OK, 200
    ***REMOVED***
    # NOTE: Delivered ipn will end up here
    if path == "delivered":
        pass
    elif path == "clicks":
        pass
    elif path == "opens":
        pass
    elif path == "failure":
        pass
    elif path == "spam":
        pass
    elif path == "unsubscribe":
        pass

    return "OK", 200

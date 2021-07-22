***REMOVED***
    notifications for when emails have been sent will be received here

***REMOVED***
from flask import Blueprint, request
email_ipn_bp = Blueprint("email_ipn", __name__)


@email_ipn_bp.route('/_ipn/v1/email/received/<path:path>', methods=["GET", "POST"])
def email_received_ipn(path: str) -> tuple:
    ***REMOVED***
        :param path: organization_id
        :return: OK, 200
    ***REMOVED***

    return "OK", 200


@email_ipn_bp.route('/_ipn/v1/email/sent/<path:path>', methods=["GET", "POST"])
def email_sent_ipn(path: str) -> tuple:
    ***REMOVED***
        :param path: organization_id
        :return: OK, 200
    ***REMOVED***

    return "OK", 200

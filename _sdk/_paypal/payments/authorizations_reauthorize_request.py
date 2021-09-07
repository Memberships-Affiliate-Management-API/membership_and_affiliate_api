# This class was generated on Tue, 10 Jul 2018 10:40:35 PDT by version 0.1.0-dev+0ee05a-dirty of Braintree SDK Generator
# authorizations_reauthorize_request.py
# @version 0.1.0-dev+0ee05a-dirty
# @type request
# DO NOT EDIT
import paypalhttp
from urllib.parse import quote  # Python 3+


# noinspection PyDictCreation
class AuthorizationsReauthorizeRequest:
    """
    Reauthorizes an authorized PayPal account payment, by ID. To ensure that funds are still available, reauthorize an authorized payment after its initial three-day honor period expires.<br/><br/>After the three-day honor period expires,
    you can reauthorize an authorized payment only once from days four to 29. If 30 days have passed since the date of
    the authorized payment, you must create an authorized payment instead.<br/><br/>A
    reauthorized payment itself has a new three-day honor period. You can reauthorize an authorized payment once
    for up to 115% of the original authorized amount and not to exceed an increase of $75 USD.<br/><br/>Supports
    the <code>amount</code> request parameter only.
    """
    def __init__(self, authorization_id):
        self.verb = "POST"
        self.path = "/v2/payments/authorizations/{authorization_id}/reauthorize?".replace("{authorization_id}", quote(str(authorization_id)))
        self.headers = {}
        self.headers["Content-Type"] = "application/json"
        self.body = None

    def pay_pal_request_id(self, pay_pal_request_id):
        self.headers["PayPal-Request-Id"] = str(pay_pal_request_id)

    def prefer(self, prefer):
        self.headers["Prefer"] = str(prefer)

    def request_body(self, reauthorize_request):
        self.body = reauthorize_request
        return self
